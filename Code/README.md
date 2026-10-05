# Code examples

CircuitPython examples for Desert Media Art, written for the **Adafruit Feather RP2040 Prop-Maker** running **CircuitPython 10.x**.

- Board: https://learn.adafruit.com/adafruit-rp2040-prop-maker-feather
- Download CircuitPython 10.x: https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/

The earlier examples for the Feather M4 Express with the Prop-Maker FeatherWing are in [M4_Express_Legacy](../M4_Express_Legacy). They won't run unchanged on this board.

## Running an example

Copy the example to the `CIRCUITPY` drive and either save it as `code.py` or import it from `code.py` (for example `import neoring`). Examples that use sound or other files expect those files on the drive too, at the paths named in the example.

Every example prints its own file name (without `.py`) when it starts, so you can see in the serial console which file is running.

## Installing libraries

Most examples use only modules built into CircuitPython. The others need libraries from the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries) (for 10.x). Copy the library file or folder into `CIRCUITPY/lib`, or install with [circup](https://github.com/adafruit/circup), which also installs dependencies:

```
circup install adafruit_lis3dh
```

## Examples

| Example | What it does | Libraries needed (in `lib`) |
|---|---|---|
| `button_led.py` | Onboard red LED on while the button on the Btn terminal is pressed | none |
| `analogin_demo.py` | Read a potentiometer and photoresistor on A0, A1 | none |
| `analogread_pot.py` | Read a potentiometer on A0 | none |
| `photocell_demo.py` | Read a photocell on A1, normalized to 0-1, LED on when dark | none |
| `touch.py` | Capacitive touch on D24 (needs a 1M ohm resistor to ground) | none |
| `servo_standard.py` | Sweep a servo on the servo terminal | `adafruit_motor` |
| `neoring.py` | Rainbow on a NeoPixel ring (external NeoPixel terminal) | `neopixel` |
| `neostrip_rgbw.py` | RGBW NeoPixel strip demo (`code.py` loads this one) | `neopixel` |
| `demo_mp3.py` | Play an MP3 every 10 seconds on the speaker | none |
| `mp3example.py` | Play MP3s in order, button on the Btn terminal to continue | none |
| `mp3_button.py` | Play MP3s from `/mang`, push button on the Btn terminal to continue | none |
| `mp3tap.py` | Play an MP3 each time you tap the board | `adafruit_lis3dh` |
| `hcsr04_distance.py` | HC-SR04 ultrasonic distance on D5 / D6 | `adafruit_hcsr04` |
| `tof_distance.py` | VL53L1X distance sensor over I2C, onboard NeoPixel shows range | `adafruit_vl53l1x` |

Built-in modules (no install needed) include `board`, `digitalio`, `analogio`, `pwmio`, `touchio`, `audiobusio`, `audiomp3`, `rainbowio` and `synthio`.

## Extras

Longer or more advanced examples are in [Extras](Extras). They use the same pins and wiring.

| Example | What it does | Libraries needed (in `lib`) |
|---|---|---|
| `Extras/propmaker_accel.py` | Everything at once: audio effects, servo, NeoPixels, accelerometer (plays `sounds/strings.wav`, so copy the `sounds` folder to the drive) | `adafruit_lis3dh`, `adafruit_motor`, `adafruit_led_animation`, `neopixel` |
| `Extras/lock_reload.py` | Stop macOS from triggering auto-reloads (see `Extras/blog-post-autoreload-macos.html`) | none |

## Prop-Maker pin names

These names are specific to this board.

| Name | Use |
|---|---|
| `board.EXTERNAL_POWER` | Set high to power the speaker amp and the external NeoPixel and servo terminals |
| `board.I2S_BIT_CLOCK`, `board.I2S_WORD_SELECT`, `board.I2S_DATA` | I2S audio to the speaker amp |
| `board.EXTERNAL_NEOPIXELS` | External NeoPixel terminal |
| `board.EXTERNAL_SERVO` | Servo terminal |
| `board.EXTERNAL_BUTTON` | Button terminal (wire a button to ground) |
| `board.ACCELEROMETER_INTERRUPT` | Interrupt from the onboard accelerometer |
| `board.NEOPIXEL` | Onboard NeoPixel |
| `board.LED` | Onboard red LED |

Free pins for your own sensors: A0 to A3 (the only analog inputs), D5, D6, D9, D24 and D25.

## Wiring

The examples use different pins, so all of them can be connected at once. See the combined diagram [Circuits/wiring_all_examples.png](../Circuits/wiring_all_examples.png) (pin names on the Feather, which example uses each part). The HC-SR04 divider has its own schematic: [Circuits/hcsr04_distance_schematic.png](../Circuits/hcsr04_distance_schematic.png).

## Sound credits

See [sounds/ATTRIBUTION.txt](sounds/ATTRIBUTION.txt).
