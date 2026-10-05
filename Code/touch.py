# NYUAD IM
# Desert Media Art
# Modified by Lydia Yan
#
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Reference: https://learn.adafruit.com/circuitpython-essentials/circuitpython-cap-touch

"""CircuitPython Essentials Capacitive Touch example"""
print("touch")

import time
import board
import touchio

# On the RP2040 there is no built-in touch hardware, so you need to connect
# a 1M ohm resistor between the touch pad pin and ground.
# Pad on pin D24. You can change it to another free pin.
touch_pin = board.D24

touch_pad = touchio.TouchIn(touch_pin)

while True:
    # touch_pad.raw_value is the raw value from the touch pad. It will be a number between 0 and 65535.
    # touch_pad.threshold is the threshold value for the touch pad.
    # touch_pad.value is a boolean value that is True if the touch pad reads above the threshold.

    if touch_pad.value:
        print("raw_value: ", touch_pad.raw_value, "threshold: ", touch_pad.threshold, "touched!")
    else:
        print("raw_value: ", touch_pad.raw_value, "threshold: ", touch_pad.threshold)

    time.sleep(0.1)
