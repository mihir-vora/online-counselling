# Generated by Django 3.1.1 on 2021-03-26 06:50

import consultant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0005_consultant_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='date_of_birth',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='phone_no',
            field=models.CharField(default=9999999999, max_length=10, validators=[consultant.models.phone_validator]),
        ),
    ]