# Generated by Django 3.0 on 2020-08-24 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_student_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='level',
        ),
    ]
