from machine import Pin, PWM
from time import sleep

# Define pins for LEDs
led_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Define pin for the buzzer
buzzer = PWM(Pin(16))
melody = [262, 294, 330, 349, 392, 440, 494, 523]

def play_song():
    for note in melody:
        buzzer.freq(note)
        buzzer.duty_u16(500)
        sleep(0.5)
        buzzer.duty_u16(0)
        sleep(0.1)

def light_leds():
    for led in leds:
        led.value(1)
        sleep(1)
        led.value(0)

def main():
    for _ in range(5):
        light_leds()
        play_song()

if __name__ == "__main__":
    main()
