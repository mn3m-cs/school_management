# Generated by Django 3.0 on 2020-08-26 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_teacher_is_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
    ]
