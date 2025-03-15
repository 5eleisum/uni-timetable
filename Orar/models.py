from django.db import models
from django.core.exceptions import ValidationError

class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.capacity} seats)"

class Course(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} (Year: {self.year})"

class Hour(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
    
class Group(models.Model):
    name = models.CharField(max_length=5)
    student_count = models.IntegerField()
    assigned_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.student_count} students, year {self.assigned_year})"

class Timetable(models.Model):
    CLASS_TYPE_CHOICES = [
        ('Single Class', 'Single Class'),
        ('Dual Class', 'Dual Class'),
        ('Different Subgroups', 'Different Subgroups'),
    ]
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    WEEK_TYPE_CHOICES = [
        ('Odd Weeks', 'Odd Weeks'),
        ('Even Weeks', 'Even Weeks'),
        ('Any Week', 'Any Week'),
    ]
    COURSE_TYPE_CHOICES = [
        ('Lecture', 'Lecture'),
        ('Laboratory', 'Laboratory'),
        ('Seminar', 'Seminar'),
    ]
    class_type = models.CharField(max_length=20, choices=CLASS_TYPE_CHOICES, default='Single Class')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAY_CHOICES)
    hours = models.ForeignKey(Hour, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    week_type = models.CharField(max_length=10, choices=WEEK_TYPE_CHOICES, null=True, blank=True)
    
    # Fields for the second class in "Dual Class" or "Different Subgroups"
    second_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='second_course', null=True, blank=True)
    second_course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, null=True, blank=True)
    second_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='second_instructor', null=True, blank=True)
    second_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='second_room', null=True, blank=True)
    second_week_type = models.CharField(max_length=10, choices=WEEK_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        if self.class_type == 'Single Class':
            return f"{self.course} ({self.course_type}) in {self.room} from {self.hours.start_time} to {self.hours.end_time} taught by {self.instructor} on {self.day} ({self.week_type})"
        elif self.class_type == 'Dual Class':
            return f"{self.course} ({self.course_type}) in {self.room} from {self.hours.start_time} to {self.hours.end_time} taught by {self.instructor} on {self.day} ({self.week_type}) | {self.second_course} ({self.second_course_type}) in {self.second_room} from {self.hours.start_time} to {self.hours.end_time} taught by {self.second_instructor} on {self.day} ({self.second_week_type})"
        elif self.class_type == 'Different Subgroups':
            return f"{self.course} ({self.course_type}) in {self.room} from {self.hours.start_time} to {self.hours.end_time} taught by {self.instructor} on {self.day} ({self.week_type}) | {self.second_course} ({self.second_course_type}) in {self.second_room} from {self.hours.start_time} to {self.hours.end_time} taught by {self.second_instructor} on {self.day} ({self.second_week_type})"

    def save(self, *args, **kwargs):
        # Ensure at least one course is provided for "Different Subgroups"
        if self.class_type == 'Different Subgroups' and not (self.course or self.second_course):
            raise ValidationError("At least one of the course fields (course or second_course) must be filled for 'Different Subgroups'")
        
        if self.class_type == 'Single Class':
            if not self.course:
                raise ValidationError("Course must be provided for 'Single Class'")
            if not self.course_type:
                raise ValidationError("Course type must be provided for 'Single Class'")
            if not self.instructor:
                raise ValidationError("Instructor must be provided for 'Single Class'")
            if not self.room:
                raise ValidationError("Room must be provided for 'Single Class'")
            if not self.week_type:
                raise ValidationError("Week type must be provided for 'Single Class'")
        
        if self.class_type == 'Dual Class':
            if not self.course or not self.second_course:
                raise ValidationError("Both course fields (course and second_course) must be filled for 'Dual Class'")
            if not self.course_type or not self.second_course_type:
                raise ValidationError("Both course type fields (course_type and second_course_type) must be filled for 'Dual Class'")
            if not self.instructor or not self.second_instructor:
                raise ValidationError("Both instructor fields (instructor and second_instructor) must be filled for 'Dual Class'")
            if not self.room or not self.second_room:
                raise ValidationError("Both room fields (room and second_room) must be filled for 'Dual Class'")
            if not self.week_type or not self.second_week_type:
                raise ValidationError("Both week type fields (week_type and second_week_type) must be filled for 'Dual Class'")
            if self.room and self.group.student_count > self.room.capacity:
                raise ValidationError(f"Room {self.room} is too small for group {self.group}")
        
        if self.second_room and self.group.student_count > self.second_room.capacity:
            raise ValidationError(f"Room {self.second_room} is too small for group {self.group}")
        
        if self.course and self.group.assigned_year != self.course.year:
            raise ValidationError(f"Group {self.group} is not assigned to the same year as course {self.course}")
        
        if self.second_course and self.group.assigned_year != self.second_course.year:
            raise ValidationError(f"Group {self.group} is not assigned to the same year as course {self.second_course}")

        # Check for overlapping courses
        overlapping_timetables = Timetable.objects.filter(
            day=self.day,
            hours=self.hours,
        ).exclude(id=self.id)

        for timetable in overlapping_timetables:
            if (timetable.course and timetable.course.year):
                if (self.course and self.course.year == timetable.course.year):
                    raise ValidationError(f"Course {self.course} overlaps with another course on {self.day} from {self.hours.start_time} to {self.hours.end_time}")
                elif (self.second_course and self.second_course.year == timetable.course.year):
                    raise ValidationError(f"Course {self.second_course} overlaps with another course on {self.day} from {self.hours.start_time} to {self.hours.end_time}")
            elif (timetable.second_course and timetable.second_course.year):
                if (self.course and self.course.year == timetable.second_course.year):
                    raise ValidationError(f"Course {self.course} overlaps with another course on {self.day} from {self.hours.start_time} to {self.hours.end_time}")
                elif (self.second_course and self.second_course.year == timetable.second_course.year):
                    raise ValidationError(f"Course {self.second_course} overlaps with another course on {self.day} from {self.hours.start_time} to {self.hours.end_time}")
            if self.week_type == timetable.week_type and self.course.year == timetable.course.year and self.class_type == 'Single Class':
                raise ValidationError(f"Course {self.course} overlaps with another course on {self.day} ({self.week_type}) from {self.hours.start_time} to {self.hours.end_time}")
            if timetable.instructor:
                if self.instructor == timetable.instructor:
                    if self.course and timetable.course and self.course.year != timetable.course.year:
                        if self.week_type == timetable.week_type or self.week_type == 'Any Week' or timetable.week_type == 'Any Week':
                            raise ValidationError(f"Instructor {self.instructor} is already assigned to another course on {self.day} from {self.hours.start_time} to {self.hours.end_time} in a different year")
                    if self.second_course and timetable.course and self.second_course.year != timetable.course.year:
                        if self.week_type == timetable.week_type or self.week_type == 'Any Week' or timetable.week_type == 'Any Week':
                            raise ValidationError(f"Instructor {self.instructor} is already assigned to another course on {self.day} from {self.hours.start_time} to {self.hours.end_time} in a different year")
            if timetable.second_instructor:
                if self.instructor == timetable.second_instructor:
                    if self.course and timetable.second_course and self.course.year != timetable.second_course.year:
                        if self.week_type == timetable.week_type or self.week_type == 'Any Week' or timetable.week_type == 'Any Week':
                            raise ValidationError(f"Instructor {self.instructor} is already assigned to another course on {self.day} from {self.hours.start_time} to {self.hours.end_time} in a different year")
                    if self.second_course and timetable.second_course and self.second_course.year != timetable.second_course.year:
                        if self.week_type == timetable.week_type or self.week_type == 'Any Week' or timetable.week_type == 'Any Week':
                            raise ValidationError(f"Instructor {self.instructor} is already assigned to another course on {self.day} from {self.hours.start_time} to {self.hours.end_time} in a different year")
            if (timetable.course and timetable.course.year):
                if (self.course and self.course.year != timetable.course.year) or (self.second_course and self.second_course.year != timetable.course.year):
                    continue
            elif (timetable.second_course and timetable.second_course.year):
                if (self.course and self.course.year != timetable.second_course.year) or (self.second_course and self.second_course.year != timetable.second_course.year):
                    continue

        # Additional checks for "Different Subgroups"
        if self.class_type == 'Different Subgroups':
            if (self.second_instructor and self.second_instructor == self.instructor) and self.week_type == self.second_week_type and (self.week_type == 'Any Week' or self.second_week_type == 'Any Week'):
                raise ValidationError(f"Instructor {self.instructor} cannot teach both classes at the same time")
            if (self.second_room and self.second_room == self.room) and self.week_type == self.second_week_type and (self.week_type == 'Any Week' or self.second_week_type == 'Any Week'):
                raise ValidationError(f"Room {self.room} cannot be used for both classes at the same time")
        
        # Additional checks for "Dual Class"
        if self.class_type == 'Dual Class':
            if self.week_type == self.second_week_type and (self.week_type == 'Any Week' or self.second_week_type == 'Any Week'):
                raise ValidationError(f"Both classes must be in different weeks")

        super(Timetable, self).save(*args, **kwargs)