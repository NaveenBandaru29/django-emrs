# Generated by Django 4.0.4 on 2023-03-08 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_user_profile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='gender',
            new_name='music',
        ),
    ]
