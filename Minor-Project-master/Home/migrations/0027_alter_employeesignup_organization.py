# Generated by Django 5.1.6 on 2025-02-28 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0026_remove_employeesignup_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignup',
            name='organization',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='Home.organization'),
            preserve_default=False,
        ),
    ]
