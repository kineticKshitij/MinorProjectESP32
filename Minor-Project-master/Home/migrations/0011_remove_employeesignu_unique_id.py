# Generated by Django 5.1.1 on 2024-12-09 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_employeesignu_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeesignu',
            name='Unique_id',
        ),
    ]
