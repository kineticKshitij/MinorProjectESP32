# Generated by Django 5.1.6 on 2025-03-02 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0030_alter_employeesignup_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignup',
            name='unique_id',
            field=models.CharField(default='1f19d0611816', editable=False, max_length=12, unique=True),
        ),
    ]
