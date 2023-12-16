import network
import urequests as requests
import ntptime
import utime
import env
import machine

class DataSender:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def send_data(self, insert_payload):
        print("Sending data...")
        response = requests.post(self.url, headers=self.headers, json=insert_payload)
        print("Response: ({}) , msg = {}".format(response.status_code, response.text))

        if response.status_code == 201:
            print("Added Successfully")
        else:
            print("Error")

        # Always close response objects so we don't leak memory
        response.close()

class TemperatureSensor:
    def __init__(self, adc_pin):
        self.sensor = machine.ADC(adc_pin)

    def read_temperature(self):
        adc_value = self.sensor.read_u16()
        # Convert ADC value to temperature.
        temperature = self.convert_adc_to_temperature(adc_value)
        return temperature

    @staticmethod
    def convert_adc_to_temperature(adc_value):
        """Converts ADC value to temperature."""
        # Here we assume a simple conversion. The actual conversion depends on the sensor.
        # In this example, we convert ADC values in the range of 0 to 65535 to temperatures in the range of 0°C to 100°C.
        temperature = adc_value * 100 / 65535
        return temperature

class IoTDevice:
    def __init__(self, ssid, psk, api_key, mongodb_url, mongodb_headers):
        self.SSID = ssid
        self.PSK = psk
        self.API_KEY = api_key
        self.mongodb_url = mongodb_url
        self.mongodb_headers = mongodb_headers
        self.wlan = network.WLAN(network.STA_IF)

    def connect_to_wifi(self):
        # Enable Wifi in Client Mode
        self.wlan.active(True)

        # Connect to Wifi, keep trying until failure or success
        self.wlan.connect(self.SSID, self.PSK)

        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            print("Waiting to Connect")
            utime.sleep(5)

        if not self.wlan.isconnected():
            raise Exception("Wifi not available")

        print("Connected to WiFi")

    def synchronize_time(self):
        # Synchronize time with NTP server
        ntptime.settime()

    def get_formatted_time(self):
        current_time = utime.localtime()
        formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            current_time[0], current_time[1], current_time[2],
            current_time[3], current_time[4], current_time[5]
        )
        return formatted_time

    def main(self):
        try:
            self.connect_to_wifi()
            self.synchronize_time()

            current_time = self.get_formatted_time()

            temperature_sensor = TemperatureSensor(0)
            temperature = temperature_sensor.read_temperature()

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

            data_sender = DataSender(self.mongodb_url, self.mongodb_headers)
            data_sender.send_data(insert_payload)

        except Exception as e:
            print(e)

        finally:
            # Stop the Wifi
            try:
                self.wlan.active(False)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    iot_device = IoTDevice(env.SSID, env.PASSWORD, env.API_KEY, env.MONGO_URL, {"api-key": env.API_KEY})
    iot_device.main()
