from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from towit.form.tracker import TrackerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from towit.model.tracker import Tracker, TrackerData
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
              0: True,
            }

SKEY = "c0ntr453n1a"

class TrackerUpdateView(LoginRequiredMixin,UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'towit/trailer/new_tracker.html' 
    
    def form_valid(self, form):
        resp = {}
        if(Tracker.objects.get(id=self.kwargs['pk']).Tint !=  form.instance.Tint):
            resp['Tint'] = form.instance.Tint
        if(Tracker.objects.get(id=self.kwargs['pk']).TintB !=  form.instance.TintB):            
            resp['TintB'] = form.instance.TintB
        if(Tracker.objects.get(id=self.kwargs['pk']).MAX_ERRORS !=  form.instance.MAX_ERRORS):
            resp['MAX_ERRORS'] = form.instance.MAX_ERRORS
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPS !=  form.instance.TGPS):            
            resp['TGPS'] = form.instance.TGPS
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPSB !=  form.instance.TGPSB):
            resp['TGPSB'] = form.instance.TGPSB
        if(Tracker.objects.get(id=self.kwargs['pk']).SMART !=  form.instance.SMART):
            resp['SMART'] = form.instance.SMART
        if(Tracker.objects.get(id=self.kwargs['pk']).Tsend !=  form.instance.Tsend):
            resp['Tsend'] = form.instance.Tsend
        if(Tracker.objects.get(id=self.kwargs['pk']).TsendB !=  form.instance.TsendB):
            resp['TsendB'] = form.instance.TsendB
        
        # Send sms when we detect changes in parameters 
        if(len(resp) > 0):    
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
            
        # Update Traccar URL
        trackers = Tracker.objects.all()
        for tracker in trackers:
            tracker.traccar_url = form.instance.traccar_url
            tracker.save()

        return super(TrackerUpdateView, self).form_valid(form)
    
    
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
            print(tracker)
        except:
            return HttpResponse("Unknown IMEI %s!" % imei)
            
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
        if tracker.feed_traccar:
            sendOsmAnd(tracker, td)
        td.save()
            
        return HttpResponse("ok")

@login_required
def tracker_export(request, id):
    tracker = Tracker.objects.get(id=id)
    data = TrackerData.objects.filter(tracker=tracker)
    for td in data:
        sendOsmAnd(tracker, td)
        
    return render(request, 'towit/tracker/export_ok.html', {'tracker': tracker})

def sendOsmAnd(tracker, td):
    req_str = '{}?id={}&lat={}&lon={}&speed={}&batt={}&timestamp={}&heading={}'.format(
                    tracker.traccar_url,
                    tracker.imei, 
                    td.latitude, 
                    td.longitude, 
                    td.speed/1.852, # Km/h to Nuts
                    int(123-123/(1+(td.battery/3.7)**80)**0.165), 
		            int(td.timestamp.timestamp()), 
                    td.heading)
    print(req_str)

    r = requests.get(req_str)
    if r.status_code != 200:
        print('Status code != 200!')

@login_required
def tracker_detail(request, id):
    tracker = Tracker.objects.get(id=id)
    
    try:
        data = TrackerData.objects.filter(tracker=tracker).order_by("-timestamp")[:30]

        if (data[0].mode == 0): # Powered
            max_elapsed_time = 80*tracker.Tint
        else:
            max_elapsed_time = 80*tracker.TintB

        elapsed_time = (datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)) - data[0].timestamp).total_seconds()

        print("elapsed_time: %is" % elapsed_time)
        print("max_elapsed_time: %is" % max_elapsed_time)

        online = elapsed_time < max_elapsed_time
    except Exception as err:
        raise err 
    
    return render(request, 'towit/tracker/tracker_data.html', {'tracker': tracker,
                                                               'data': data[0],
                                                               'online': online,
                                                               'history': data})
@login_required
def trackers(request):
    trackers = Tracker.objects.all()
    return render(request, 'towit/tracker/trackers.html', {'trackers': trackers})



