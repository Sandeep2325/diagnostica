# Generated by Django 4.0.5 on 2022-07-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_alter_category_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityname', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'City',
            },
        ),
        migrations.AlterModelOptions(
            name='healthcheckuppackages',
            options={'verbose_name_plural': 'Lab Tests'},
        ),
    ]
