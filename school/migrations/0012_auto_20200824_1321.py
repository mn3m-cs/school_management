# Generated by Django 3.0 on 2020-08-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_teacher_achievements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='achievements',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]