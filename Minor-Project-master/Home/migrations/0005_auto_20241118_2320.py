from django.db import migrations
from django.contrib.auth.hashers import make_password

def hash_existing_passwords(apps, schema_editor):
    Organization = apps.get_model('Home', 'Organization')
    for organization in Organization.objects.all():
        organization.password = make_password(organization.password)
        organization.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_organization_delete_signup'),
    ]

    operations = [
        migrations.RunPython(hash_existing_passwords),
    ]
