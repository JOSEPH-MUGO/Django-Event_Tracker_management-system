# Generated by Django 5.0.6 on 2024-05-24 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_employee_employee_id_alter_employee_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='Employee_ID',
        ),
    ]
