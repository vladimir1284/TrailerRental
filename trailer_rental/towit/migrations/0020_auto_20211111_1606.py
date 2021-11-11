# Generated by Django 3.2.7 on 2021-11-11 22:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0019_auto_20211111_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2021, 11, 11, 16, 6, 5, 33191))),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('line_credit', models.FloatField(blank=True, null=True)),
                ('battery', models.IntegerField()),
                ('powered', models.BooleanField()),
                ('errors', models.IntegerField()),
                ('tracker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_tracker', to='towit.tracker')),
            ],
        ),
        migrations.DeleteModel(
            name='Tracker_data',
        ),
    ]