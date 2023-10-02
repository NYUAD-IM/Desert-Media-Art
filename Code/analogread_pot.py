# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from analogio import AnalogIn

potentiometer = AnalogIn(board.A1)  # potentiometer connected to A1, Aref & ground

while True:

    print((potentiometer.value,))      # Display value

    time.sleep(0.25)                   # Wait a bit before checking all again
