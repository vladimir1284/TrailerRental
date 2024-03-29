from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import User


class Tracker(models.Model):
    owner = models.ForeignKey(User,
                              default=None,
                              null=True,
                              blank=True,
                              on_delete=models.SET_DEFAULT,
                              related_name='tracker_owner')
    last_update = models.DateTimeField(blank=True, null=True)
    imei = models.IntegerField()
    device_password = models.CharField(max_length=15, default="123456")
    device_id = models.IntegerField(blank=True)
    phone_password = models.CharField(max_length=15, blank=True)
    traccar_url = models.CharField(max_length=500, blank=True)
    feed_traccar = models.BooleanField(default=False)
    # Configuration parameters
    pendingConfigs = models.BinaryField(default=b'')
    Tcheck = models.IntegerField(default=15)

    class Modes(models.IntegerChoices):
        Keepalived = 0
        Tracking = 1
    Mode = models.IntegerField(choices=Modes.choices, default=0)
    Tint = models.IntegerField(default=60)
    TintB = models.IntegerField(default=360)
    TGPS = models.IntegerField(default=10)
    TGPSB = models.IntegerField(default=5)
    SMART = models.BooleanField(default=False)
    Tsend = models.IntegerField(default=5)
    TsendB = models.IntegerField(default=3)
    # Tracker and lessee Data
    trailer_description = models.CharField(max_length=100, default="")
    trailer_bin_number = models.CharField(max_length=50, default="")
    lessee_name = models.CharField(max_length=50, default="")

    def get_absolute_url(self):
        return reverse('tracker_detail', kwargs={'id': self.id})


class TrackerData(models.Model):
    tracker = models.ForeignKey(Tracker,
                                on_delete=models.CASCADE,
                                related_name='data_tracker')
    sats = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.IntegerField(blank=True, null=True)
    battery = models.FloatField(blank=True, null=True)
    power = models.BooleanField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)


class TrackerUpload(models.Model):
    tracker = models.ForeignKey(Tracker,
                                on_delete=models.CASCADE,
                                related_name='data_upload')
    timestamp = models.DateTimeField(default=datetime.now)
    sequence = models.IntegerField(blank=True, null=True)
    charging = models.BooleanField(blank=True, null=True)
    battery = models.FloatField(blank=True, null=True)
    wur = models.IntegerField(blank=True, null=True)
    wdgc = models.IntegerField(blank=True, null=True)
    SOURCES = [
        ('LTE', 'Radio base'),
        ('GPS', 'GPS data'),
    ]
    source = models.CharField(
        max_length=3,
        choices=SOURCES,
        default='LTE',
    )
    # GPS
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    precision = models.FloatField(blank=True, null=True)
    # LTE
    mcc = models.IntegerField(blank=True, null=True)
    mnc = models.IntegerField(blank=True, null=True)
    lac = models.IntegerField(blank=True, null=True)
    cellid = models.IntegerField(blank=True, null=True)


class TrackerDebugData(models.Model):
    tracker = models.ForeignKey(Tracker,
                                on_delete=models.CASCADE,
                                related_name='debug_tracker')
    timestamp = models.DateTimeField(default=datetime.now)
    battery = models.FloatField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)


class TrackerDebugGPS(models.Model):
    tdd = models.OneToOneField(TrackerDebugData,
                               on_delete=models.CASCADE,
                               primary_key=True)
    sats = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.IntegerField(blank=True, null=True)
    gps_delay = models.IntegerField(blank=True, null=True)
    lte_delay = models.IntegerField(blank=True, null=True)


class TrackerDebugStartup(models.Model):
    tdd = models.OneToOneField(TrackerDebugData,
                               on_delete=models.CASCADE,
                               primary_key=True)
    wake_reason = models.IntegerField(blank=True, null=True)
    reset_cause = models.IntegerField(blank=True, null=True)
    lte_delay = models.IntegerField(blank=True, null=True)


class TrackerDebugError(models.Model):
    tdd = models.OneToOneField(TrackerDebugData,
                               on_delete=models.CASCADE,
                               primary_key=True)
    gps_delay = models.IntegerField(blank=True, null=True)
    lte_delay = models.IntegerField(blank=True, null=True)
