# Generated by Django 5.0.6 on 2024-06-11 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventRecord', '0005_assignment_updated_at'),
        ('employee', '0002_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='assignment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='EventRecord.assignment'),
        ),
        migrations.AlterField(
            model_name='report',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]
