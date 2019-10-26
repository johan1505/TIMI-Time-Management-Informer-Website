from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_total_hours')
def get_due_hour_string(value):
    return (value.days * 24) + (value.seconds // 3600)

@register.filter(name='get_total_minutes')
def get_due_min_string(value):
   return (value.seconds % 3600) // 60

@register.filter(name="get_total_time")
def getTotalTimeString(value):
    hours = (value.days * 24) + (value.seconds // 3600)
    minutes = (value.seconds % 3600) // 60
    outputTime = ""
    if hours > 0:
        if hours == 1:
            outputTime = outputTime +  str(hours) + " hour " 
        else:
            outputTime = outputTime +  str(hours) + " hours " 
    if minutes > 0:
        if minutes == 1:
            outputTime = outputTime + str(minutes) + " minute"
        else:
            outputTime = outputTime + str(minutes) + " minutes"
    return outputTime
