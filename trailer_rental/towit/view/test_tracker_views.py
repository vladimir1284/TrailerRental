import requests

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

addrs_val_list = list(addrs.values())
addrs_key_list = list(addrs.keys())

error_codes = {"Wrong password": 200,
               "Wrong ID": 201,
               }

err_val_list = list(error_codes.values())
err_key_list = list(error_codes.keys())


def processResult(result):
    content = [x for x in result.content]
    print(content)
    first_byte = content[0]
    if (first_byte in err_val_list):
        print(err_key_list[err_val_list.index(first_byte)])
    else:
        for i in range(first_byte):
            print("Data index: %i" % (i+1))
            print("%s: %i" % (addrs_key_list[addrs_val_list.index(
                content[i*3+1])], content[i*3+2] + content[i*3+3] * 256))

# # Get ID
# result = requests.get("http://localhost:8000/towit/tracker_id/c0ntr453n1a/864713037301317")
# processResult(result)
#
# # Get Parameters
# result = requests.get("http://localhost:8000/towit/tracker_parameters/c0ntr453n1a/2")
# processResult(result)


# Upload data
result = requests.get(
    "http://trailerrental.pythonanywhere.com/towit/tracker_data/c0ntr453n1a/3/2133456/7893457/72/1/2/0")
processResult(result)
