# Generated by Django 4.0.5 on 2022-08-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_healthcheckuppackages_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthpackages',
            name='test_name',
            field=models.ManyToManyField(blank=True, to='app1.test'),
        ),
        migrations.AlterField(
            model_name='healthsymptoms',
            name='test_name',
            field=models.ManyToManyField(blank=True, to='app1.test'),
        ),
    ]
