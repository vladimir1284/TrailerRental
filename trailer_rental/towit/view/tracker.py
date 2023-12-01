from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
import pytz
from towit.form.tracker import TrackerForm, TrackerLesseeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from towit.model.tracker import (
    Tracker,
    TrackerData,
    TrackerDebugData,
    TrackerDebugError,
    TrackerDebugGPS,
    TrackerDebugStartup,
    TrackerUpload)
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from django.http import JsonResponse
import json
from requests.auth import HTTPBasicAuth
from ..config import pwd

from .bat_percent import vbat2percent


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
         'Mode': 2,  # the EEPROM address used to store Mode
         'Tint': 3,       # the EEPROM address used to store Tint (2 bytes)
         'TintB': 5,      # the EEPROM address used to store TintB (2 bytes)
         'TGPS': 7,       # the EEPROM address used to store TGPS
         'TGPSB': 8,      # the EEPROM address used to store TGPSB
         'SMART': 9,      # the EEPROM address used to store SMART
         'Tsend': 10,     # the EEPROM address used to store Tsend
         'TsendB': 11,    # the EEPROM address used to store TsendB
         # the EEPROM address used to store trackerID (2 bytes)
         'trackerID': 12
         }

error_codes = {"Wrong password": 200,
               "Wrong IMEI": 201,
               "Wrong FORMAT": 202,
               }

power_modes = {1: False,
               0: True,
               }

SKEY = "c0ntr453n1a"


class TrackerUpdateView(LoginRequiredMixin, UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'towit/trailer/new_tracker.html'

    def form_valid(self, form):
        resp = {}
        if (Tracker.objects.get(id=self.kwargs['pk']).Tint != form.instance.Tint):
            resp['Tint'] = form.instance.Tint
        if (Tracker.objects.get(id=self.kwargs['pk']).TintB != form.instance.TintB):
            resp['TintB'] = form.instance.TintB
        if (Tracker.objects.get(id=self.kwargs['pk']).Mode != form.instance.Mode):
            resp['Mode'] = form.instance.Mode
        if (Tracker.objects.get(id=self.kwargs['pk']).TGPS != form.instance.TGPS):
            resp['TGPS'] = form.instance.TGPS
        if (Tracker.objects.get(id=self.kwargs['pk']).TGPSB != form.instance.TGPSB):
            resp['TGPSB'] = form.instance.TGPSB
        if (Tracker.objects.get(id=self.kwargs['pk']).SMART != form.instance.SMART):
            resp['SMART'] = form.instance.SMART
        if (Tracker.objects.get(id=self.kwargs['pk']).Tsend != form.instance.Tsend):
            resp['Tsend'] = form.instance.Tsend
        if (Tracker.objects.get(id=self.kwargs['pk']).TsendB != form.instance.TsendB):
            resp['TsendB'] = form.instance.TsendB

        # Send sms when we detect changes in parameters
        if (len(resp) > 0):
            data = {
                "deviceid": form.instance.device_id,
                "fromnumber": "+522221111122",
                "body": json.dumps(resp)
            }
            try:
                # Send SMS
                response = requests.post(
                    'https://dashboard.hologram.io/api/1/sms/incoming',
                    data=data,
                    auth=HTTPBasicAuth(usr, pwd)
                )
                # Logs
                print(response.json())
            except:
                print(data)

        # # Update Traccar URL
        # trackers = Tracker.objects.all()
        # for tracker in trackers:
        #     tracker.traccar_url = form.instance.traccar_url
        #     tracker.save()

        return super(TrackerUpdateView, self).form_valid(form)


class TrackerCreateView(LoginRequiredMixin, CreateView):
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
def get_tracker_data(request, id):
    try:
        tracker_data = TrackerData.objects.filter(id__gt=int(id)).order_by("-id")[:600]
    except TrackerData.DoesNotExist:
        return JsonResponse({'error': 'Tracker data not found.'}, status=404)
    
    tracker_data = json.loads(serializers.serialize('json',tracker_data))
    return JsonResponse(tracker_data,safe=False)

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
            imei = int(data[0])
            seq = int(data[1])
            mode = int(data[2])
            event = int(data[3])
            lat = float(data[4])
            lon = float(data[5])
            speed = int(data[6])
            heading = int(data[7])
            sats = int(data[8])
            vbat = int(data[9])/1000.  # Volts
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

        td = TrackerData(tracker=tracker,
                         sats=sats,
                         timestamp=datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                         latitude=lat,
                         longitude=lon,
                         speed=speed,
                         heading=heading,
                         event_id=event,
                         battery=vbat,
                         sequence=seq,
                         power=power_modes[mode],
                         mode=mode)
        td.save()
        # Forward to towit page
        charging = mode
        wur = 0  # WakeUp reason
        wdgc = 0  # Watchdog resets count
        source = "GPS"  # LTE or GPS
        precision = 20

        msg = f"{imei},{seq},{charging},{int(vbat*1000)},{wur},{wdgc},{source},{lat},{lon},{speed},{precision}"
        # requests.post("http://towithouston.com/erp/rent/tracker-upload", data=msg)

        return HttpResponse("ok")

# Incoming debug data from a tracker


@csrf_exempt
def tracker_debug(request):
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
            msg_type = data[0]
            imei = int(data[1])
            seq = int(data[2])
            mode = int(data[3])
            vbat = int(data[4])/1000.  # Volts

            print("IMEI #: %i" % imei)
            print("seq #: %i" % seq)
            print("mode: %i" % mode)
            print("vbat: %.3fV" % vbat)

        except:
            return HttpResponse("Malformed message!")
        try:
            tracker = Tracker.objects.get(imei=imei)
            print(tracker)
        except:
            return HttpResponse("Unknown IMEI %s!" % imei)

        tdd = TrackerDebugData(tracker=tracker,
                               timestamp=datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                               battery=vbat,
                               sequence=seq,
                               mode=mode)
        tdd.save()

        if msg_type == "gps":
            event = int(data[5])
            lat = float(data[6])
            lon = float(data[7])
            speed = int(data[8])
            heading = int(data[9])
            sats = int(data[10])
            gps_delay = int(data[11])
            lte_delay = int(data[12])
            print("event id: %i" % event)
            print("number of sats: %i" % sats)
            print("heading: %ideg" % heading)
            print("lat: %.5f" % lat)
            print("lon: %.5f" % lon)
            print("speed: %.2fkm/h" % speed)
            print("GPS delay: %is" % gps_delay)
            print("LTE delay: %is" % lte_delay)

            tdg = TrackerDebugGPS(
                tdd=tdd,
                sats=sats,
                latitude=lat,
                longitude=lon,
                speed=speed,
                heading=heading,
                #event_id = event,
                gps_delay=gps_delay,
                lte_delay=lte_delay
            )
            tdg.save()

        if msg_type == "error":
            gps_delay = int(data[5])
            lte_delay = int(data[6])
            print("GPS delay: %is" % gps_delay)
            print("LTE delay: %is" % lte_delay)

            tde = TrackerDebugError(
                tdd=tdd,
                gps_delay=gps_delay,
                lte_delay=lte_delay
            )
            tde.save()

        if msg_type == "wake":
            lte_delay = int(data[5])
            wake_reason = int(data[6])
            reset_cause = int(data[7])
            print("LTE delay: %is" % lte_delay)
            print("Wake reason: %i" % wake_reason)
            print("Reset cause: %i" % reset_cause)

            tds = TrackerDebugStartup(
                tdd=tdd,
                wake_reason=wake_reason,
                reset_cause=reset_cause,
                lte_delay=lte_delay
            )
            tds.save()

        return HttpResponse("ok")

# use custom response class to override HttpResponse.close()


class SendOsmAndAfterResponse(HttpResponse):

    def __init__(self, tracker, td, content=b'',  *args, **kwargs):
        super().__init__(content=content, *args, **kwargs)
        self._tracker = tracker
        self._td = td

    def close(self):
        super(SendOsmAndAfterResponse, self).close()
        # do whatever you want, this is the last codepoint in request handling
        if self._tracker.feed_traccar:
            sendOsmAnd(self._tracker, self._td)


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
        td.speed/1.852,  # Km/h to Nuts
        int(123-123/(1+(td.battery/3.7)**80)**0.165),
        int(td.timestamp.timestamp()),
        td.heading)
    print(req_str)

    try:
        r = requests.get(req_str)
        if r.status_code != 200:
            print('Status code != 200!')
    except Exception as err:
        print(err)


@login_required
def tracker_detail(request, id):
    tracker = Tracker.objects.get(id=id)
    if request.method == 'POST':
        form = TrackerLesseeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            tracker.lessee_name = form.cleaned_data['lessee_name']
            tracker.save()
    data_v1 = TrackerUpload.objects.filter(
        tracker=tracker).order_by("-timestamp")
    if data_v1:
        return render(request, 'towit/tracker/tracker_upload.html', getTrackerUpload(id, 30))

    return render(request, 'towit/tracker/tracker_data.html', getTrackerDetails(id, 30))


""" def getTrackerUpload(tracker, data: List[TrackerUpload]):
    for item in data:
        if item.latitude is None:
            url = "http://opencellid.org/cell/get?key=pk.5b6bc57dbacf5078433585d1ddba0fa6&mcc={}&mnc={}&lac={}&cellid={}&format=json".format(
                item.mcc,
                item.mnc,
                item.lac,
                item.cellid
            )
            response = requests.get(url)
            if response.status_code == 200:
                print("Location data downloaded for Tracker {} at {}".format(
                    tracker.id, item.timestamp))
                json_data = response.json()
                item.latitude = json_data['lat']
                item.longitude = json_data['lon']
                item.speed = 0
                item.save()

    return {'tracker': tracker,
            'data': data[0],
            'online': True,
            'history': data}
 """


@login_required
def tracker_detail_n(request, id, n):
    return render(request, 'towit/tracker/tracker_data.html', getTrackerDetails(id, n))


def getTrackerUpload(id, n):
    tracker = Tracker.objects.get(id=id)

    try:
        data = TrackerUpload.objects.filter(
            tracker=tracker).order_by("-timestamp")[:n]

        for i, item in enumerate(data):
            data[i].battery = vbat2percent(item.battery)

        if (data[0].charging):  # Powered
            max_elapsed_time = 4800
        else:
            max_elapsed_time = 80*tracker.Tint

        elapsed_time = (datetime.now().replace(tzinfo=pytz.timezone(
            settings.TIME_ZONE)) - data[0].timestamp).total_seconds()

        print("elapsed_time: %is" % elapsed_time)
        print("max_elapsed_time: %is" % max_elapsed_time)

        online = elapsed_time < max_elapsed_time
    except Exception as err:
        raise err
    return {'tracker': tracker,
            'data': data[0],
            'online': online,
            'history': data}


def getTrackerDetails(id, n):
    tracker = Tracker.objects.get(id=id)

    try:
        data = TrackerData.objects.filter(
            tracker=tracker).order_by("-timestamp")[:n]

        for i, item in enumerate(data):
            data[i].battery = vbat2percent(item.battery)

        if (data[0].mode == 0):  # Powered
            max_elapsed_time = 80*tracker.Tint
        else:
            max_elapsed_time = 80*tracker.TintB

        elapsed_time = (datetime.now().replace(tzinfo=pytz.timezone(
            settings.TIME_ZONE)) - data[0].timestamp).total_seconds()

        print("elapsed_time: %is" % elapsed_time)
        print("max_elapsed_time: %is" % max_elapsed_time)

        online = elapsed_time < max_elapsed_time
    except Exception as err:
        raise err
    return {'tracker': tracker,
            'data': data[0],
            'online': online,
            'history': data}


@login_required
def debug_detail(request, id):
    tracker = Tracker.objects.get(id=id)

    try:
        data = TrackerDebugData.objects.filter(
            tracker=tracker).order_by("-timestamp")[:50]

    except Exception as err:
        raise err

    return render(request, 'towit/tracker/debug_data.html', {'tracker': tracker,
                                                             'data': data})


@login_required
def trackers_data(request):
    trackers = Tracker.objects.all()
    data = []
    for tracker in trackers:
        try:
            td = TrackerData.objects.filter(
                tracker=tracker).order_by("-timestamp")[0]
            if (td.mode == 0):  # Powered
                max_elapsed_time = 80*tracker.Tint
            else:
                max_elapsed_time = 80*tracker.TintB

            elapsed_time = (datetime.now().replace(tzinfo=pytz.timezone(
                settings.TIME_ZONE)) - td.timestamp).total_seconds()

            print("elapsed_time: %is" % elapsed_time)
            print("max_elapsed_time: %is" % max_elapsed_time)

            online = elapsed_time < max_elapsed_time

            data.append({
                'tracker': td.tracker.id,
                'timestamp': td.timestamp,
                'latitude': td.latitude,
                'longitude': td.longitude,
                'speed': td.speed,
                'heading': td.heading,
                'battery': vbat2percent(td.battery),
                'mode': td.mode,
                'power': td.power,
                'online': online
            })

        except Exception as err:
            print(err)
    return JsonResponse({'data': data})


@login_required
def trackers(request):
    trackers = Tracker.objects.all()
    return render(request, 'towit/tracker/trackers.html', {'trackers': trackers})


@login_required
def trackers_table(request):
    trcks = Tracker.objects.all()
    trackers = []
    for tracker in trcks:
        try:
            # V1.0
            data_v1 = TrackerUpload.objects.filter(
                tracker=tracker).order_by("-timestamp")
            if data_v1:
                td = data_v1[0]
                td.mode = {True: 0, False: 1}[td.charging]
                if (td.charging):  # Powered
                    max_elapsed_time = 4800
                else:
                    max_elapsed_time = 80*tracker.Tint
            else:
                # V0.1
                td = TrackerData.objects.filter(
                    tracker=tracker).order_by("-timestamp")[0]
                if (td.mode == 0):  # Powered
                    max_elapsed_time = 80*tracker.Tint
                else:
                    max_elapsed_time = 80*tracker.TintB

            elapsed_time = (datetime.now().replace(tzinfo=pytz.timezone(
                settings.TIME_ZONE)) - td.timestamp).total_seconds()

            print("elapsed_time: %is" % elapsed_time)
            print("max_elapsed_time: %is" % max_elapsed_time)

            online = elapsed_time < max_elapsed_time

            trackers.append({
                'id': td.tracker.id,
                'updated': td.timestamp,
                'bat': int(vbat2percent(td.battery)*100)/100.,
                'mode': td.mode,
                'online': online,
                'lessee_name': td.tracker.lessee_name,
                'trailer_description': td.tracker.trailer_description,
            })

        except Exception as err:
            print(err)
    return render(request, 'towit/tracker/trackers_table.html', {'trackers': trackers})


@csrf_exempt
def get_tracker_upload(request, id):
    try:
        tracker_upload = TrackerUpload.objects.filter(id__gt=int(id)).order_by("-id")[:600]
    except TrackerUpload.DoesNotExist:
        return JsonResponse({'error': 'Tracker data not found.'}, status=404)
    
    tracker_upload = json.loads(serializers.serialize('json',tracker_upload))
    return JsonResponse(tracker_upload,safe=False)

@csrf_exempt
def tracker_upload(request):
    # Incoming data from a tracker v1.0
    if request.method == 'POST':
        """
          Parse data from tracker
          msg structure:    
            imei,seq,mode,event,lat,lon,speed,heading,sats,vbat
        """
        try:
            msg = request.body.decode()
            print(msg)
            # Make a post request to a remote url using the same payload
            # requests.post("http://towithouston.com/erp/rent/tracker-upload", data=msg)
        except:
            return HttpResponse("Wrong codification!")
        try:
            data = msg.split(',')

            imei = int(data[0])
            try:
                tracker = Tracker.objects.get(imei=imei)
                print(tracker)
            except:
                return HttpResponse("Unknown IMEI %s!" % imei)

            seq = int(data[1])
            charging = bool(int(data[2]))
            vbat = int(data[3])/1000.  # Volts
            wur = int(data[4])  # WakeUp reason
            wdgc = int(data[5])  # Watchdog resets count
            source = data[6]  # LTE or GPS
            print("IMEI #: %i" % imei)
            print("seq #: %i" % seq)
            print("Charging: %r" % charging)
            print("WakeUp reason: %i" % wur)
            print("Watchdog resets count: %i" % wdgc)
            print("vbat: %.3fV" % vbat)
            print("Datasource: %s" % source)

            if source == 'LTE':
                # 310-410,0x712A,137002000
                # mcc-mnc,lac,cellid
                mcc_mnc = data[7].split('-')
                mcc = int(mcc_mnc[0])
                mnc = int(mcc_mnc[1])
                lac = int(data[8], 16)
                cellid = int(data[9])
                print("mcc: %i" % mcc)
                print("mnc: %i" % mnc)
                print("lac: %i" % lac)
                print("Cell ID: %i" % cellid)

                td = TrackerUpload(tracker=tracker,
                                   timestamp=datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                                   sequence=seq,
                                   charging=charging,
                                   battery=vbat,
                                   wur=wur,
                                   wdgc=wdgc,
                                   source=source,
                                   mcc=mcc,
                                   mnc=mnc,
                                   lac=lac,
                                   cellid=cellid)

            if source == 'GPS':
                lat = float(data[7])
                lon = float(data[8])
                speed = int(data[9])
                precision = int(data[10])
                print("lat: %.5f" % lat)
                print("lon: %.5f" % lon)
                print("speed: %.2fkm/h" % speed)
                print("precision: %i" % precision)

                td = TrackerUpload(tracker=tracker,
                                   timestamp=datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)),
                                   sequence=seq,
                                   charging=charging,
                                   battery=vbat,
                                   wur=wur,
                                   wdgc=wdgc,
                                   source=source,
                                   latitude=lat,
                                   longitude=lon,
                                   speed=speed,
                                   precision=precision)

        except:
            return HttpResponse("Malformed message!")

        td.save()
        # Return Configurations
        return JsonResponse({
            'Mode': tracker.Mode,
            'Tint': tracker.Tint,
            'TGPS': tracker.TGPS,
            'Tsend': tracker.Tsend,
        })
