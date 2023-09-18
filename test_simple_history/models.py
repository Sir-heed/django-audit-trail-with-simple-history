from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model() 


class AuditAbstractModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
        verbose_name=_('created on'),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        null=True,
        verbose_name=_('modified on'),
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret
