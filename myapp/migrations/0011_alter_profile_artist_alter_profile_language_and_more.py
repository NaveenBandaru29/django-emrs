# Generated by Django 4.0.4 on 2023-03-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_rename_music_profile_musician'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='artist',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='musician',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
