# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Modified for Desert Media Art by Michael Ang

# MP3 playback with tap trigger
# Works on the Feather RP2040 Prop-Maker (uses the onboard accelerometer
# and the I2S amplifier driving the speaker connector)
print("mp3tap")

import time
import board
import digitalio
import audiobusio
import audiomp3
import adafruit_lis3dh

startup_play = False  # set to True to play all samples once on startup

# Set up the onboard accelerometer on the I2C bus
i2c = board.I2C()
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
accel = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
accel.set_tap(1, 100)  # single or double-tap, threshold

# The amplifier is only powered when EXTERNAL_POWER is enabled
enable = digitalio.DigitalInOut(board.EXTERNAL_POWER)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

sample_number = 0
samples = ['happy.mp3', 'slow.mp3']

# You have to specify some mp3 file when creating the decoder.
# Changing the .file property later reuses the decoder, which
# helps avoid running out of memory.
decoder = audiomp3.MP3Decoder(open(samples[0], "rb"))

print("Tap to play.")

if startup_play:  # Play all on startup
    for sample in samples:
        print("Now playing: '{}'".format(sample))
        decoder.file = open(sample, "rb")
        audio.play(decoder)

        while audio.playing:
            time.sleep(0.1)


while True:
    if accel.tapped and audio.playing is False:
        sample = samples[sample_number]
        print("Now playing: '{}'".format(sample))
        decoder.file = open(sample, "rb")
        audio.play(decoder)
        sample_number = (sample_number + 1) % len(samples)
