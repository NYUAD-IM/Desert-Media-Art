# =============================================================================
# Palette Throb  -  Adafruit Feather RP2040 Prop-Maker
# =============================================================================
#
# What it does:
#   The NeoPixel gently "throbs" (breathes) in the currently selected color.
#   Pressing the external button smoothly rotates the hue to the next color,
#   which sits almost opposite on the color wheel -- so every press is a big,
#   dramatic color change.
#
# Controls:
#   - Button on the "Btn" terminal: advance to the next color.
#   - Serial console: SPACE advances the color; "r" or Ctrl-D reloads the
#     program (useful when auto-reload has been locked off).
#
# Hardware:
#   - Onboard NeoPixel (board.NEOPIXEL) by default, or an external strip on
#     the screw terminals (set USE_EXTERNAL = True; NUM_PIXELS = strip length).
#   - Momentary button wired between the "Btn" terminal (board.EXTERNAL_BUTTON,
#     GPIO19) and the "G" ground terminal. Uses the chip's internal pull-up,
#     so no external resistor: button open = HIGH, pressed = LOW (active-low).
#   - board.EXTERNAL_POWER (GPIO23) gates the screw-terminal 5V + amp; it's
#     enabled only when USE_EXTERNAL is True. The Btn terminal is NOT gated by
#     it, so the button works either way.
#
# How it works:
#   - Fully non-blocking: no time.sleep(). Each pass through the main loop reads
#     the button and the serial console and updates the LED from the clock, so
#     input is picked up instantly and other work can share the loop.
#   - All timing uses time.monotonic_ns() (integer nanoseconds), NOT
#     time.monotonic(). Floats on most boards carry only ~22 bits of precision,
#     so monotonic() loses millisecond accuracy after roughly 1.165 hours of
#     uptime -- a piece left running for days would visibly stair-step.
#   - Colors live in HSV. The "throb" modulates the value (V) with a cosine
#     between THROB_MIN and full over THROB_PERIOD seconds, so the color pulses
#     without ever changing hue.
#   - The palette is generated, not hand-picked: NUM_COLORS hues spread evenly
#     around the wheel, but VISITED in circle-of-fifths order -- each step is
#     HUE_STEP/NUM_COLORS of the wheel (~half, i.e. near-complementary). Like
#     the musical circle of fifths, HUE_STEP is coprime with NUM_COLORS, so all
#     hues are used exactly once before the sequence repeats.
#   - A button press does not change the color immediately. The ease is
#     SCHEDULED so its midpoint lands on the next throb trough (the dim
#     "downbeat"), so the hue swings while the LED is dark and blooms back up
#     already on the new color -- no smearing across bright hues. The wait is
#     up to one THROB_PERIOD; the press itself is still registered instantly.
#   - The ease runs over TRANSITION_DUR seconds, hue taking the short way
#     around the wheel, shaped by an ease-in/out curve. Pressing again while
#     one is pending or running just re-targets and re-schedules to the next
#     trough, starting from whatever is displayed at that moment.
#   - BRIGHTNESS is the master ceiling, kept low so colors stay saturated.
#
# Tuning:
#   NUM_COLORS     - how many hues in the cycle.
#   HUE_STEP       - wheel step per press = HUE_STEP/NUM_COLORS. Keep it coprime
#                    with NUM_COLORS and near NUM_COLORS/2 for complementary
#                    jumps (e.g. 15 colors -> 7 or 8).
#   HUE_START      - hue (0..1) of the first color (0.0 red, 0.08 orange...).
#   SATURATION     - color purity, 0..1 (1.0 = fully vivid).
#   THROB_PERIOD   - seconds per breath (larger = slower throb).
#   THROB_MIN      - dimmest point of the throb (fraction of full value).
#   TRANSITION_DUR - seconds to ease hue to the next color.
#   BRIGHTNESS     - overall level; keep low for saturated color.
#
# Built iteratively with Claude Code (Opus 4.8) on 2026-09-15.
# =============================================================================

import time
import math
import board
import digitalio
import neopixel
import supervisor
import sys

# ---- Config -------------------------------------------------
USE_EXTERNAL   = False   # False = onboard pixel, True = screw-terminal strip
NUM_PIXELS     = 1
BRIGHTNESS     = 0.3     # master ceiling; keep low so color reads as color
SATURATION     = 1.0     # color purity, 0..1 (1.0 = fully vivid)

NUM_COLORS     = 15      # hues in the cycle
HUE_STEP       = 7       # wheel step per press = HUE_STEP/NUM_COLORS (~half)
HUE_START      = 0.08    # hue of the first color (0.08 ~ orange)

THROB_PERIOD   = 2.5     # seconds per breath
THROB_MIN      = 0.20    # dimmest point of the throb (fraction of full value)
TRANSITION_DUR = 0.5     # seconds to ease hue to the next color
# -------------------------------------------------------------

# Timing runs in integer nanoseconds -- see the precision note in the header.
NS_PER_SEC        = 1000000000
THROB_PERIOD_NS   = int(THROB_PERIOD * NS_PER_SEC)
TRANSITION_DUR_NS = int(TRANSITION_DUR * NS_PER_SEC)


def hsv_to_rgb(h, s, v):
    """h,s,v in 0..1 -> (r, g, b) each in 0..255."""
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i %= 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return (int(r * 255), int(g * 255), int(b * 255))


def lerp(a, b, t):
    return a + (b - a) * t


def hue_lerp(a, b, t):
    """Interpolate hue the short way around the 0..1 wheel."""
    d = b - a
    if d > 0.5:
        d -= 1.0
    elif d < -0.5:
        d += 1.0
    return (a + d * t) % 1.0


def ease_in_out(t):
    """Cubic ease-in/out: slow start, slow finish."""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - ((-2 * t + 2) ** 3) / 2


# Circle-of-fifths palette: NUM_COLORS evenly spaced hues, visited in jumps of
# HUE_STEP/NUM_COLORS so consecutive colors are almost complementary.
PALETTE_HSV = [
    ((HUE_START + (i * HUE_STEP) / NUM_COLORS) % 1.0, SATURATION, 1.0)
    for i in range(NUM_COLORS)
]

# Prop-Maker external power gates the screw-terminal output + amp
ext_power = digitalio.DigitalInOut(board.EXTERNAL_POWER)
ext_power.direction = digitalio.Direction.OUTPUT
ext_power.value = USE_EXTERNAL

pin = board.EXTERNAL_NEOPIXELS if USE_EXTERNAL else board.NEOPIXEL
if not USE_EXTERNAL:
    NUM_PIXELS = 1

pixel = neopixel.NeoPixel(pin, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=True)

# External button on the Btn terminal (GPIO19), wired Btn -> button -> G
button = digitalio.DigitalInOut(board.EXTERNAL_BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


class ColorThrob:
    """Throbs in the current HSV color; next_color() eases to the next one."""

    def __init__(self, pixel, palette_hsv):
        self.pixel = pixel
        self.palette = palette_hsv
        self.index = 0
        self.cur = palette_hsv[0]        # (h, s, v) shown right now (pre-throb)
        self.frm = self.cur
        self.to = self.cur
        self.transitioning = False
        self.trans_start = 0

    def next_color(self):
        self.index = (self.index + 1) % len(self.palette)
        self.frm = self.cur              # ease from whatever is displayed now
        self.to = self.palette[self.index]
        # Schedule the ease so its midpoint lands on the next throb trough
        # (phase 0 = dimmest), so the hue swings while the LED is dark.
        now = time.monotonic_ns()
        half = TRANSITION_DUR_NS // 2
        # Integer ceiling division: first multiple of THROB_PERIOD_NS at or
        # after (now + half).
        trough = ((now + half + THROB_PERIOD_NS - 1) // THROB_PERIOD_NS) * THROB_PERIOD_NS
        self.trans_start = trough - half
        self.transitioning = True
        return self.index

    def update(self):
        now = time.monotonic_ns()

        if self.transitioning:
            te = (now - self.trans_start) / TRANSITION_DUR_NS
            if te <= 0.0:
                k = 0.0                  # scheduled but not started: hold old color
            elif te >= 1.0:
                k = 1.0
                self.transitioning = False
            else:
                k = ease_in_out(te)
            h = hue_lerp(self.frm[0], self.to[0], k)
            s = lerp(self.frm[1], self.to[1], k)
            v = lerp(self.frm[2], self.to[2], k)
            self.cur = (h, s, v)
        else:
            self.cur = self.to

        # Throb: modulate value with a cosine between THROB_MIN and 1.0
        phase = (now % THROB_PERIOD_NS) / THROB_PERIOD_NS
        env = 0.5 - 0.5 * math.cos(2 * math.pi * phase)      # 0..1
        scale = THROB_MIN + (1.0 - THROB_MIN) * env

        h, s, v = self.cur
        self.pixel.fill(hsv_to_rgb(h, s, v * scale))


class Button:
    """Non-blocking debounced button. read() returns True once per press."""

    def __init__(self, dio, debounce=0.02):
        self.dio = dio
        self.debounce_ns = int(debounce * NS_PER_SEC)
        self.stable = dio.value
        self._last = dio.value
        self._changed_at = time.monotonic_ns()

    def read(self):
        now = time.monotonic_ns()
        level = self.dio.value
        if level != self._last:
            self._last = level
            self._changed_at = now
        elif now - self._changed_at >= self.debounce_ns and level != self.stable:
            self.stable = level
            if level is False:          # HIGH -> LOW = press (active-low)
                return True
        return False

def check_keys():
    """Non-blocking: consume any pending serial input and act on it."""
    while supervisor.runtime.serial_bytes_available:
        key = sys.stdin.read(1)
        if key in ("r", "R", "\x04"):   # "r", or Ctrl-D (EOT), as at the REPL
            print("reloading...")
            supervisor.reload()
        elif key == " ":
            i = throb.next_color()      # same action as the button
            print("keyboard -> color", i + 1)


throb = ColorThrob(pixel, PALETTE_HSV)
btn = Button(button)
print("Ready. Press the button to jump ~half the color wheel.")

print("Send space in serial terminal to change color")
print("Send 'r' or Ctrl-D in serial terminal to reload code")

# ---- Main loop: throb + button, nothing blocks ---------------
while True:
    # Defined in code.py
    check_keys()

    if btn.read():
        i = throb.next_color()
        h = PALETTE_HSV[i][0]
        print("color {}/{}: hue {:3.0f} deg  rgb {}".format(
            i + 1, NUM_COLORS, h * 360, hsv_to_rgb(h, SATURATION, 1.0)))

    throb.update()
