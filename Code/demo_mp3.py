# SPDX-FileCopyrightText: 2026 Michael Ang with Claude Code
#
# SPDX-License-Identifier: MIT

print("demo_mp3")

# Minimal demo: play an MP3 every 10 seconds on the Prop-Maker Feather RP2040's
# external speaker (the speaker connector driven by the on-board amp).
# Plays the file named by SOUND_FILE (below the imports), by default
# sounds/strings.mp3 on the CIRCUITPY drive.
#
# Libraries: none to install. Everything used is built into CircuitPython
# itself (board, time, digitalio, audiobusio, audiomp3), so the lib folder
# on CIRCUITPY doesn't need anything for this demo. You only need CircuitPython
# 10.x for the "Adafruit Feather RP2040 Prop-Maker" installed:
#   https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/
# (Libraries from the Adafruit bundle, https://circuitpython.org/libraries, are
# installed by copying the needed .mpy files or folders into CIRCUITPY/lib,
# or with `circup install <library_name>`.)
#
# Setup:
#   1. Copy this file to CIRCUITPY (e.g. as demo_mp3.py).
#   2. Put your MP3 on CIRCUITPY (see "Making your own MP3" below) and set
#      SOUND_FILE to its path, e.g. "sounds/mysound.mp3".
#   3. Connect a speaker to the speaker connector on the board.
#   4. Run it from code.py with "import demo_mp3", or save it as code.py.
#
# Making your own MP3:
#   The board has limited memory and processing power, so compress your audio
#   before copying it over. For example, in Audacity (https://www.audacityteam.org,
#   steps checked with version 3.7.7):
#   1. Open your audio file.
#   2. Choose File > Export Audio... (Ctrl/Cmd+Shift+E).
#   3. In the Export Audio dialog, set Format to "MP3 Files", Channels to
#      Mono and Sample Rate to 22050 Hz. Audacity converts these on export,
#      so you don't need to change the project rate or resample first.
#   4. Set Bit Rate Mode to Constant and Quality to 32 kbps.
#   5. Click Export, and copy the exported file to CIRCUITPY/sounds/ and
#      update SOUND_FILE.
#   Higher quality settings can sound better but may stutter or run out of
#   memory. If so, lower the sample rate or bitrate.
#
# Sound credit: "260709_183106-32_FR_String_trio_in_public_garden" by kevp888
# (Kevin Luce), from Freesound: https://freesound.org/people/kevp888/sounds/873226/
# Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
# Changes: a short excerpt, converted to mono 22050 Hz 32 kbps MP3.

import time
import board
import audiobusio
import audiomp3
from digitalio import DigitalInOut, Direction

SOUND_FILE = "sounds/strings.mp3"  # MP3 to play, relative to CIRCUITPY
PLAY_INTERVAL = 10  # seconds between starts of playback

# The amplifier is only powered when EXTERNAL_POWER is enabled
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

mp3 = audiomp3.MP3Decoder(open(SOUND_FILE, "rb"))

last_play = time.monotonic() - PLAY_INTERVAL  # play right away on start
play_count = 0

while True:
    now = time.monotonic()
    if now - last_play >= PLAY_INTERVAL and not audio.playing:
        last_play = now
        play_count += 1
        print("playing", play_count)
        # Re-open the file to restart the decoder from the beginning
        mp3.file = open(SOUND_FILE, "rb")
        audio.play(mp3)

    # other non-blocking work can go here
