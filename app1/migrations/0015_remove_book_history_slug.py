# Generated by Django 4.0.5 on 2022-07-04 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_book_history_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book_history',
            name='slug',
        ),
    ]
