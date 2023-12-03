from machine import I2C, Pin, ADC, PWM
from time import sleep
from pico_i2c_lcd import I2cLcd

# センサーのピン番号
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

# 温度を取得する関数
def get_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    # 温度の計算式
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

# I2Cの初期化
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]

print("I2C Address:", I2C_ADDR)

# LCDの初期化
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
degree = bytearray([0x1c, 0x14, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00])
lcd.custom_char(0, degree)

# Set up the LED on pin GP16 as an OUTPUT pin
led = Pin(16, Pin.OUT)

# Create a PWM object for the buzzer on pin 15
buzzer = PWM(Pin(15))

# melody = [262:ド, 294:レ, 330:ミ, 349:ファ, 392:ソ, 440:ラ, 494:シ, 523:ド ]
melody = [ 262, 294, 330, 349, 330, 294, 262 ]

def play_frog_song():
    for note in melody:
        # Play each note of the melody
        buzzer.freq(note)
        buzzer.duty_u16(100)
        # Play each note for 0.5 seconds
        sleep(1)
        buzzer.duty_u16(0)
        # Short pause between notes
        sleep(0.1)

while True:
    # 温度を取得
    temperature = get_temperature()
    print("Temperature:", temperature)

    # Toggle the state of the LED (ON to OFF or OFF to ON)
    led.toggle()

    # LCDに温度を表示
    lcd.putstr("Temperature:\n" + str(temperature) + " C" + chr(0))

    # Play frog song
    play_frog_song()

    sleep(3)

    # Set the duty cycle of the buzzer to 0 (minimum) to turn it off
    buzzer.duty_u16(0)

    lcd.clear()
