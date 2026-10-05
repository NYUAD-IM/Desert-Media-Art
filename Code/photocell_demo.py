# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

print("photocell_demo")

# Wiring
# A1 - photocell as voltage divider with 10K resistor to GND

import time
import board
from analogio import AnalogIn
import digitalio

# Delay to see startup message 
time.sleep(1)

# Measured minimum and maximum ADC readings for photocell dark / bright
PHOTOCELL_MINIMUM = 29000
PHOTOCELL_MAXIMUM = 55000

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

analog_in = AnalogIn(board.A1)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# Sensor normalization function
# Generated with ChatGPT-6 Sol Medium
def normalize_sensor(value, minimum, maximum):
    if minimum == maximum:
        raise ValueError("minimum and maximum must differ")
    return max(0.0, min(1.0, (value - minimum) / (maximum - minimum)))


while True:
    # print((get_voltage(analog_in),))

    #normalized_value = analog_in.value / 65535
    normalized_value = normalize_sensor(analog_in.value, PHOTOCELL_MINIMUM, PHOTOCELL_MAXIMUM)

    bright_threshold = 0.5

    if normalized_value < bright_threshold:
        direction = "Dark"
        led.value = True
    else:
        direction = "Bright"
        led.value = False

    print(analog_in.value, normalized_value, direction)

    time.sleep(0.1)

