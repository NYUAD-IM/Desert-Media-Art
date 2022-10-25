# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modified by Mangtronix for Desert Media Art at NYUAD
# https://desert.nyuadim.com

"""Simple rainbow example for 12-pixel NeoPixel ring"""

print("Starting neoring")

import digitalio
import board
from rainbowio import colorwheel
import neopixel


NUM_PIXELS = 12  # NeoPixel ring length (in pixels)
BRIGHTNESS = 0.25 # Let's not blind everyone

# The power for the NeoPixels is not enabled by default (to save battery power)
# We need to turn on the power by setting pin D10 high
print("Enabling NeoPixel power!")
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

strip = neopixel.NeoPixel(board.D5, NUM_PIXELS, brightness=BRIGHTNESS)

while True:
    for i in range(255):
        strip.fill((colorwheel(i)))
# Write your code here :-)
