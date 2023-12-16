import network
import urequests as requests
import ntptime
import utime
import env
import machine

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
        utime.sleep(5)
        
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    
    print("Connected to WiFi")

def synchronize_time():
    # Synchronize time with NTP server
    ntptime.settime()

def get_formatted_time():
    current_time = utime.localtime()
    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[0], current_time[1], current_time[2],
        current_time[3], current_time[4], current_time[5]
    )
    return formatted_time

def convert_adc_to_temperature(adc_value):
    """Converts ADC value to temperature."""
    # Here we assume a simple conversion. The actual conversion depends on the sensor.
    # In this example, we convert ADC values in the range of 0 to 65535 to temperatures in the range of 0°C to 100°C.
    temperature = adc_value * 100 / 65535
    return temperature

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
        synchronize_time()

        mongodb_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-rfbar/endpoint/data/v1/action/insertOne"
        mongodb_headers = {"api-key": API_KEY}

        current_time = get_formatted_time()

        # Create an object for analog-to-digital conversion using ADC(0).
        sensor = machine.ADC(0)
        # Read temperature from the analog sensor.
        adc_value = sensor.read_u16()

        # Convert ADC value to temperature.
        temperature = convert_adc_to_temperature(adc_value)

        document_to_add = {
            "device": "MyPico",
            "temperature": temperature,
            "timestamp": current_time
        }

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
