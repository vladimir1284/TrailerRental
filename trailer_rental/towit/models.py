from django.db import models
from datetime import datetime
from gdstorage.storage import GoogleDriveStorage
from django.template.defaultfilters import default
from django.urls import reverse
from django.contrib.auth.models import User

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class UserProfile(models.Model):
    user   = models.OneToOneField(User,
                        on_delete=models.CASCADE,
                        related_name='profile_user')
    avatar = models.ImageField(upload_to='avatars')
    # avatar = models.ImageField(upload_to='towit/avatars', storage=gd_storage)
    def __str__(self):
        return self.user.get_username()

class Owners(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7, blank=True)
    
    def __str__(self):
        return self.name
    
class TrailerType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Interest(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class LeaseStage(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class MaintenanceStatus(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Stage(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Trailer(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(TrailerType,
                            on_delete=models.CASCADE,
                            related_name='trailer_type')
    vin = models.CharField(max_length=50)
    year = models.DateField(default=datetime.now().strftime(("%Y")))
    size = models.IntegerField()
    number_of_axles = models.PositiveSmallIntegerField(
        choices=((1,'2'),
                (2,'3')),
        default=1,
    )
    color = models.ForeignKey(Color,
                            on_delete=models.CASCADE,
                            related_name='trailer_color')
    status = models.ForeignKey(Status,
                            on_delete=models.CASCADE,
                            default = 1,
                            related_name='trailer_status')
    bed_type = models.PositiveSmallIntegerField(
        choices=((1,'Wood'),
                (2,'Steel')),
        default=1,
    )
    bed_comments = models.TextField(blank=True)
    current_tires_condition = models.PositiveSmallIntegerField(
        choices=((1,'100%'),
                (2,'75%'),
                (3,'50%')),
        default=1,
    )
    has_spare_tire = models.PositiveSmallIntegerField(
        choices=((1,'Yes'),
                (2,'No')),
        default=1,
    )
    number_of_ramps = models.IntegerField()
    ramps_material = models.PositiveSmallIntegerField(
        choices=((1,'Aluminium'),
                (2,'Steel')),
        default=1,
    )
    ramps_length = models.PositiveSmallIntegerField(
        choices=((1,'5'),
                (2,'6'),
                (3,'7'),
                (4,'8'),
                (5,'9')),
        default=1,
    )
    electrical_instalation = models.TextField(blank=True)
    price = models.IntegerField()
    tax_price = models.IntegerField()
    owner = models.ForeignKey(Owners,
                            on_delete=models.CASCADE,
                            related_name='trailer_owner')
    Legal_owner = models.ForeignKey(Owners,
                            on_delete=models.CASCADE,
                            related_name='trailer_legal_owner')
    plate = models.CharField(max_length=50)
    plate_stage = models.PositiveSmallIntegerField(
        choices=((1,'Temporary'),
                (2,'Permanent')),
        default=1,
    )
    title = models.ForeignKey(Stage,
                            on_delete=models.CASCADE,
                            related_name='title_stage')
    # title_file = models.FileField(upload_to='titles', blank=True)
    title_file = models.FileField(upload_to='towit/titles', blank=True, 
                                  storage=gd_storage)
    title_note = models.TextField(blank=True)
    sticker = models.ForeignKey(Stage,
                            on_delete=models.CASCADE,
                            related_name='sticker_stage')
    # sticker_file = models.FileField(upload_to='stickers', blank=True)
    sticker_file = models.FileField(upload_to='towit/stickers', blank=True, 
                                    storage=gd_storage)
    sticker_note = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('trailer_detail', kwargs={'id': self.id})
    
    def __str__(self):
        return self.name

class TrailerPicture(models.Model):
    trailer = models.ForeignKey(Trailer,
                            on_delete=models.CASCADE,
                            related_name='trailer_picture')
    # image = models.FileField(upload_to='pictures')
    image = models.FileField(upload_to='towit/pictures', storage=gd_storage)

class Maintenance(models.Model):
    trailer = models.ForeignKey(Trailer,
                            on_delete=models.CASCADE,
                            related_name='trailer_maintenance')
    date =  models.DateField()
    price = models.IntegerField()
    status = models.ForeignKey(MaintenanceStatus,
                            on_delete=models.CASCADE,
                            related_name='maintenance_status')
    comments = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('maintenances', kwargs={'trailer_id': self.trailer.id})
    

class Person(models.Model):
    name = models.CharField(max_length=150)
    address  = models.CharField(max_length=500, blank=True)
    mail  = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    
    
    def __str__(self):
        return self.name
 
class Lessee(Person):    
    insurance_number = models.CharField(max_length=150, blank=True)
    insurance_file = models.FileField(upload_to='towit/insurances', 
                                      storage=gd_storage, blank=True)
    license_number = models.CharField(max_length=150, blank=True)
    license_file = models.FileField(upload_to='towit/licenses', 
                                    storage=gd_storage, blank=True)    
    
    def __str__(self):
        return self.name    
    
    def get_absolute_url(self):
        return reverse('new_contract', kwargs={'lessee_id': self.lessee.id})
 
class Contact(Person): 
    interest = models.ForeignKey(Interest,
                            on_delete=models.CASCADE,
                            related_name='contact_interest')    
    size = models.IntegerField(blank=True)   
    price = models.IntegerField(blank=True)
    term = models.IntegerField()
    term_unit = models.PositiveSmallIntegerField(
        choices=((1,'Weeks'),
                (2,'Months')),
        default=1,
    )
    type = models.ForeignKey(TrailerType, blank=True, 
                            on_delete=models.CASCADE,
                            related_name='contact_type')
    interest_date =  models.DateField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'id': self.id})
 
class Lease(models.Model):
    lessee = models.ForeignKey(Lessee,
                            on_delete=models.CASCADE,
                            related_name='lease')   
    trailer = models.ForeignKey(Trailer,
                            on_delete=models.CASCADE,
                            related_name='lease_trailer')
    stage = models.ForeignKey(LeaseStage,
                            on_delete=models.CASCADE,
                            related_name='lease_stage')      
    location = models.CharField(max_length=500)
    location_file = models.FileField(upload_to='towit/locations', blank=True,
                                     storage=gd_storage)    
    effective_date = models.DateField()
    contract_end_date = models.DateField()
    number_of_payments = models.IntegerField()
    payment_amount = models.IntegerField()
    service_charge = models.IntegerField()
    security_deposit = models.IntegerField()
    inspection_date = models.DateField()
    current_condition = models.PositiveSmallIntegerField(
        choices=((1,'New'),
                (2,'Like new'),
                (3,'Used')),
        default=1,
    )
    
    def __str__(self):
        return self.trailer.name + " -> " + self.lessee.name
    
    class Meta:
        ordering = ('-effective_date',)
    
    def get_absolute_url(self):
        return reverse('contract_detail', kwargs={'id': self.id})
    
    
    
    
    
    
