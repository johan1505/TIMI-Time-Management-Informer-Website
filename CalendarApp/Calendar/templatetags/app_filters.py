from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_total_hours')
def get_due_date_string(value):
    return (value.days * 24) + (value.seconds / 3600)