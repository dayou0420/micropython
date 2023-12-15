import time
import network
import urequests as requests
import env

# Wifi Credentials
SSID = env.SSID
PSK = env.PASSWORD
API_KEY = env.API_KEY

def connect_to_wifi(ssid, psk):
    # Enable Wifi in Client Mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Connect to Wifi, keep trying until failure or success
    wlan.connect(ssid, psk)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        time.sleep(5)
        
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    
    print("Connected to WiFi")

def send_data_to_mongodb(url, headers, insert_payload):
    print("Sending data...")
    
    response = requests.post(url, headers=headers, json=insert_payload)
    
    print("Response: ({}) , msg = {}".format(response.status_code, response.text))

    if response.status_code == 201:
        print("Added Successfully")
    else:
        print("Error")

    # Always close response objects so we don't leak memory
    response.close()

def main():
    try:
        connect_to_wifi(SSID, PSK)

        mongodb_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-rfbar/endpoint/data/v1/action/insertOne"
        mongodb_headers = {"api-key": API_KEY}

        document_to_add = {"device": "MyPico", "readings": [1, 3, 1, 2, 6, 2, 6]}

        insert_payload = {
            "dataSource": "Cluster0",
            "database": "MyData",
            "collection": "deviceReadings",
            "document": document_to_add,
        }

        send_data_to_mongodb(mongodb_url, mongodb_headers, insert_payload)

    except Exception as e:
        print(e)

    finally:
        # Stop the Wifi
        try:
            wlan.active(False)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
