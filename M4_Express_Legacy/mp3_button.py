# NYU Abu Dhabi Interactie Media
#
# Desert Media Art
#
# Tutorial for Sound on M4 Express / Prop-Maker
#
# Modified by Lydia Yan
#
# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
#
# Reference: https://learn.adafruit.com/mp3-circuitpython-lars?view=all#code-dot-py-3064048-3
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio

"""CircuitPython Essentials Audio Out MP3 Example"""

import time
import board
import busio
import digitalio
import audioio
import audiomp3

# Digital input using external push button
button = digitalio.DigitalInOut(board.A1)
button.switch_to_input(pull=digitalio.Pull.UP)

num_sample = 3 # The amount of your mp3 files
sample_number = 0 # Initial played file

# Set up speaker enable pin
enable = digitalio.DigitalInOut(board.D10)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

# Output from external speaker
speaker = audioio.AudioOut(board.A0)


while True:
    # Play your music files in cycle
    for i in range(num_sample):
        # You may also specify your files' names, here the file names are in number orders starting from 0.
        sample = "/mang/{}.mp3".format(sample_number)
        mp3stream = audiomp3.MP3Decoder(open(sample, "rb"))
        speaker.play(mp3stream)
        sample_number = (sample_number + 1) % 10
        print("playing", sample)
        if i >= (num_sample-1):
            sample_number = 0

        # This allows you to do other things while the audio plays!
        while speaker.playing:
            pass

        print("Waiting for button press to continue!")
        while button.value:
            pass
