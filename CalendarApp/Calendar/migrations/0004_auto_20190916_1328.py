# Generated by Django 2.2.5 on 2019-09-16 20:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0003_auto_20190915_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='endDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='summary',
            name='startDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]