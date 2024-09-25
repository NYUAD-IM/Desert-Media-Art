# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modified by Mangtronix for Desert Media Art at NYUAD
# https://desert.nyuadim.com

# Full tutorial:
# https://desert.nyuadim.com/2022/10/25/tutorial-neopixels-with-prop-maker-featherwing/

# Make sure to have neopixel.mpy and adafruit_bus_device
# copied to /lib on your CIRCUITPY drive

"""Simple rainbow example for 12-pixel NeoPixel ring"""

print("Starting neoring")

import digitalio
import board
from rainbowio import colorwheel
import neopixel
import time

NUM_PIXELS = 12 # NeoPixel ring length (in pixels)
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

# Setting individual pixels
#while True:
#    strip[0] = (255, 0, 0)
#    strip[1] = (0, 255, 0)
#    strip.show()
