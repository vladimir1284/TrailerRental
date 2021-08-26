from django.db import models
from datetime import datetime
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class Map(models.Model):
    id = models.AutoField( primary_key=True)
    map_name = models.CharField(max_length=200)
    map_data = models.FileField(upload_to='maps', storage=gd_storage)
    
class Contract(models.Model):
    lessee_name  = models.CharField(max_length=150)
    lessee_address  = models.CharField(max_length=500)
    lessee_mail  = models.CharField(max_length=50)
    vin = models.CharField(max_length=50)
    model = models.CharField(max_length=150)
    year = models.DateField(default=datetime.now().strftime(("%Y")))
    length = models.IntegerField()
    width = models.IntegerField()
    axles = models.IntegerField()
    color = models.CharField(max_length=20)
    location = models.CharField(max_length=500)
    inspection_date = models.DateField()
    current_condition = models.PositiveSmallIntegerField(
        choices=((1,'New'),
                (2,'Like new'),
                (3,'Used')),
        default=1,
    )
    bed_type = models.PositiveSmallIntegerField(
        choices=((1,'Wood'),
                (2,'Steel')),
        default=1,
    )
    bed_comments = models.CharField(max_length=5000)
    current_tires_condition = models.PositiveSmallIntegerField(
        choices=((1,'100%'),
                (2,'75%'),
                (3,'50%')),
        default=1,
    )
    spare_tire = models.PositiveSmallIntegerField(
        choices=((1,'Yes'),
                (3,'No')),
        default=1,
    )
    number_of_ramps = models.IntegerField()
    ramps_material = models.PositiveSmallIntegerField(
        choices=((1,'Aluminium'),
                (2,'Steel')),
        default=1,
    )
    ramps_comments = models.CharField(max_length=5000)
    electrical_instalation = models.CharField(max_length=5000)
    effective_date = models.DateField()
    contract_end_date = models.DateField()
    number_of_payments = models.IntegerField()
    payment_amount = models.IntegerField()
    service_charge = models.IntegerField()
    security_deposit = models.IntegerField()
    accepted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-effective_date',)

