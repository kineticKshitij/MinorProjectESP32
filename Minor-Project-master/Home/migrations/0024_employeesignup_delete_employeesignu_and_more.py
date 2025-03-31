# Generated by Django 5.1.6 on 2025-02-24 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0023_auto_20241221_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('unique_id', models.CharField(blank=True, max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='employees_photos/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='EmployeeSignu',
        ),
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='query',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='signuprequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
