from django import template
from datetime import date, timedelta

register = template.Library()
colors = ['#eb4d4b','#18dcff','#f9ca24', '#7efff5','#00b894', '#ff4d4d','#eb4d4b','#ff3838','#1289A7','#63cdda','#eccc68','#6ab04c','#3ae374','#34ace0', '#227093','#C4E538','#b33939','#4834d4','#7ed6df','#0652DD','#be2edd','#e15f41','#ff5252','#22a6b3','#7ed6df','#1e90ff',
        '#badc58','#30336b', '#32ff7e','#0984e3','#ED4C67','#D980FA','#fbc531','#f0932b','#2f3542', '#2ed573','#f78fb3','#ff6b81','#786fa6','#7158e2','#ffb142','#10ac84','#01a3a4']

@register.filter(name="get_total_time_string")
def getTotalTimeString(value):
    hours = getHours(value)
    minutes = getMinutes(value)
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

@register.filter(name="get_total_time_chart_value")
def getTotalTimeChartValue(value):
    hours = getHours(value) * 100
    minutes = getMinutes(value)
    return (hours + minutes)

@register.filter(name="get_color")
def getColor(value):
    # Returns a color based on the chartValue mod 32 (size of the array of colors)
    return colors[getTotalTimeChartValue(value) % len(colors)] 
     

def getHours(value):
    return (value.days * 24) + (value.seconds // 3600)

def getMinutes(value):
    return (value.seconds % 3600) // 60