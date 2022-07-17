# Generated by Django 4.0.5 on 2022-07-17 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_healthcheckuppackages_dpricel5_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='city_icon',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='dpricel5',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='dpricel6',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='dpricel7',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='pricel5',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='pricel6',
        ),
        migrations.RemoveField(
            model_name='healthcheckuppackages',
            name='pricel7',
        ),
        migrations.RemoveField(
            model_name='healthpackages',
            name='pricel7',
        ),
        migrations.RemoveField(
            model_name='test',
            name='pricel7',
        ),
        migrations.AlterField(
            model_name='healthcheckuppackages',
            name='dpricel2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chennai Discounted Price'),
        ),
        migrations.AlterField(
            model_name='healthcheckuppackages',
            name='dpricel4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Delhi Discounted Price'),
        ),
        migrations.AlterField(
            model_name='healthcheckuppackages',
            name='pricel2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chennai Price'),
        ),
        migrations.AlterField(
            model_name='healthcheckuppackages',
            name='pricel3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mumbai Price'),
        ),
        migrations.AlterField(
            model_name='healthcheckuppackages',
            name='pricel4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Delhi Price'),
        ),
        migrations.AlterField(
            model_name='healthpackages',
            name='pricel3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chennai Price'),
        ),
        migrations.AlterField(
            model_name='healthpackages',
            name='pricel4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Hyderabad Price'),
        ),
        migrations.AlterField(
            model_name='healthpackages',
            name='pricel5',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Delhi Price'),
        ),
        migrations.AlterField(
            model_name='healthpackages',
            name='pricel6',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Kolkata Price'),
        ),
        migrations.AlterField(
            model_name='test',
            name='pricel3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Chennai Price'),
        ),
        migrations.AlterField(
            model_name='test',
            name='pricel4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Hyderabad Price'),
        ),
        migrations.AlterField(
            model_name='test',
            name='pricel5',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Delhi Price'),
        ),
        migrations.AlterField(
            model_name='test',
            name='pricel6',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Kolkata Price'),
        ),
    ]
