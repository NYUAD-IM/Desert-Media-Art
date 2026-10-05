# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

'''RP2040 Prop-Maker Feather Example'''
print("propmaker_accel")


import time
import board
import audiocore
import audiobusio
import audiofilters
import audiomixer
import synthio
import pwmio
from digitalio import DigitalInOut, Direction, Pull
import neopixel
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_motor import servo
import adafruit_lis3dh

# enable external power pin
# provides power to the external components
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# i2s playback
sample_rate = 22050
# Sound credit: see sounds/ATTRIBUTION.txt
wave_file = open("sounds/strings.wav", "rb")
wave = audiocore.WaveFile(wave_file)
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)
mixer = audiomixer.Mixer(voice_count=1, sample_rate=sample_rate, channel_count=1,
                         bits_per_sample=16, samples_signed=True)

# Effects are chained as WAV -> low-pass -> distortion -> mixer -> I2S.
# Both effects start fully dry so the board sounds unchanged while Y is level.
low_pass_biquad = synthio.Biquad(
    synthio.FilterMode.LOW_PASS,
    10000,
    Q=0.707,
)
low_pass = audiofilters.Filter(
    filter=low_pass_biquad,
    mix=0.0,
    buffer_size=1024,
    sample_rate=sample_rate,
    channel_count=1,
)
distortion = audiofilters.Distortion(
    drive=0.0,
    mode=audiofilters.DistortionMode.CLIP,
    soft_clip=True,
    mix=0.0,
    buffer_size=1024,
    sample_rate=sample_rate,
    channel_count=1,
)

low_pass.play(wave, loop=True)
distortion.play(low_pass)
mixer.voice[0].play(distortion)
audio.play(mixer)
mixer.voice[0].level = 0.5

# servo control
pwm = pwmio.PWMOut(board.EXTERNAL_SERVO, duty_cycle=2 ** 15, frequency=50)
prop_servo = servo.Servo(pwm)
angle = 0
angle_plus = True

# external button
switch = DigitalInOut(board.EXTERNAL_BUTTON)
switch.direction = Direction.INPUT
switch.pull = Pull.UP
switch_state = False

# external neopixels
num_pixels = 30
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, num_pixels)
pixels.brightness = 0.3
rainbow = Rainbow(pixels, speed=0.05, period=2)

# onboard LIS3DH
i2c = board.I2C()
int1 = DigitalInOut(board.ACCELEROMETER_INTERRUPT)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

def volume_for_x(x):
    '''Map X tilt in Gs to the mixer's 0.0 to 1.0 volume range.'''
    return min(max((x + 1) / 2, 0.0), 1.0)

def effect_levels(y, dead_zone=0.1):
    '''Map negative Y to low-pass and positive Y to distortion.'''
    # Keep a small center dead zone so sensor noise does not color the audio.
    if y < -dead_zone:
        low_pass_level = min((-y - dead_zone) / (1.0 - dead_zone), 1.0)
        return round(low_pass_level, 3), 0.0
    if y > dead_zone:
        distortion_level = min((y - dead_zone) / (1.0 - dead_zone), 1.0)
        return 0.0, round(distortion_level, 3)
    return 0.0, 0.0

while True:
    # rainbow animation on external neopixels
    rainbow.animate()
    # read and print LIS3DH values
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    # print(f"x = {x:.3f} G, y = {y:.3f} G, z = {z:.3f} G")

    # Set volume based on rotation of the board (x-axis of LIS3DH)
    volume = volume_for_x(x)
    # print(volume)
    mixer.voice[0].level = volume

    low_pass_level, distortion_level = effect_levels(y)

    # Negative Y blends in the filter while sweeping its cutoff from 10 kHz
    # down to 300 Hz. Positive Y blends in progressively stronger distortion.
    low_pass.mix = low_pass_level
    low_pass_biquad.frequency = 10000 - low_pass_level * 9700
    distortion.mix = distortion_level
    distortion.drive = distortion_level

    # move servo back and forth
    prop_servo.angle = angle
    if angle_plus:
        angle += 5
    else:
        angle -= 5
    if angle == 180:
        angle_plus = False
    elif angle == 0:
        angle_plus = True
    # if the switched is pressed, turn off power to external components
    if not switch.value and switch_state is False:
        external_power.value = False
        switch_state = True
    if switch.value and switch_state is True:
        external_power.value = True
        switch_state = False

    time.sleep(0.02)
