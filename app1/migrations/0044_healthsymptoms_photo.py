# Generated by Django 4.0.5 on 2022-07-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0043_remove_test_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthsymptoms',
            name='photo',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='symptoms', verbose_name='Profile photo'),
        ),
    ]
