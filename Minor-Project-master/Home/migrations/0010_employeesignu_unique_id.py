# Generated by Django 5.1.1 on 2024-12-09 10:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_employeesignu'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesignu',
            name='Unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
