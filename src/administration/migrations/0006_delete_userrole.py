# Generated by Django 3.1.1 on 2021-03-06 06:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('administration', '0005_userrole'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
