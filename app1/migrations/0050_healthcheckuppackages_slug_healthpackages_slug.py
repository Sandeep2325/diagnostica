# Generated by Django 4.0.5 on 2022-07-07 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0049_remove_healthcheckuppackages_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcheckuppackages',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='healthpackages',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
