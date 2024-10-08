print("HC-SR04 distance test")

# Example of using HC-SR04 ultrasonic sensor with CircuitPython
# Adapted from 
# https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython#circuitpython-and-python-usage-of-hc-sr04-3046469

# Modifications by Michael Ang for Desert Media Art
# 2024-10-08

# We can't use D5 or D6 for the sensor since they
# are used by the Prop-Maker Featherwing
# https://learn.adafruit.com/adafruit-prop-maker-featherwing/pinouts
# - IRQ - Interrupt pin for LIS3DH accelerometer, used for tap or shake detection. Connected to D6 on Feather M0 or M4.
# - NeoPixel (NEO) - Data pin for NeoPixel connector. This pin is level shifted to 5V output. Connected to D5 on Feather M0 or M4.

# That page gives us a hint which pins we should use:
# Available Logic Pins:
#   The logic pins in the longer section along the bottom on the PropMaker
#   FeatherWing are not used, except for A0. These pins differ by Feather,
#   therefore a list is not included here. The pins are available to use
#   for other purposes, such as multiple buttons, etc.

# Referring to the pinout page for the Adafruit M4 Express Feather
# we can see that A2-A5 along the bottom row look like good candidates.
# Let's use A4 and A5

# Circuit:
# Follow the wiring here, but use A4 and A5 instead of D5 and D6
# https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython#circuitpython-microcontroller-wiring-3046455

import time
import board
import adafruit_hcsr04

# Original pins from example
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

# Using pins for M4 Express Feather with Prop-Maker Featherwing
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A4, echo_pin=board.A5)

while True:
    try:
        print((sonar.distance,))
    except RuntimeError as e:
        print(e)
        print("Retrying!")
    time.sleep(0.1)
