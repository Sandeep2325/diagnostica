# Generated by Django 4.0.5 on 2022-07-06 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_test_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthpackages',
            name='discount',
        ),
    ]
