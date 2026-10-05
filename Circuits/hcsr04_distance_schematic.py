# /// script
# dependencies = ["schemdraw", "matplotlib"]
# ///
"""HC-SR04 ultrasonic sensor wired to the Feather RP2040 Prop-Maker.

Regenerate the diagram (writes hcsr04_distance_schematic.svg and .png here):

    uv run hcsr04_distance_schematic.py
"""
from pathlib import Path

import schemdraw
schemdraw.use("matplotlib")
import schemdraw.elements as elm

OUT = str(Path(__file__).with_name("hcsr04_distance_schematic"))

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=12, lw=1.5)

    sensor = elm.Ic(
        pins=[
            elm.IcPin(name="VCC", side="bottom", anchorname="vcc"),
            elm.IcPin(name="Trig", side="bottom", anchorname="trig"),
            elm.IcPin(name="Echo", side="bottom", anchorname="echo"),
            elm.IcPin(name="GND", side="bottom", anchorname="gnd"),
        ],
        size=(5.5, 2), pinspacing=1.5, edgepadH=0.2,
        label="HC-SR04\nUltrasonic sensor",
    ).at((0, 9))
    d += sensor

    # Echo -> R1 -> junction -> R2 -> ground (divider: 5V echo -> ~2.5V)
    d += elm.Line().at(sensor.echo).down(1.5)
    d += elm.Resistor().down().label("R1\n10kΩ", loc="bottom")
    d += elm.Dot()
    junction = d.here
    d += elm.Resistor().down().label("R2\n10kΩ", loc="bottom")
    d += elm.Ground()
    ground_y = d.here[1]

    # Feather box and its pin heights: D5 high, D6 at the divider midpoint
    FX, W = 13.0, 5.5
    y_d5 = sensor.trig[1] - 0.9
    y_d6 = junction[1]
    y_gnd = ground_y - 1.0
    y_usb = ground_y - 2.0
    top, bottom = y_d5 + 1.0, y_usb - 1.0
    for a, b in [((FX, bottom), (FX + W, bottom)), ((FX + W, bottom), (FX + W, top)),
                 ((FX + W, top), (FX, top)), ((FX, top), (FX, bottom))]:
        d += elm.Line().at(a).to(b)
    d += elm.Label().at((FX + W / 2, (top + bottom) / 2 + 0.2)).label(
        "Feather RP2040\nProp-Maker", fontsize=13)
    for name, y in [("D5", y_d5), ("D6", y_d6), ("GND", y_gnd), ("USB (5V)", y_usb)]:
        d += elm.Label().at((FX + 0.2, y)).label(name, halign="left", valign="center")

    # Wires (D5/D6 enter the box edge; "|-" = vertical then horizontal)
    d += elm.Wire("|-").at(sensor.trig).to((FX, y_d5))
    d += elm.Line().at(junction).to((FX, y_d6))
    d += elm.Wire("|-").at(sensor.gnd).to((FX, y_gnd))
    d += elm.Wire("|-").at(sensor.vcc).to((FX, y_usb))

    d += elm.Label().at((6.0, y_d5 + 0.3)).label("trigger (3.3V logic out)", halign="left", fontsize=10)
    d += elm.Label().at((3.5, y_d6 + 0.3)).label("echo, divided to ~2.5V", halign="left", fontsize=10)

    d.save(OUT + ".svg", transparent=False)
    d.save(OUT + ".png", dpi=150, transparent=False)
