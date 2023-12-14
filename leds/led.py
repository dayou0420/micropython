from machine import Pin
from time import sleep

class LEDController:
    def __init__(self, pin_numbers):
        self.led_pins = pin_numbers
        self.leds = [Pin(pin, Pin.OUT) for pin in self.led_pins]

    def light_leds(self):
        # Turn on each LED one by one and wait for 1 second
        for led in self.leds:
            led.value(1)
            sleep(1)
            led.value(0)

    def run_sequence(self, num_repeats):
        # Repeat the LED sequence specified number of times
        for _ in range(num_repeats):
            self.light_leds()

def main():
    # Define pins for LEDs
    led_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # Create an instance of LEDController
    led_controller = LEDController(led_pins)

    # Run the LED sequence 5 times
    led_controller.run_sequence(5)

if __name__ == "__main__":
    main()
