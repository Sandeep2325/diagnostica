# Generated by Django 4.0.5 on 2022-07-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_city_alter_healthcheckuppackages_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='test_nos',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, null=True, verbose_name='user name'),
        ),
    ]
