# Generated by Django 5.0.6 on 2024-06-08 07:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventRecord', '0003_alter_assignment_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assign_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assignment',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]