# Generated by Django 4.0.5 on 2022-08-16 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_medications_alter_healthsymptoms_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medications',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
