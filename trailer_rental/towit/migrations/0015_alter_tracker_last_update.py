# Generated by Django 3.2.7 on 2021-09-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0014_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
