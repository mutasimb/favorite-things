from django.db import models
import uuid
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Create your models here.


class FavThing(models.Model):
    pid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=60)
    description = models.TextField(
        blank=True, validators=[MinLengthValidator(10)], default='')
    category = models.CharField(max_length=60, default="uncategorized")
    ranking = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    meta = models.TextField(
        blank=False, default='[]')
