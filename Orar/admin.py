from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Instructor, Group, Room, Course, Timetable, Hour
from .forms import TimetableForm

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count', 'assigned_year')
    search_fields = ('name',)
    list_filter = ('student_count',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)
    list_filter = ('capacity',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ('year',)
    search_fields = ('name', 'instructor__name')

@admin.register(Hour)
class HoursAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')

class InstructorFilter(admin.SimpleListFilter):
    title = 'Instructor'
    parameter_name = 'instructor'

    def lookups(self, request, model_admin):
        instructors = set(Instructor.objects.all())
        return [(instructor.id, instructor.name) for instructor in instructors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(instructor__id=self.value()) | queryset.filter(second_instructor__id=self.value())
        return queryset

class RoomFilter(admin.SimpleListFilter):
    title = 'Room'
    parameter_name = 'room'

    def lookups(self, request, model_admin):
        rooms = set(Room.objects.all())
        return [(room.id, room.name) for room in rooms]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(room__id=self.value()) | queryset.filter(second_room__id=self.value())
        return queryset

class WeekTypeFilter(admin.SimpleListFilter):
    title = 'Week Type'
    parameter_name = 'week_type'

    def lookups(self, request, model_admin):
        week_types = set(Timetable.objects.values_list('week_type', flat=True)) | set(Timetable.objects.values_list('second_week_type', flat=True))
        return [(week_type, week_type) for week_type in week_types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(week_type=self.value()) | queryset.filter(second_week_type=self.value())
        return queryset

class CourseTypeFilter(admin.SimpleListFilter):
    title = 'Course Type'
    parameter_name = 'course_type'

    def lookups(self, request, model_admin):
        course_types = set(Timetable.objects.values_list('course_type', flat=True)) | set(Timetable.objects.values_list('second_course_type', flat=True))
        return [(course_type, course_type) for course_type in course_types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(course_type=self.value()) | queryset.filter(second_course_type=self.value())
        return queryset

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    form = TimetableForm
    list_display = ('display_courses', 'display_instructors', 'display_course_types', 'display_rooms', 'day', 'display_week_types', 'hours')
    list_filter = (InstructorFilter, RoomFilter, WeekTypeFilter, CourseTypeFilter, 'day', 'course__year')
    search_fields = ('course__name', 'room__name')

    class Media:
        js = ('admin/js/timetable.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def display_courses(self, obj):
        if obj.class_type == 'Dual Class' or obj.class_type == 'Different Subgroups':
            return f"{obj.course} + {obj.second_course}"
        return obj.course
    display_courses.short_description = 'Courses'

    def display_instructors(self, obj):
        if obj.class_type == 'Dual Class' or obj.class_type == 'Different Subgroups':
            return f"{obj.instructor} + {obj.second_instructor}"
        return obj.instructor
    display_instructors.short_description = 'Instructors'
    
    def display_rooms(self, obj):
        if obj.class_type == 'Dual Class' or obj.class_type == 'Different Subgroups':
            return f"{obj.room} + {obj.second_room}"
        return obj.room
    display_rooms.short_description = 'Rooms'
    
    def display_week_types(self, obj):
        if obj.class_type == 'Dual Class' or obj.class_type == 'Different Subgroups':
            return f"{obj.week_type} + {obj.second_week_type}"
        return obj.week_type
    display_week_types.short_description = 'Week Types'
    
    def display_course_types(self, obj):
        if obj.class_type == 'Dual Class' or obj.class_type == 'Different Subgroups':
            return f"{obj.course_type} + {obj.second_course_type}"
        return obj.course_type
    display_course_types.short_description = 'Course Types'