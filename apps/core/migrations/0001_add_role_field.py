# Generated migration for adding role field to User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('admin', 'Administrator'), ('provider', 'Healthcare Provider'), ('patient', 'Patient')],
                default='provider',
                help_text='High-level persona used for role-based access control.',
                max_length=20
            ),
        ),
    ]

