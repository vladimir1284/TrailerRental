# Generated by Django 3.2.6 on 2021-08-25 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0004_auto_20210825_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trailer_status', to='towit.status'),
        ),
    ]
