# Generated by Django 3.0 on 2020-09-16 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_teacher_classrooms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classrooms',
        ),
    ]