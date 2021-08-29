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
    # avatar = models.ImageField(upload_to='avatars')
    avatar = models.ImageField(upload_to='towit/avatars', storage=gd_storage)
    def __str__(self):
        return self.user.get_username()

class Owners(models.Model):
    name = models.CharField(max_length=50)
    
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
    model = models.CharField(max_length=150)
    year = models.DateField(default=datetime.now().strftime(("%Y")))
    length = models.IntegerField()
    width = models.IntegerField()
    number_of_axles = models.IntegerField()
    color = models.CharField(max_length=20)
    status = models.ForeignKey(Status,
                            on_delete=models.CASCADE,
                            default = 1,
                            related_name='trailer_status')
    location = models.TextField()
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
                (3,'No')),
        default=1,
    )
    number_of_ramps = models.IntegerField()
    ramps_material = models.PositiveSmallIntegerField(
        choices=((1,'Aluminium'),
                (2,'Steel')),
        default=1,
    )
    ramps_comments = models.TextField(blank=True)
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
    title_file = models.FileField(upload_to='towit/titles', blank=True, storage=gd_storage)
    title_note = models.TextField(blank=True)
    sticker = models.ForeignKey(Stage,
                            on_delete=models.CASCADE,
                            related_name='sticker_stage')
    # sticker_file = models.FileField(upload_to='stickers', blank=True)
    sticker_file = models.FileField(upload_to='towit/stickers', blank=True, storage=gd_storage)
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
    
   
    
    
    
    
    
    
    
    
