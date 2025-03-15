from django.shortcuts import render, redirect
from .models import Timetable, Course, Hour
from .templatetags import timetable_filters
from django.db.models import Q

def timetable_view(request):
    year = request.GET.get('year', 1)
    timetables = Timetable.objects.filter(Q(course__year=year) | Q(second_course__year=year))
    days = [day[0] for day in Timetable.DAY_CHOICES]
    hours = Hour.objects.all()
    return render(request, 'timetable.html', {'timetables': timetables, 'days': days, 'hours': hours, 'year': year})

def home_view(request):
    return render(request, 'home.html')