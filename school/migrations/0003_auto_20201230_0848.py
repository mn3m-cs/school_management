# Generated by Django 3.0 on 2020-12-30 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='to',
            field=models.CharField(choices=[('1', 'Mothers'), ('2', 'Fathers'), ('3', 'Fathers and Mothers')], max_length=20, verbose_name='To'),
        ),
    ]