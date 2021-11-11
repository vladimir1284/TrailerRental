# Generated by Django 3.2.7 on 2021-11-11 20:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0018_auto_20210910_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='trailer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracker_trailer', to='towit.trailer'),
        ),
        migrations.CreateModel(
            name='Tracker_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2021, 11, 11, 14, 24, 9, 425723))),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('line_credit', models.FloatField(blank=True, null=True)),
                ('battery', models.IntegerField()),
                ('powered', models.BooleanField()),
                ('errors', models.IntegerField()),
                ('tracker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_tracker', to='towit.tracker')),
            ],
        ),
    ]
