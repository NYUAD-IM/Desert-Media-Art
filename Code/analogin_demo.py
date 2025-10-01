# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modified by Michael Ang for Desert Media Art

# Connections:
# A0 - Potentiometer as voltage divider
# A1 - Photoresistor as voltage divider

"""CircuitPython Essentials Analog In example"""
import time
import board
from analogio import AnalogIn

print("analogin_demo")

pot_in = AnalogIn(board.A0)
photo_in = AnalogIn(board.A1)

photo_threshold = 0.5

# Convert raw ADC reading to voltage
# 10-bit ADC reads 0-65536
def get_voltage(raw_reading):
    return (raw_reading * 3.3) / 65536

# Convert raw ADC reading to 0-1.0
def get_percentage(raw_reading):
    return raw_reading / 65536.0

while True:
    pot_raw = pot_in.value
    photo_raw = photo_in.value

    # Check if light level is above threshold
    photo_triggered = get_percentage(photo_raw) > photo_threshold

    # Output raw readings with voltage values and trigger
    print(("pot", pot_raw, get_voltage(pot_raw), "photo", photo_raw, get_voltage(photo_raw), photo_triggered))
    time.sleep(0.1)
