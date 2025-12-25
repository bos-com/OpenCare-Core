# Generated migration for setting admin role for superusers

from django.db import migrations


def _set_admin_role(apps, schema_editor):
    """Set admin role for existing superusers."""
    User = apps.get_model("core", "User")
    User.objects.filter(is_superuser=True).update(role="admin")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_add_role_field"),
    ]

    operations = [
        migrations.RunPython(_set_admin_role, migrations.RunPython.noop),
    ]

