from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from ..forms import TrackerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from towit.models import Tracker, TrackerData

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
               "Wrong ID": 201,
               }

SKEY = "c0ntr453n1a"

class TrackerUpdateView(LoginRequiredMixin,UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'towit/trailer/new_tracker.html' 
    
    def form_valid(self, form):
        if(Tracker.objects.get(id=self.kwargs['pk']).Tint !=  form.instance.Tint):
            storeForUpdate('Tint', form.instance.Tint, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).TintB !=  form.instance.TintB):
            storeForUpdate('TintB', form.instance.TintB, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).Tcheck !=  form.instance.Tcheck):
            storeForUpdate('Tcheck', form.instance.Tcheck, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).MAX_ERRORS !=  form.instance.MAX_ERRORS):
            storeForUpdate('MAX_ERRORS', form.instance.MAX_ERRORS, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPS !=  form.instance.TGPS):
            storeForUpdate('TGPS', form.instance.TGPS, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).TGPSB !=  form.instance.TGPSB):
            storeForUpdate('TGPSB', form.instance.TGPSB, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).SMART !=  form.instance.SMART):
            storeForUpdate('SMART', form.instance.SMART, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).Tsend !=  form.instance.Tsend):
            storeForUpdate('Tsend', form.instance.Tsend, form.instance)
        if(Tracker.objects.get(id=self.kwargs['pk']).TsendB !=  form.instance.TsendB):
            storeForUpdate('TsendB', form.instance.TsendB, form.instance)
            
            
        return super(TrackerUpdateView, self).form_valid(form)
    
def storeForUpdate(key, value, instance):
    data_low = value & 0xff
    data_high = (value >> 8) & 0xff
    if (len(instance.pendingConfigs) < 3):
        instance.pendingConfigs = bytes([addrs[key], data_low, data_high])
    else:
        data = [val for val in instance.pendingConfigs]
        exist = False
        for i in range(0,len(data), 3):
            if (addrs[key] == data[i]):
                # Already modified
                data[i+1] = data_low
                data[i+2] = data_high
                exist = True
                break
        if (not(exist)): # Add a new pending configuration
            data.append(addrs[key])
            data.append(data_low)
            data.append(data_high)
        instance.pendingConfigs = bytes(data)
    
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
def tracker_data(request, passwd, tracker_id, lat, lon, battery, power, errors):
    if (SKEY != passwd):
        print("Wrong password: %s" % passwd)
        payload = bytes([error_codes["Wrong password"]])
        response = HttpResponse(payload)
        return response
    try:
        tracker = Tracker.objects.get(id=tracker_id) 
    except:
        print("Wrong ID: %i" % tracker_id)
        payload = bytes([error_codes["Wrong ID"]])
        response = HttpResponse(payload)
        return response
    # Store data
    data = TrackerData(tracker=tracker,
                        longitude=float(lon),
                        latitude=float(lat),
                        battery=battery,
                        powered=power,
                        errors=errors)

    data.save()
    
    if (tracker.pendingConfigs != b''): # Send and clean pending data
        nData = bytes([int(len(tracker.pendingConfigs)/3)])
        payload = nData + tracker.pendingConfigs
        response = HttpResponse(payload)
        tracker.pendingConfigs = b''
        tracker.save()
        print("here")
        return response        
    else:
        payload = bytes([0])
        response = HttpResponse(payload)
        print("there")
        return response

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
        data = TrackerData.objects.filter(tracker=tracker).order_by("-timestamp")[0]
    except:
        return render(request, 'towit/tracker/tracker.html', {'tracker': tracker})
    
    return render(request, 'towit/tracker/tracker_data.html', {'tracker': tracker,
                                                               'data': data})
@login_required
def trackers(request):
    trackers = Tracker.objects.all()
    return render(request, 'towit/tracker/trackers.html', {'trackers': trackers})



