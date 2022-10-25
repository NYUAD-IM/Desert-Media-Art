# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modified by Mangtronix for Desert Media Art at NYUAD
# https://desert.nyuadim.com

"""Simple rainbow swirl example for 3W LED"""
import pwmio
import board
#from rainbowio import colorwheel
import digitalio
import time

# Using high power LEDs without the proper power supply can
# cause the board to reset.
# Let's wait a few seconds so we have a chance to save new code
# in case the board is constantly resetting.
startup_delay = 3
print("Waiting", startup_delay, "seconds... now's your chance to save new code")
time.sleep(startup_delay)

def colorwheel(pos):
    if pos < 0 or pos > 255:  return (0, 0, 0)
    if pos < 85: return (255 - pos * 3, pos * 3, 0)
    if pos < 170: pos -= 85; return (0, 255 - pos * 3, pos * 3)
    pos -= 170; return (pos * 3, 0, 255 - pos * 3)

print("Firing up LED")
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

red = pwmio.PWMOut(board.D11, duty_cycle=0, frequency=20000)
green = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=20000)
blue = pwmio.PWMOut(board.D13, duty_cycle=0, frequency=20000)

# 0 - 65536
#while True:
#    red.duty_cycle = 600
#    green.duty_cycle = 600
#    blue.duty_cycle = 600

brightness = 0.1
print("Using brightness ", brightness)
while True:
    for i in range(255):
        (r, g, b) = colorwheel(i)
        red.duty_cycle = int((r * 65536 / 256) * brightness)
        green.duty_cycle = int((g * 65536 / 256) * brightness)
        blue.duty_cycle = int((b * 65536 / 256) * brightness)
        time.sleep(0.1)

# 在这里写上你的代码 :-)
