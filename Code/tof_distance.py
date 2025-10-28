# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of the VL53L1X distance sensor.
# Will print the sensed range/distance every second.

# https://learn.adafruit.com/adafruit-vl53l1x/python-circuitpython

# Adapted for Desert Media Art
# by Michael Ang
# 2025-10-28
#
# Onboard NeoPixel will go through R, G, B, W for 0, 100, 200, 300+ cm

print("distance_demo")

import time
import math

import board

import adafruit_vl53l1x

# NeoPixel setup
if hasattr(board, "APA102_SCK"):
    import adafruit_dotstar

    pixel = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    import neopixel

    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

min_brightness = 0.1
max_brightness = 0.5
pixel.brightness = 0.05
pixel[0] = (255,255,255)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
# vl53.distance_mode = 1 # short - up to 136cm
vl53.distance_mode = 2 # long range - up to 400cm

# Increasing the timing budget (in ms) increases the maximum distance the device can range and improves the repeatability error.
vl53.timing_budget = 100 

print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = vl53.model_info
print(f"Model ID: 0x{model_id:0X}")
print(f"Module Type: 0x{module_type:0X}")
print(f"Mask Revision: 0x{mask_rev:0X}")
print("Distance Mode: ", end="")
if vl53.distance_mode == 1:
    print("SHORT")
elif vl53.distance_mode == 2:
    print("LONG")
else:
    print("UNKNOWN")
print(f"Timing Budget: {vl53.timing_budget}")
print("--------------------")

vl53.start_ranging()

"""Brightness starts at min_brightness at each meter then increases"""
def distance_to_brightness(distance):
    if not distance:
        return 0

    brightness = (distance % 100) / 100. * max_brightness + min_brightness
    brightness = min(brightness, max_brightness)

    return gamma_correction(brightness)

# From Perplexity
def distance_to_color(distance):
    if not distance:
        return (0, 0, 0)
    if distance < 100:
        return (255, 0, 0)       # Red
    elif distance < 200:
        return (0, 255, 0)       # Green
    elif distance < 300:
        return (0, 0, 255)       # Blue
    else:
        return (255, 255, 255)   # White

def gamma_correction(linear_value, max_linear_value=1, gamma=1.8):
    normalized = linear_value / max_linear_value
    return normalized ** gamma

while True:
    if vl53.data_ready:

        distance = vl53.distance

        # Set color and brightness based on distance
        pixel[0] = distance_to_color(distance)
        pixel.brightness = distance_to_brightness(distance)
    
        
        print(f"Distance: {distance} cm")
        vl53.clear_interrupt()
        time.sleep(0.1) 
