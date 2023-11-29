from machine import Pin
import time

# Set up the LED on pin GP16 as an OUTPUT pin
led = Pin(16, Pin.OUT)

# Set up the button on pin GP14 as an INPUT pin with pull-down resistor
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

while True:
    # Check if the button is pressed (input is HIGH due to pull-down resistor)
    if button.value():
        print("Button is pressed!")

        # Toggle the state of the LED (ON to OFF or OFF to ON)
        led.toggle()

        # Add a small delay to avoid rapid toggling when the button is held down
        time.sleep(0.5)
