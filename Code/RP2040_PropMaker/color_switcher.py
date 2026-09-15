# =============================================================================
# Palette Throb  -  Adafruit Feather RP2040 Prop-Maker
# =============================================================================
#
# What it does:
#   The NeoPixel gently "throbs" (breathes) in the currently selected color.
#   Pressing the external button smoothly rotates the hue to the next color in
#   a 15-color palette over 0.5s with an ease-in/out curve.
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
#     the button and updates the LED from time.monotonic(), so a press is picked
#     up instantly and other work can share the loop.
#   - Colors live in HSV. The "throb" modulates the value (V) with a cosine
#     between THROB_MIN and full over THROB_PERIOD seconds, so the color pulses
#     without ever changing hue.
#   - A button press eases from the currently displayed color to the next
#     palette color over TRANSITION_DUR seconds: hue rotates the short way
#     around the wheel while saturation/value cross-fade, all shaped by an
#     ease-in/out curve. Pressing again mid-transition simply starts a new
#     ease from wherever the color is right now.
#   - PALETTE is written in friendly RGB and converted to HSV once at startup.
#   - BRIGHTNESS is the master ceiling, kept low so colors stay saturated
#     instead of washing out toward white.
#
# Tuning:
#   PALETTE        - edit/reorder freely; the count is derived with len().
#   THROB_PERIOD   - seconds per breath (larger = slower throb).
#   THROB_MIN      - dimmest point of the throb (0..1 of full value).
#   TRANSITION_DUR - seconds to ease from one color to the next.
#   BRIGHTNESS     - overall level; keep low for saturated color.
#
# Built iteratively with Claude Code (Opus 4.8) on 2026-09-15.
# =============================================================================

import time
import math
import board
import digitalio
import neopixel

# ---- Config -------------------------------------------------
USE_EXTERNAL   = False   # False = onboard pixel, True = screw-terminal strip
NUM_PIXELS     = 1
BRIGHTNESS     = 0.3     # master ceiling; keep low so color reads as color
THROB_PERIOD   = 2.5     # seconds per breath
THROB_MIN      = 0.20    # dimmest point of the throb (fraction of full value)
TRANSITION_DUR = 0.5     # seconds to ease hue to the next color
# -------------------------------------------------------------

# 15 nice colors, walking around the wheel warm -> cool -> warm
PALETTE = [
    (255,  90,   0),   # orange
    (255, 160,   0),   # amber
    (255, 214,  60),   # gold
    (150, 220,  40),   # lime
    ( 30, 200,  90),   # green
    (  0, 200, 170),   # teal
    (  0, 190, 220),   # cyan
    ( 40, 140, 255),   # sky blue
    ( 60,  80, 230),   # blue
    (110,  70, 220),   # indigo
    (170,  60, 220),   # purple
    (230,  50, 190),   # magenta
    (255,  70, 140),   # pink
    (240,  40,  40),   # red
    (255, 110,  70),   # coral
]


def rgb_to_hsv(r, g, b):
    """r,g,b in 0..255 -> (h, s, v) each in 0..1."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    v = mx
    s = 0.0 if mx == 0 else d / mx
    if d == 0:
        h = 0.0
    elif mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = ((b - r) / d) + 2
    else:
        h = ((r - g) / d) + 4
    return (h / 6.0, s, v)


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


PALETTE_HSV = [rgb_to_hsv(*c) for c in PALETTE]

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
        self.trans_start = 0.0

    def next_color(self):
        self.index = (self.index + 1) % len(self.palette)
        self.frm = self.cur              # ease from whatever is displayed now
        self.to = self.palette[self.index]
        self.trans_start = time.monotonic()
        self.transitioning = True
        return self.index

    def update(self):
        now = time.monotonic()

        if self.transitioning:
            te = (now - self.trans_start) / TRANSITION_DUR
            if te >= 1.0:
                te = 1.0
                self.transitioning = False
            k = ease_in_out(te)
            h = hue_lerp(self.frm[0], self.to[0], k)
            s = lerp(self.frm[1], self.to[1], k)
            v = lerp(self.frm[2], self.to[2], k)
            self.cur = (h, s, v)
        else:
            self.cur = self.to

        # Throb: modulate value with a cosine between THROB_MIN and 1.0
        phase = (now % THROB_PERIOD) / THROB_PERIOD
        env = 0.5 - 0.5 * math.cos(2 * math.pi * phase)      # 0..1
        scale = THROB_MIN + (1.0 - THROB_MIN) * env

        h, s, v = self.cur
        self.pixel.fill(hsv_to_rgb(h, s, v * scale))


class Button:
    """Non-blocking debounced button. read() returns True once per press."""

    def __init__(self, dio, debounce=0.02):
        self.dio = dio
        self.debounce = debounce
        self.stable = dio.value
        self._last = dio.value
        self._changed_at = time.monotonic()

    def read(self):
        now = time.monotonic()
        level = self.dio.value
        if level != self._last:
            self._last = level
            self._changed_at = now
        elif now - self._changed_at >= self.debounce and level != self.stable:
            self.stable = level
            if level is False:          # HIGH -> LOW = press (active-low)
                return True
        return False


throb = ColorThrob(pixel, PALETTE_HSV)
btn = Button(button)
print("Ready. Throbbing on 'orange'. Press the button to shift color.")

# ---- Main loop: throb + button, nothing blocks ---------------
while True:
    if btn.read():
        i = throb.next_color()
        print("color {}/{}: {}".format(i + 1, len(PALETTE), PALETTE[i]))

    throb.update()
