from machine import Pin
from time import sleep

class LEDController:
    def __init__(self, pin_numbers):
        self.led_pins = pin_numbers
        self.leds = [Pin(pin, Pin.OUT) for pin in self.led_pins]

    def light_leds(self):
        # Turn on each LED one by one and wait for 0.5 seconds
        for led in self.leds:
            led.value(1)
            sleep(0.5)
            led.value(0)

    def light_leds_reversed(self):
        # Turn on each LED one by one in reverse order and wait for 0.5 seconds
        for led in reversed(self.leds):
            led.value(1)
            sleep(0.5)
            led.value(0)

    def light_leds_even(self):
        # Turn on even-indexed LEDs one by one and wait for 0.5 seconds
        for i, led in enumerate(self.leds):
            if i % 2 == 0:
                led.value(1)
                sleep(0.5)
                led.value(0)

    def light_leds_odd(self):
        # Turn on odd-indexed LEDs one by one and wait for 0.5 seconds
        for i, led in enumerate(self.leds):
            if i % 2 != 0:
                led.value(1)
                sleep(0.5)
                led.value(0)

    def run_sequence(self, num_repeats):
        # Repeat the combined LED sequence specified number of times
        for _ in range(num_repeats):
            self.light_leds()
            self.light_leds_reversed()
            self.light_leds_even()
            self.light_leds_odd()

def main():
    # Define pins for LEDs
    led_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    # Create an instance of LEDController
    led_controller = LEDController(led_pins)

    # Run the combined LED sequence 10 times
    led_controller.run_sequence(10)

if __name__ == "__main__":
    main()
