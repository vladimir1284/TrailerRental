import requests

#url = 'http://trailerrental.pythonanywhere.com/towit/tracker_debug'
url = 'http://localhost:8000/towit/tracker_debug'


    
def upload_data(msg_type: str):
# Upload data to the remote server
    msg = None

    if msg_type == "wake":
        msg = "{},{},{},{},{},{},{},{}".format(
            "wake",
            865235030873836,
            5,
            1,
            3985,
            130,
            0,
            1
        )

    if msg_type == "error":
        msg = "{},{},{},{},{},{},{}".format(
            "error",
            865235030873836,
            2,
            0,
            4123,
            346,
            105
        )

    if msg_type == "gps":
        msg = "{},{},{},{},{},{},{:.5f},{:.5f},{},{},{},{},{}".format(
            'gps',
            865235030873836,
            1,
            1,
            4123,
            0,
            41.64403,      # latitude
            -108.54682,    # longitude
            102, # speed_kph
            85, # headi11ng
            4,      # Number of sats
            346,
            105
        )

    if msg is not None: 
        x = requests.post(url, data = msg)
        print(x.text)    
    else:
        print("Unknown message type: {}".format(msg_type))    

upload_data("wake")