# Generated by Django 3.2.6 on 2021-08-29 16:08

from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('towit', '0009_auto_20210828_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LeaseStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('mail', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lessee',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='towit.person')),
                ('insurance_number', models.CharField(max_length=150)),
                ('insurance_file', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/insurances')),
                ('license_number', models.CharField(max_length=150)),
                ('license_file', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/licenses')),
            ],
            bases=('towit.person',),
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=500)),
                ('location_file', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='towit/locations')),
                ('effective_date', models.DateField()),
                ('contract_end_date', models.DateField()),
                ('number_of_payments', models.IntegerField()),
                ('payment_amount', models.IntegerField()),
                ('service_charge', models.IntegerField()),
                ('security_deposit', models.IntegerField()),
                ('inspection_date', models.DateField()),
                ('current_condition', models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'Like new'), (3, 'Used')], default=1)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lease_stage', to='towit.leasestage')),
                ('trailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lease_trailer', to='towit.trailer')),
                ('lessee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lease', to='towit.lessee')),
            ],
            options={
                'ordering': ('-effective_date',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='towit.person')),
                ('size', models.IntegerField(blank=True)),
                ('price', models.IntegerField(blank=True)),
                ('term', models.DurationField()),
                ('interest_date', models.DateField()),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_interest', to='towit.interest')),
                ('type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_type', to='towit.trailertype')),
            ],
            bases=('towit.person',),
        ),
    ]
