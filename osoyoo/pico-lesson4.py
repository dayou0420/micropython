from machine import I2C, Pin, ADC
from time import sleep
from pico_i2c_lcd import I2cLcd

sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

def get_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]

print("I2C Address:", I2C_ADDR)

lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
degree = bytearray([0x1c, 0x14, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00])
lcd.custom_char(0, degree)

while True:
    temperature = get_temperature()
    print("Temperature:", temperature)

    lcd.putstr("Temperature:\n" + str(temperature) + " C" + chr(0))
    sleep(4)
    lcd.clear()
