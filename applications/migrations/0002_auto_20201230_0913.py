# Generated by Django 3.0 on 2020-12-30 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentapplication',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Male'), (1, 'Female')]),
        ),
    ]
