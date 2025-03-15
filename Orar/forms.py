from django import forms
from .models import Timetable

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['second_course'].required = False
        self.fields['second_course_type'].required = False
        self.fields['second_instructor'].required = False
        self.fields['second_room'].required = False
        self.fields['second_week_type'].required = False