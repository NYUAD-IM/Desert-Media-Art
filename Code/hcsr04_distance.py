
# Example of using HC-SR04 ultrasonic sensor with CircuitPython
# Adapted from
# https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython#circuitpython-and-python-usage-of-hc-sr04-3046469

# Modifications by Michael Ang for Desert Media Art
# 2024-10-08

# Pins for the Feather RP2040 Prop-Maker:
# - D5 is the trigger pin and D6 is the echo pin. Both are free on this board
#   (the Prop-Maker functions have their own pins, such as
#   board.ACCELEROMETER_INTERRUPT and board.EXTERNAL_NEOPIXELS).

# Circuit:
# Schematic: Circuits/hcsr04_distance_schematic.png
# https://github.com/NYUAD-IM/Desert-Media-Art/blob/main/Circuits/hcsr04_distance_schematic.png
# Or follow the wiring here, using D5 for trigger and D6 for echo
# https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython#circuitpython-microcontroller-wiring-3046455
# - the sensor is powered from USB (5V), which is the "USB" pin on the Feather
# - the microcontroller can't accept more than 3.3V input, so we use a simple
#   voltage divider using the two 10K resistors to bring the 5V signal
#   from "echo" to an acceptable range

print("hcsr04_distance")

import time
import board
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

while True:
    try:
        print((sonar.distance,))
    except RuntimeError as e:
        print(e)
        print("Retrying!")
    time.sleep(0.1)
