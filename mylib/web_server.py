import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
# ENV
import env

ssid = env.SSID
password = env.PASSWORD



def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


try:
    ip = connect()
    # Edit
    led= machine.Pin('LED', machine.Pin.OUT)
    led.toggle()
    sleep(0.5)
    led.off()
except KeyboardInterrupt:
    machine.reset()