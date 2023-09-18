from django.contrib.auth.models import User
from django.db import models
from simple_history import register
from simple_history.models import HistoricalRecords

from test_simple_history.models import AuditAbstractModel

class Poll(AuditAbstractModel):
    """Model with history field"""
    history = HistoricalRecords()  # No need to register
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(AuditAbstractModel):
    """Model without history field"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


# Register model for log
register(User)
register(Choice)
