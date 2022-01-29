from django.apps import AppConfig
import struct
from paho.mqtt import client as mqtt_client
import pytz
from datetime import datetime
from django.conf import settings

power_modes ={1: False,
              6: True,
            }

class TowitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'towit'
    def ready(self):        
        client = connect_mqtt()
        subscribe(client)
        client.loop_start()



#broker = 'localhost'
broker = 'test.mosquitto.org'
port = 1883
#topic = "864713037301317"
# generate client ID with pub prefix randomly
client_id = 'towit-houston'
# username = 'emqx'
# password = 'public'

"""
  Parse binary data from tracker
  msg structure:    
    seq     (1byte)  - Sequence number
    mode    (1byte)  - Tracker operation mode
    event   (1byte)  - Tracker event
    sats    (1byte)  - Number of connected sats
    vbat    (2bytes) - Battery voltage mV
    heading (2bytes) - Heading course deg
    lat     (4bytes) - Latitude (float)
    lon     (4bytes) - Longitude (float)
    speed   (4bytes) - Speed km/h (float)
"""
def decode_payload(msg):
    from towit.models import Tracker, TrackerData
    try:
        data = struct.unpack("BBBBHHfff", msg.payload)
        seq     = data[0]
        mode    = data[1]
        event   = data[2]
        sats    = data[3]
        vbat    = data[4]/1000. # Volts
        heading = data[5]
        lat     = data[6]
        lon     = data[7]
        speed   = data[8]
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
        print("Malformed msg from %s!" % msg.topic)
        return
    try:
        tracker = Tracker.objects.get(imei=int(msg.topic))
        # No repeated messages
        last_seq = -1
        try:
            last_seq = TrackerData.objects.filter(tracker=tracker).order_by("-timestamp")[0].sequence
        except:
            print("No previous data")
        if (seq != last_seq): # Only save if record does not exist
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
        print("Unknown IMEI %s!" % msg.topic)
        return
    
    
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        decode_payload(msg)
    # Subscribe to all trackers
    from towit.models import Tracker
    trackers = Tracker.objects.all()
    for tracker in trackers:
        client.subscribe(str(tracker.imei))
    client.on_message = on_message



      