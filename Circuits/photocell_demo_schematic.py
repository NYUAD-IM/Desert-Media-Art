# /// script
# dependencies = ["schemdraw", "matplotlib"]
# ///
"""Photocell voltage divider read on A1.

Regenerate the diagram (writes photocell_demo_schematic.svg and .png here):

    uv run photocell_demo_schematic.py
"""
from pathlib import Path

import schemdraw
schemdraw.use("matplotlib")
import schemdraw.elements as elm

OUT = str(Path(__file__).with_name("photocell_demo_schematic"))

with schemdraw.Drawing(show=False) as d:
    d.config(unit=3)
    d += elm.Dot(open=True).label('3.3V', 'top')
    ldr = elm.Photoresistor().down()
    d += ldr
    d += elm.Label().at((ldr.center[0] + 1.6, ldr.center[1])).label('Photocell')
    d += elm.Dot()
    d.push()
    d += elm.Line().right().length(1.5)
    d += elm.Dot(open=True).label('to A1', 'right')
    d.pop()
    r = elm.Resistor().down()
    d += r
    d += elm.Label().at((r.center[0] + 1.0, r.center[1])).label('10kΩ')
    d += elm.Ground()
    d.save(OUT + ".svg", transparent=False)
    d.save(OUT + ".png", dpi=150, transparent=False)
