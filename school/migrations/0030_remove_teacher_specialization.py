# Generated by Django 3.0 on 2020-08-26 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0029_course_classroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='specialization',
        ),
    ]
