from machine import Pin, PWM
from time import sleep

led_1 = Pin(0, Pin.OUT)
led_2 = Pin(1, Pin.OUT)
led_3 = Pin(2, Pin.OUT)
led_4 = Pin(3, Pin.OUT)
led_5 = Pin(4, Pin.OUT)
led_6 = Pin(5, Pin.OUT)
led_7 = Pin(6, Pin.OUT)

buzzer = PWM(Pin(15))
buzzer.freq(500)
buzzer.duty_u16(200)
sleep(1)
buzzer.duty_u16(0)

for i in range(5):
    led_1.value(1)

    sleep(1)
    led_1.value(0)
    led_2.value(1)

    sleep(1)
    led_2.value(0)
    led_3.value(1)

    sleep(1)
    led_3.value(0)
    led_4.value(1)

    sleep(1)
    led_4.value(0)
    led_5.value(1)

    sleep(1)
    led_5.value(0)
    led_6.value(1)

    sleep(1)
    led_6.value(0)
    led_7.value(1)

    sleep(1)
    led_7.value(0)
    buzzer.duty_u16(0)
