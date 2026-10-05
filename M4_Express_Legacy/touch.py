# NYUAD IM
# Desert Media Art
# Modified by Lydia Yan
#
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Reference: https://learn.adafruit.com/circuitpython-essentials/circuitpython-cap-touch

"""CircuitPython Essentials Capacitive Touch example"""
import time
import board
import touchio

# Please change the pin code if you want to use other pins. (A0-A5)
touch_pad0 = board.A0

touch0 = touchio.TouchIn(touch_pad0)

while True:
    if touch0.value:
        print("A0 Touched!")
    time.sleep(0.05)
