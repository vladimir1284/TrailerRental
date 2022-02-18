from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from ..forms import TrackerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from towit.models import Tracker, TrackerData
from weasyprint.css.computed_values import content
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import pytz
from django.conf import settings
import requests
import json
from requests.auth import HTTPBasicAuth
from ..config import pwd

# Authentication
usr = 'apikey'

"""
Response binary datagram

Config changes pending:

    Ndata | addr1 | low1 | high1 | ... | addrN | lowN | highN
    
No pending configs:

    0
    
Error response:

    error_code > 200
"""

addrs = {'Tcheck': 1,    # the EEPROM address used to store Tcheck
        'MAX_ERRORS': 2, # the EEPROM address used to store MAX_ERRORS
        'Tint': 3,       # the EEPROM address used to store Tint (2 bytes)
        'TintB': 5,      # the EEPROM address used to store TintB (2 bytes)
        'TGPS': 7,       # the EEPROM address used to store TGPS
        'TGPSB': 8,      # the EEPROM address used to store TGPSB
        'SMART': 9,      # the EEPROM address used to store SMART
        'Tsend': 10,     # the EEPROM address used to store Tsend
        'TsendB': 11,    # the EEPROM address used to store TsendB
        'trackerID': 12  # the EEPROM address used to store trackerID (2 bytes)
        }

error_codes ={"Wrong password": 200,
               "Wrong IMEI": 201,
               "Wrong FORMAT": 202,
            }

power_modes ={1: False,
              6: True,
            }

SKEY = "c0ntr453n1a"

class TrackerUpdateView(LoginRequiredMixin,UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'towit/trailer/new_tracker.html' 
    
    def form_valid(self, form):
        resp = {'status':'ok'}
        if(Tracker.objects.get(id=self.kwargs['pk']).Tint !=  form.instance.Tint):
            storeForUpdate('Tint', form.instance.Tint, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).TintB !=  form.instance.TintB):
            storeForUpdate('TintB', form.instance.TintB, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).Tcheck !=  form.instance.Tcheck):
            storeForUpdate('Tcheck', form.instance.Tcheck, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).MAX_ERRORS !=  form.instance.MAX_ERRORS):
            storeForUpdate('MAX_ERRORS', form.instance.MAX_ERRORS, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPS !=  form.instance.TGPS):
            storeForUpdate('TGPS', form.instance.TGPS, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPSB !=  form.instance.TGPSB):
            storeForUpdate('TGPSB', form.instance.TGPSB, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).SMART !=  form.instance.SMART):
            storeForUpdate('SMART', form.instance.SMART, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).Tsend !=  form.instance.Tsend):
            storeForUpdate('Tsend', form.instance.Tsend, resp)
        if(Tracker.objects.get(id=self.kwargs['pk']).TsendB !=  form.instance.TsendB):
            storeForUpdate('TsendB', form.instance.TsendB, resp)
            
        data={
            "deviceid": form.instance.device_id,
            "fromnumber":"+522221111122",
            "body": json.dumps(resp)
            }
        try:
            # Send SMS
            response = requests.post(
            'https://dashboard.hologram.io/api/1/sms/incoming',
            data = data,
            auth = HTTPBasicAuth(usr, pwd)
            )
            # Logs
            print(response.json())    
        except:
            print(data)
            
        return super(TrackerUpdateView, self).form_valid(form)
    
def storeForUpdate(key, value, resp):
    if 'configs' not in resp:
        resp['configs'] = {}
        
    resp['configs'][key] = value
    
    
class TrackerCreateView(LoginRequiredMixin,CreateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'towit/trailer/new_tracker.html' 
    
    def get_initial(self):
        return {'trailer': self.kwargs['trailer_id']}  
    
@login_required
def delete_tracker(request, id):
    try:
        tracker = Tracker.objects.get(id=id)
        trailer_id = tracker.trailer.id
        tracker.delete()
        return redirect('/towit/trailer/%i' % trailer_id)
    except:
        return redirect('/towit/trailers/')
    
def tracker_parameters(request, passwd, tracker_id):
    if (SKEY != passwd):
        payload = bytes([error_codes["Wrong password"]])
        response = HttpResponse(payload)
        return response
    try:
        tracker = Tracker.objects.get(id=tracker_id) 
    except:
        payload = bytes([error_codes["Wrong ID"]])
        response = HttpResponse(payload)
        return response
    # Prepare all data
    storeForUpdate('Tint', tracker.Tint, tracker)
    storeForUpdate('TintB', tracker.TintB, tracker)
    storeForUpdate('Tcheck', tracker.Tcheck, tracker)
    storeForUpdate('MAX_ERRORS', tracker.MAX_ERRORS, tracker)
    storeForUpdate('TGPS', tracker.TGPS, tracker)
    storeForUpdate('TGPSB', tracker.TGPSB, tracker)
    storeForUpdate('SMART', tracker.SMART, tracker)
    storeForUpdate('Tsend', tracker.Tsend, tracker)
    storeForUpdate('TsendB', tracker.TsendB, tracker)
    # Send data
    nData = bytes([int(len(tracker.pendingConfigs)/3)])
    payload = nData + tracker.pendingConfigs
    response = HttpResponse(payload)
    tracker.pendingConfigs = b''
    return response   
    
# Incoming data from a tracker
@csrf_exempt
def tracker_data(request): 
    if request.method == 'POST':
        """
          Parse data from tracker
          msg structure:    
            imei,seq,mode,event,lat,lon,speed,heading,sats,vbat
        """ 
        try:
            msg = request.body.decode()
            print(msg)
        except:
            return HttpResponse("Wrong codification!")
        try:
            data = msg.split(',')
            imei     = int(data[0])            
            seq     = int(data[1])
            mode    = int(data[2])
            event   = int(data[3])
            lat     = float(data[4])
            lon     = float(data[5])
            speed   = int(data[6])
            heading = int(data[7])
            sats    = int(data[8])
            vbat    = int(data[9])/1000. # Volts
            print("IMEI #: %i" % imei)
            print("seq #: %i" % seq)
            print("mode: %i" % mode)
            print("event id: %i" % event)
            print("number of sats: %i" % sats)
            print("vbat: %.3fV" % vbat)
            print("heading: %ideg" % heading)
            print("lat: %.5f" % lat)
            print("lon: %.5f" % lon)
            print("speed: %.2fkm/h" % speed)
        except:
            return HttpResponse("Malformed message!")
        try:
            tracker = Tracker.objects.get(imei=imei)
            td = TrackerData( tracker=tracker,
                            sats = sats,
                            timestamp = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                            latitude = lat,
                            longitude = lon,
                            speed = speed,
                            heading = heading,
                            event_id = event,
                            battery = vbat,
                            sequence = seq,
                            power = power_modes[mode],
                            mode = mode)
            td.save()
        except:
            return HttpResponse("Unknown IMEI %s!" % imei)
            
        return HttpResponse("ok")

# For those trackers that are new or lost their ID
def tracker_id(request, passwd, imei):
    if (SKEY != passwd):
        payload = bytes([error_codes["Wrong password"]])
        response = HttpResponse(payload)
        return response
    try:
        tracker = Tracker.objects.get(imei=imei)
    except:
        # Create a new tracker
        tracker = Tracker(imei=imei)
        tracker.save()
    print(tracker)
    nData = 1
    trackerID_ADDR = 12
    data_low = tracker.id & 0xff
    data_high = (tracker.id >> 8) & 0xff
    payload = bytes([nData, trackerID_ADDR, data_low, data_high])

    response = HttpResponse(payload)
    return response

@login_required
def tracker_detail(request, id):
    tracker = Tracker.objects.get(id=id)
    
    try:
        data = TrackerData.objects.filter(tracker=tracker).order_by("-timestamp")[:10]
    except:
        return render(request, 'towit/tracker/tracker.html', {'tracker': tracker})
    
    return render(request, 'towit/tracker/tracker_data.html', {'tracker': tracker,
                                                               'data': data[0],
                                                               'history': data})
@login_required
def trackers(request):
    trackers = Tracker.objects.all()
    return render(request, 'towit/tracker/trackers.html', {'trackers': trackers})



