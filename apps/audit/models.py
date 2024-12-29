from django.db import models

from ..authentication.models import User

class Audit(models.Model):
    """
    Model to store the changes/updates of some other system models

    table: table name of changes
    object_id: Object ID that the changes took place
    updated_at: Datetime that the changes took place
    old_values: Table fields name affected by changes with their previous values
    user: 'apps.authentication.models' object executed the changes
    """

    table = models.CharField(max_length=100, blank=False, null=False)
    object_id = models.IntegerField(blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    old_values = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
