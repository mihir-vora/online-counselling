# Generated by Django 4.0.2 on 2022-03-31 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0012_consultant_expertise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultant',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='consultant',
            name='last_name',
        ),
    ]
