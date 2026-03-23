# Generated migration for updating role field choices to support RBAC

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_set_admin_role_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('admin', 'Administrator'), ('doctor', 'Doctor'), ('receptionist', 'Receptionist')],
                default='receptionist',
                help_text='High-level persona used for role-based access control.',
                max_length=20
            ),
        ),
    ]
