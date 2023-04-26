# Generated by Django 4.0.2 on 2022-03-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0010_auto_20220329_2115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consultancytype',
            old_name='category_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='consultancytype',
            old_name='category_type',
            new_name='profession',
        ),
        migrations.AddField(
            model_name='consultancytype',
            name='expertise',
            field=models.CharField(default='', max_length=250),
        ),
    ]