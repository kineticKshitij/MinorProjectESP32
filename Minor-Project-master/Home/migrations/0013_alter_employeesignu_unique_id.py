# Generated by Django 5.1.1 on 2024-12-09 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_employeesignu_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignu',
            name='Unique_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
