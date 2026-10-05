# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modifications by Michael Ang for Desert Media Art NYUAD

"""CircuitPython Essentials NeoPixel RGBW example"""

print("Starting neostrip_rgbw")

import time
import board
import neopixel
import digitalio

pixel_pin = board.D5
num_pixels = 10
brightness = 0.2

# The power for the NeoPixels is not enabled by default (to save battery power)
# We need to turn on the power by setting pin D10 high
print("Enabling NeoPixel power!")
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False,
                           pixel_order=(1, 0, 2, 3))


def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
OFF = (0, 0, 0, 0)

# There are multiple ways we can make white
RGBWHITE = (255, 255, 255, 0) # Combine RGB to make a white
WARMWHITE = (0, 0, 0, 255) # Use the warm white LEDs

# Write the pixels directly
pixels.fill(OFF)
pixels.show() # Send the values to the strip - needed since we have auto_write=False
pixels[0] = (255, 0, 0, 0) # First pixel red
pixels[1] = (0, 255, 0, 0) # Second pixel blue
pixels[2] = (0, 0, 255, 0)
pixels[3] = (255, 255, 255, 0) # White from full RGB
pixels[4] = (0, 0, 0, 255) # White from just the warm white LED
pixels[5] = (128, 128, 128, 128) # White mix
pixels[6] = (255, 255, 255, 255) # Full throttle
pixels.show() # Send the values to the strip
time.sleep(5)

while True:
    print('Normal from combining just RGB - RGBW = (255, 255, 255, 0)')
    pixels.fill(RGBWHITE)
    pixels.show()
    time.sleep(5)

    print('White using only warm white LED - RGBW = (0, 0, 0, 255)')
    pixels.fill(WARMWHITE)
    pixels.show()
    time.sleep(5)

    print('White using a mix - RGBW = (128, 128, 128, 128)')
    pixels.fill((128, 128, 128, 128))
    pixels.show()
    time.sleep(5)

    print('Desaturate blue')
    # Add warm white in steps of 1
    for warm_component in range(0, 255, 1):
        color = (0, 0, 255, warm_component)
        print(color)
        pixels.fill(color)
        pixels.show()
        time.sleep(0.1)

    pixels.fill(RED)
    pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)

    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow
# Write your code here :-)