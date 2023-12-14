import machine
import time

# Define Pin objects for each LED
led_red = machine.Pin(14, machine.Pin.OUT)
led_amber = machine.Pin(13, machine.Pin.OUT)
led_green = machine.Pin(12, machine.Pin.OUT)

while True:
    # Turn on the green LED for 5 seconds
    led_green.value(1)
    time.sleep(5)
    led_green.value(0)

    # Blink the amber LED three times with a 0.5-second delay between each blink
    for i in range(3):
        led_amber.value(1)
        time.sleep(0.5)
        led_amber.value(0)
        time.sleep(0.5)

    # Turn on the red LED for 5 seconds
    led_red.value(1)
    time.sleep(5)
    led_red.value(0)
