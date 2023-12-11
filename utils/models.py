from django.utils import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated at"), default=timezone.now)

    class Meta:
        abstract = True
