# Generated by Django 4.0.5 on 2022-09-06 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_invoicee_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Subscriptions', 'verbose_name_plural': 'Subscriptions'},
        ),
    ]