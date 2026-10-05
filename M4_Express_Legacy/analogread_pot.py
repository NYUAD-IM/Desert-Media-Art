# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Modified for Desert Media Art by Michael Ang

import time
import board
from analogio import AnalogIn

print("Read from analog")

'''Scale sensor reading to a float from 0.0 to 1.0'''
def scaleReading(reading):
    maxValue = 65535
    minValue = 256
    return reading / (maxValue - minValue)

potentiometer = AnalogIn(board.A1)  # potentiometer connected to A1, Aref & ground

while True:

    #print((potentiometer.value,))      # Display value

    # Get a value from 0.0 to 1.0
    scaled = scaleReading(potentiometer.value)

    # Convert to degrees - 270 degrees full range
    degrees = scaled * 270
    print((int(degrees),)) # print using special formatting needed by plotter
    #print(scaled)

    time.sleep(0.25)                   # Wait a bit before checking all again
