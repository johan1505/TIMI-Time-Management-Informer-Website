from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone


class Summary(models.Model):
    user = models.ForeignKey(User, on_delete="CASCADE")
    # Here the ForignKey is used as there is a Many-to-One relationship between summaries and user
    # A user CAN have multiple summaries
    activities = ArrayField(models.CharField(max_length = 100)) # Array of CharFields, each representes the of an activity with a max length of 100 characters
    times = ArrayField(models.DurationField()) # Array of DurationFields, each duration represents how much time a user spent on it correspondent activity
    startDate = models.DateTimeField(default = timezone.now) # Start date of the week
    endDate = models.DateTimeField(default = timezone.now)   # End date of the week
