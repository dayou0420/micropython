import machine
import utime

def convert_adc_to_temperature(adc_value):
    """Converts ADC value to temperature."""
    # Here we assume a simple conversion. The actual conversion depends on the sensor.
    # In this example, we convert ADC values in the range of 0 to 65535 to temperatures in the range of 0°C to 100°C.
    temperature = adc_value * 100 / 65535
    return temperature

def main():
    # Create an object for analog-to-digital conversion using ADC(0).
    sensor = machine.ADC(0)

    # Infinite loop
    while True:
        # Read temperature from the analog sensor.
        adc_value = sensor.read_u16()

        # Convert ADC value to temperature.
        temperature = convert_adc_to_temperature(adc_value)

        # Print the temperature.
        print("Temperature: {:.1f}".format(temperature))

        # Wait for 4 seconds.
        utime.sleep(4)

if __name__ == "__main__":
    main()
