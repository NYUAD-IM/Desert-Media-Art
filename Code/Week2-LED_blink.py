# Example of blinking the built-in LED for Desert Media Art
# Michael Ang
# 2022-09-07

# Uses code from Adafruit
# https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/creating-and-editing-code

print('Hello Desert Media Art 20222!!!!')
print("Let's blink!!!!!")

import board
import digitalio   # Gives us access to the pins
import time

print("It is now " + str(time.monotonic()))

# print('The basic LED is attached to pin ' + str(board.LED))

# This variable gives us access to the hardware pin
led = digitalio.DigitalInOut(board.LED)

# Set the LED pin as an output so we can turn it on/off
led.direction = digitalio.Direction.OUTPUT

# Record the starting time
startTime = time.monotonic()

# How long to blink for (seconds)
secondsToBlink = 5

print("Starting to blink")
while (time.monotonic() - startTime) < secondsToBlink:
    led.value = True
    time.sleep(0.5 / 2)
    led.value = False
    time.sleep(0.5 / 2)
    print("  time - %.1f" % time.monotonic())

print("All done")


