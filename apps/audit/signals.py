from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import inspect

from .models import Audit
from ..operations.models import Buy, Sell
from ..stocks.models import Stock, StockPrice, StockType, Dividend
from ..authentication.models import User


@receiver(pre_save, sender=User)
@receiver(pre_save, sender=Buy)
@receiver(pre_save, sender=Sell)
@receiver(pre_save, sender=Stock)
@receiver(pre_save, sender=StockType)
@receiver(pre_save, sender=StockPrice)
@receiver(pre_save, sender=Dividend)
def check_update(sender, instance, **kwargs):
    if instance.pk is not None and not kwargs['raw']:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except Exception as e:
            raise Exception(str(e))
        else:
            fields_name = {attr.attname: attr.column for attr in instance._meta.fields if attr.attname not in ['last_login']}
            fields_diff = list(filter(lambda field: getattr(instance, field, None) != getattr(obj, field, None), fields_name))
            changes = {attr: obj.__dict__[attr] for attr in fields_diff}

            if len(changes) > 0:
                records = Audit(table=instance._meta.db_table, object_id=instance.pk, old_values=changes, user_id=get_usuario())
                records.save()

@receiver(post_save, sender=User)
@receiver(post_save, sender=Buy)
@receiver(post_save, sender=Sell)
@receiver(post_save, sender=Stock)
@receiver(post_save, sender=StockType)
@receiver(post_save, sender=StockPrice)
@receiver(post_save, sender=Dividend)
def save_created(sender, instance, created, **kwargs):
    if created:
        try:
            records = Audit(table=instance._meta.db_table, object_id=instance.pk, old_values='created', user_id=get_usuario())
            records.save()
        except Exception as e:
            raise Exception(str(e))

def get_usuario():
    frame = inspect.currentframe()
    try:
        while frame:
            if 'request' in frame.f_locals:
                request = frame.f_locals['request']
                if request.user.id is not None:
                    return request.user.id
                
            frame = frame.f_back
    except:
        return None
    finally:
        del frame