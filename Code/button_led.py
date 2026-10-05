# SPDX-FileCopyrightText: 2026 Michael Ang with Claude Code
#
# SPDX-License-Identifier: MIT

print("button_led")

# Turn the onboard red LED on while the external button is pressed.
# Wire a push button between the "Btn" terminal and the "G" terminal.

import board
import digitalio

# The Btn terminal is not powered through EXTERNAL_POWER, so the button
# works without enabling it. We use the chip's internal pull-up: the pin
# reads True when the button is open and False when it is pressed.
button = digitalio.DigitalInOut(board.EXTERNAL_BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Press the external button to turn on the builtin LED.")
while True:
    led.value = not button.value
