# Generated by Django 5.1.6 on 2025-02-28 13:45

import Home.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0028_delete_signuprequest_employeesignup_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignup',
            name='unique_id',
            field=models.CharField(default='0da5c70178bd', editable=False, max_length=12, unique=True),
        ),
        migrations.CreateModel(
            name='OrganizationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=Home.models.generate_uuid, max_length=40, unique=True)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='Home.organization')),
            ],
        ),
    ]
