# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Modified by Michael Ang for Desert Media Art
# Original tutorial: https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio

"""CircuitPython Essentials Audio Out MP3 Example"""
import board
import digitalio
import audiobusio

print("mp3 example")

from digitalio import DigitalInOut, Direction, Pull
# enable external power pin
# provides power to the external components
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# Use button on board (boot button)
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# The listed mp3files will be played in order
mp3files = ["slow.mp3", "happy.mp3"]

# You have to specify some mp3 file when creating the decoder
mp3 = open(mp3files[0], "rb")
decoder = MP3Decoder(mp3)
#audio = AudioOut(board.A0)
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

while True:
    for filename in mp3files:
        # Updating the .file property of the existing decoder
        # helps avoid running out of memory (MemoryError exception)
        decoder.file = open(filename, "rb")
        audio.play(decoder)
        print("playing", filename)

        # This allows you to do other things while the audio plays!
        while audio.playing:
            pass

        print("Waiting for button press to continue!")
        while button.value:
            pass
