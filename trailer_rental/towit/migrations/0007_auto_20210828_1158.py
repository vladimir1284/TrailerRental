# Generated by Django 3.2.6 on 2021-08-28 11:58

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailer',
            name='sticker_file',
            field=models.FileField(blank=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/stickers'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='title_file',
            field=models.FileField(blank=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/titles'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/avatars'),
        ),
    ]