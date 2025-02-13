from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import inspect

from .models import Audit
from ..operations.models import Buy, Sell, Custody, CustodyDividend, CustodySnapshot
from ..assets.models import Asset, AssetPrice, AssetType, Dividend, Sector, SubSector
from ..authentication.models import User


@receiver(pre_save, sender=User)
@receiver(pre_save, sender=Buy)
@receiver(pre_save, sender=Sell)
@receiver(pre_save, sender=Asset)
@receiver(pre_save, sender=Sector)
@receiver(pre_save, sender=SubSector)
@receiver(pre_save, sender=AssetType)
@receiver(pre_save, sender=AssetPrice)
@receiver(pre_save, sender=Dividend)
@receiver(pre_save, sender=Custody)
@receiver(pre_save, sender=CustodyDividend)
@receiver(pre_save, sender=CustodySnapshot)
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
@receiver(post_save, sender=Asset)
@receiver(post_save, sender=Sector)
@receiver(post_save, sender=SubSector)
@receiver(post_save, sender=AssetType)
@receiver(post_save, sender=AssetPrice)
@receiver(post_save, sender=Dividend)
@receiver(post_save, sender=Custody)
@receiver(post_save, sender=CustodyDividend)
@receiver(post_save, sender=CustodySnapshot)
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