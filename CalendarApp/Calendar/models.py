from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    eventTitle = models.CharField(max_length = 100)
    durationTime = models.DurationField()
    def _str_(self):
        return self.eventTitle

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete="CASCADE")
    events = models.ManyToManyField(Event)
    creationDate = models.DateTimeField(default = timezone.now)
    startDate = models.DateTimeField(default = timezone.now) 
    endDate = models.DateTimeField(default = timezone.now)