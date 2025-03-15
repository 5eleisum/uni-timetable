from django import template

register = template.Library()

@register.filter
def filter_by_day(timetables, day):
    return timetables.filter(day=day)

@register.filter
def filter_by_hour(timetables, hour):
    return timetables.filter(hours__start_time=hour)