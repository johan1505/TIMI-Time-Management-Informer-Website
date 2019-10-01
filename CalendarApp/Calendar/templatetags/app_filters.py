from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_total_hours')
def get_due_hour_string(value):
    return (value.days * 24) + (value.seconds // 3600)

@register.filter(name='get_total_minutes')
def get_due_min_string(value):
   return (value.seconds % 3600) // 60