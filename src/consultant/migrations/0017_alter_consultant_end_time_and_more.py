# Generated by Django 4.0.2 on 2022-04-04 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0016_remove_consultant_timming_consultant_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='end_time',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='start_time',
            field=models.CharField(max_length=255),
        ),
    ]
