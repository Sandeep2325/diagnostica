# Generated by Django 4.0.5 on 2022-08-16 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_alter_healthcheckuppackages_dbanglore_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='medications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medic', models.TextField(blank=True, null=True)),
                ('morning', models.BooleanField(default=True)),
                ('afternoon', models.BooleanField(default=True)),
                ('evening', models.BooleanField(default=True)),
                ('night', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'User Medications',
            },
        ),
        migrations.AlterModelOptions(
            name='healthsymptoms',
            options={'verbose_name_plural': 'Life Style Assesments'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name_plural': 'Subscriptions'},
        ),
    ]
