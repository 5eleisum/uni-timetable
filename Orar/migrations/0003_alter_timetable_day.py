# Generated by Django 5.0.6 on 2024-07-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orar', '0002_daytype_hours_remove_timetable_timeslot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='day',
            field=models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=9),
        ),
    ]
