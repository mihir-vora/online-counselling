# Generated by Django 3.2.3 on 2022-03-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0009_auto_20210326_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultant',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='consultant',
            name='long',
        ),
        migrations.AddField(
            model_name='consultant',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
