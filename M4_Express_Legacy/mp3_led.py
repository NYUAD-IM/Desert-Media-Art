# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MP3 playback with tap trigger
# Works on Feather M4 (or other M4 based boards) with Propmaker
import time
import board
import busio
import digitalio
import audioio
import audiomp3
import adafruit_lis3dh

import pwmio
import board
from rainbowio import colorwheel
import digitalio


red = pwmio.PWMOut(board.D11, duty_cycle=0, frequency=20000)
green = pwmio.PWMOut(board.D12, duty_cycle=0, frequency=20000)
blue = pwmio.PWMOut(board.D13, duty_cycle=0, frequency=20000)



startup_play = False  # set to True to play all samples once on startup

# Set up accelerometer on I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)
accel = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
accel.set_tap(1, 100)  # single or double-tap, threshold

# Set up speaker enable pin
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

speaker = audioio.AudioOut(board.A0)

num_samples = 3
sample_number = 0

# RGB as float
def set_led(red_val, green_val, blue_val):
    red.duty_cycle = int(red_val * 65535)
    green.duty_cycle = int(green_val * 65535)
    blue.duty_cycle = int(blue_val * 65535)

color = (0.5, 0, 0)

print("Lars says, 'Hello, CVT Joseph. Tap to play.'")

if startup_play:  # Play some on startup
    for i in range(2):
        sample = "/mang/{}.mp3".format(i)
        print("Now playing: '{}'".format(sample))
        mp3stream = audiomp3.MP3Decoder(open(sample, "rb"))
        speaker.play(mp3stream)

        while speaker.playing:
            time.sleep(0.1)
    enable.value = speaker.playing


while True:
    if accel.tapped and speaker.playing is False:
        sample = "/mang/{}.mp3".format(sample_number)
        print("Now playing: '{}'".format(sample))
        mp3stream = audiomp3.MP3Decoder(open(sample, "rb"))
        speaker.play(mp3stream)
        sample_number = (sample_number + 1) % num_samples
    enable.value = speaker.playing
    set_led(color[0], color[1], color[2]) # hacky
