import time
import network
import socket
from machine import Pin
import env

class WebServer:
    def __init__(self):
        self.led = Pin('LED', Pin.OUT)
        self.button = Pin(16, Pin.IN, Pin.PULL_UP)
        self.ledState = 'LED State Unknown'
        self.ssid = env.SSID
        self.password = env.PASSWORD
        self.wlan = network.WLAN(network.STA_IF)
        self.html_template = """<!DOCTYPE html><html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
        .button { border: 2px solid #000000; color: white; padding: 15px 32px; font-size: 16px; margin: 4px 2px; cursor: pointer; }
        .buttonGreen { background-color: #4CAF50; }
        .buttonRed { background-color: #D11D53; }
        </style></head>
        <body><center><h1>Control Panel</h1></center><br><br>
        <form><center>
        <center> <button class="button buttonGreen" name="led" value="on" type="submit">LED ON</button>
        <br><br>
        <center> <button class="button buttonRed" name="led" value="off" type="submit">LED OFF</button>
        </form>
        <br><br>
        <br><br>
        <p>%s<p></body></html>
        """

    def connect_to_wifi(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('Connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])

    def start_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print('listening on', addr)

        while True:
            try:
                cl, addr = s.accept()
                print('client connected from', addr)

                request = cl.recv(1024)
                print("request:")
                print(request)
                request = str(request)

                self.handle_request(request)
                self.update_states()

                response = self.html_template % self.get_state_message()

                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()

            except OSError as e:
                cl.close()
                print('connection closed')

    def handle_request(self, request):
        led_on = request.find('led=on')
        led_off = request.find('led=off')

        print('led on = ' + str(led_on))
        print('led off = ' + str(led_off))

        if led_on == 8:
            print("led on")
            self.led.value(1)
        elif led_off == 8:
            print("led off")
            self.led.value(0)

    def update_states(self):
        self.ledState = "LED is OFF" if self.led.value() == 0 else "LED is ON"

    def get_state_message(self):
        buttonState = "Button is NOT pressed" if self.button.value() == 1 else "Button is pressed"
        return self.ledState + " and " + buttonState

if __name__ == "__main__":
    server = WebServer()
    server.connect_to_wifi()
    server.start_server()
