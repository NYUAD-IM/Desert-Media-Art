# photocell.py

# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT 
#
# Modified by Michael Ang for Desert Media Art
# https://desert.nyuadim.com

import time
import board
from analogio import AnalogIn

potentiometer = AnalogIn(board.A1)  # potentiometer connected to A1, power & ground

darkThreshold = 32000
brightThreshold = 45000

while True:

    brightness = potentiometer.value
    
    print((brightness,))      # Display value

    if (brightness > brightThreshold):
        print('bright')
    if (brightness < darkThreshold):
        print('dark')
        
    time.sleep(0.25)                   # Wait a bit before checking all again
    
