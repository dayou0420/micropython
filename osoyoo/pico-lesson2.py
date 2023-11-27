from machine import Pin
import time

led = Pin(16, Pin.OUT) #set GP16 as OUTPUT pin , connect it to LED
button = Pin(14, Pin.IN,Pin.PULL_DOWN) #set GP14 as INPUT pin , connect it to button

while True:
    if button.value():
        print("Button is pressed!")
        led.toggle()
        time.sleep(0.5)