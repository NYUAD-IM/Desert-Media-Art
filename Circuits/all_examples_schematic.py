# /// script
# dependencies = ["schemdraw", "matplotlib"]
# ///
"""Wiring for all the examples in Code/ on the Feather RP2040 Prop-Maker.

Regenerate the diagram (writes all_examples_schematic.svg and .png here):

    uv run all_examples_schematic.py
"""
from pathlib import Path

import schemdraw
schemdraw.use("matplotlib")
import schemdraw.elements as elm

OUT = str(Path(__file__).with_name("all_examples_schematic"))

FX, FW = 17.0, 8.0            # Feather box left edge and width
TOP, BOTTOM = 4.0, -40.5       # Feather box top and bottom
RX = FX + FW                   # right edge of the Feather box


with schemdraw.Drawing(show=False) as d:
    d.config(unit=2.0, fontsize=11, lw=1.4)

    def text(x, y, s, size=11, ha="left", va="center"):
        # .right(): otherwise the label inherits the previous element's direction,
        # which shifts its position and misaligns labels in a row.
        d.add(elm.Label().at((x, y)).right().label(s, halign=ha, valign=va, fontsize=size))

    def wire(a, b):
        d.add(elm.Line().at(a).to(b))

    def box(x0, y0, x1, y1):
        wire((x0, y0), (x1, y0)); wire((x1, y0), (x1, y1))
        wire((x1, y1), (x0, y1)); wire((x0, y1), (x0, y0))

    def used_by(x, y, lines, ha="left"):
        for i, line in enumerate(["Used by:"] + lines):
            text(x, y - i * 0.65, line, 8, ha)

    def lpin(name, y):  # pin on the Feather's left edge
        text(FX + 0.2, y, name)
        return (FX, y)

    def rpin(name, y):  # terminal on the Feather's right edge
        text(RX - 0.2, y, name, ha="right")
        return (RX, y)

    # ---- Feather -----------------------------------------------------------
    box(FX, BOTTOM, RX, TOP)
    text(FX + FW / 2, TOP + 0.8, "Feather RP2040 Prop-Maker", 13, "center")
    text(FX + FW / 2, TOP + 2.4, "Desert Media Art - All Examples Schematic", 20, "center")
    text(FX + 0.2, TOP - 0.9, "Header pins", 10)

    # ---- A0: potentiometer ---------------------------------------------------
    y = 0.0
    wire(lpin("A0", y), (13, y)); wire((13, y), (13, y))
    d.add(elm.Vdd().at((10, y + 2.2)).label("3V3", loc="top"))
    pot = d.add(elm.Potentiometer().at((10, y + 2.2)).down())
    text(9.6, y + 1.2, "Potentiometer", ha="right")
    used_by(9.6, y + 0.2, ["analogin_demo.py", "analogread_pot.py"], "right")
    d.add(elm.Ground().at(pot.end))
    wire(pot.tap, (13, pot.tap[1]))
    wire((13, pot.tap[1]), (13, y))

    # ---- A1: photoresistor + resistor ---------------------------------------
    y = -7.0
    d.add(elm.Vdd().at((10, y + 2.2)).label("3V3", loc="top"))
    ldr = d.add(elm.Photoresistor().at((10, y + 2.2)).down().label("Photoresistor", loc="bottom"))
    d.add(elm.Dot().at(ldr.end))
    used_by(9.6, y + 0.4, ["analogin_demo.py", "photocell_demo.py"], "right")
    node = ldr.end
    r = d.add(elm.Resistor().at(node).down().label("10kΩ", loc="bottom"))  # value from photocell_demo.py
    d.add(elm.Ground().at(r.end))
    wire(node, lpin("A1", node[1]))

    # ---- D24: touch pad -------------------------------------------------------
    y = -14.5
    wire(lpin("D24", y), (10, y))
    d.add(elm.Dot().at((10, y)))
    wire((10, y), (10, y + 1.0)); d.add(elm.Dot(open=True).at((10, y + 1.0)))
    text(10.4, y + 1.0, "Touch pad (foil / wire)", 10)
    used_by(9.6, y + 0.4, ["touch.py"], "right")
    r = d.add(elm.Resistor().at((10, y)).down().label("1MΩ", loc="bottom"))
    d.add(elm.Ground().at(r.end))

    # ---- SDA / SCL: VL53L1X on STEMMA QT (a sensor, so on the input side) ----
    LCX, LCR = 8.5, 13.0           # STEMMA QT block, left of the Feather
    # Rows in the connector's physical pin order: GND, V+ (3V3), SDA, SCL.
    QT_ROWS = (("GND", -20.8), ("3V3", -22.4), ("SDA", -24.0), ("SCL", -25.6))
    y_qg, y_q3, y_qsda, y_qscl = (yy for _, yy in QT_ROWS)
    box(LCX, -26.6, LCR, -19.2)
    text((LCX + LCR) / 2, -19.8, "STEMMA QT", 10, "center")
    for name, yy in QT_ROWS:
        text(LCX + 0.3, yy, name, 10)           # part side
        text(LCR - 0.3, yy, name, 10, "right")  # Feather side
    # Ground (pointing down) sits above 3V3 (pointing up): stagger the stubs so they don't meet.
    wire((LCR, y_qg), (LCR + 0.8, y_qg)); d.add(elm.Ground().at((LCR + 0.8, y_qg)))
    wire((LCR, y_q3), (LCR + 2.0, y_q3)); d.add(elm.Vdd().at((LCR + 2.0, y_q3)).label("3V3", loc="top"))
    wire((LCR, y_qsda), lpin("SDA", y_qsda))
    wire((LCR, y_qscl), lpin("SCL", y_qscl))
    box(0, -26.2, 5.5, -19.6)
    text(1.6, -22.9, "VL53L1X", 11, "center")
    for name, yy in QT_ROWS:
        text(5.3, yy, name, 9, "right"); wire((5.5, yy), (LCX, yy))
    used_by(0.1, -18.2, ["tof_distance.py"])

    # ---- D5 / D6: HC-SR04 -----------------------------------------------------
    # Trig is an output and Echo an input: a mixed-direction part, kept on the left.
    sx = {"VCC": 0.8, "Trig": 2.0, "Echo": 3.2, "GND": 5.0}
    box(0, -32.0, 5.8, -29.4)
    text(3.0, -30.0, "HC-SR04", 11, "center")
    used_by(6.2, -29.9, ["hcsr04_distance.py"])
    text(sx["VCC"], -30.0, "VCC", 10, "center")
    wire((sx["VCC"], -29.4), (sx["VCC"], -28.8))
    d.add(elm.Vdd().at((sx["VCC"], -28.8)).label("USB 5V", loc="top"))
    for n in ("Trig", "Echo", "GND"):
        x = sx[n]
        text(x, -31.5, n, 10, "center")
        wire((x, -32.0), (x, -32.4))
    wire((sx["Echo"], -32.4), (sx["Echo"], -33.4))
    r1 = d.add(elm.Resistor().at((sx["Echo"], -33.4)).down().label("10kΩ", loc="bottom"))
    d.add(elm.Dot().at(r1.end)); j = r1.end
    r2 = d.add(elm.Resistor().at(j).down().label("10kΩ", loc="bottom"))
    d.add(elm.Ground().at(r2.end))
    y_d5 = -32.9
    wire((sx["Trig"], -32.4), (sx["Trig"], y_d5)); wire((sx["Trig"], y_d5), lpin("D5", y_d5))
    wire(j, lpin("D6", j[1]))
    wire((sx["GND"], -32.4), (sx["GND"], -33.8)); d.add(elm.Ground().at((sx["GND"], -33.8)))

    # ---- Connectors: separate parts wired to the Feather ----------------------
    CX, CW = RX + 4.0, 5.0         # connector blocks, to the right of the Feather
    CR = CX + CW                   # connector right edge
    tx = CR + 3.5                  # external parts

    def feather_pin(name, y):      # signal pin on the Feather's right edge
        text(RX - 0.2, y, name, 9, "right")
        return (RX, y)

    def connector(title, y_top, y_bottom, rows):
        """rows: (name, y, kind) with kind 'sig' (wire to Feather), '5v', 'gnd' or '3v3'"""
        box(CX, y_bottom, CR, y_top)
        text(CX + CW / 2, y_top - 0.6, title, 10, "center")
        for name, y, kind in rows:
            text(CX + 0.3, y, name, 10)
            # Power stubs are longer than ground stubs, so a ground (pointing down)
            # in the row above a supply (pointing up) doesn't run into it.
            if kind in ("5v", "3v3"):
                wire((CX, y), (CX - 2.0, y))
                d.add(elm.Vdd().at((CX - 2.0, y)).label("5V" if kind == "5v" else "3V3", loc="top"))
            elif kind == "gnd":
                wire((CX, y), (CX - 0.8, y)); d.add(elm.Ground().at((CX - 0.8, y)))

    # Rows follow each connector's physical pin order (Adafruit pinout page, top edge down).
    # Terminal block: Neo, G, 5V, Btn, speaker -, speaker +
    y_neo, y_tg, y_t5, y_btn, y_sm, y_sp = -1.5, -3.5, -5.5, -7.5, -9.5, -11.0
    connector("Terminal block", 0.0, -12.5,
              [("Neo", y_neo, "sig"), ("G", y_tg, "gnd"), ("5V", y_t5, "5v"),
               ("Btn", y_btn, "sig"), ("-", y_sm, "sig"), ("+", y_sp, "sig")])
    # Servo header: G, V+, Sig
    y_sg, y_sv, y_sig = -17.0, -18.8, -20.6
    connector("Servo header", -15.0, -22.0,
              [("G", y_sg, "gnd"), ("V+", y_sv, "5v"), ("Sig", y_sig, "sig")])

    # Plain wires from the Feather pins to the connector blocks.
    # EXTERNAL_BUTTON is an input but stays on the right: it is on the terminal block.
    for name, y in [("EXTERNAL_NEOPIXELS", y_neo), ("EXTERNAL_BUTTON", y_btn),
                    ("AMP +", y_sp), ("AMP -", y_sm), ("EXTERNAL_SERVO", y_sig)]:
        wire(feather_pin(name, y), (CX, y))

    # ---- External parts, wired to the connector blocks -------------------------
    # NeoPixel ring / strip: Neo, G, 5V
    box(tx, -0.6, tx + 6.5, -6.4)
    text(tx + 4.4, -3.0, "NeoPixel", 11, "center")
    text(tx + 4.4, -3.9, "Ring or strip", 11, "center")
    for n, y in (("data", y_neo), ("GND", y_tg), ("5V", y_t5)):
        wire((CR, y), (tx, y)); text(tx + 0.2, y, n, 9)
    used_by(tx + 6.9, -1.5, ["neoring.py", "neostrip_rgbw.py", "Extras/propmaker_accel.py"])

    # Push button on Btn, other side to ground
    wire((CR, y_btn), (tx, y_btn))
    bt = d.add(elm.Button().at((tx, y_btn)).right().label("Push button", loc="top"))
    wire(bt.end, (bt.end[0] + 0.6, bt.end[1])); d.add(elm.Ground().at((bt.end[0] + 0.6, bt.end[1])))
    used_by(tx + 6.9, y_btn + 1.3, ["button_led.py", "mp3_button.py", "mp3example.py", "Extras/propmaker_accel.py"])

    # Speaker: + and -
    box(tx, -8.7, tx + 6.5, -12.0)
    text(tx + 4.4, -10.35, "Speaker", 11, "center")
    for n, y in (("+", y_sp), ("-", y_sm)):
        wire((CR, y), (tx, y)); text(tx + 0.2, y, n, 9)
    used_by(tx + 6.9, -10.6, ["demo_mp3.py", "mp3example.py", "mp3_button.py", "mp3tap.py", "Extras/propmaker_accel.py"])

    # Servo: Sig, V+, G
    box(tx, -15.4, tx + 6.5, -21.8)
    text(tx + 4.4, -18.6, "Servo", 11, "center")
    for n, y in (("signal", y_sig), ("V+", y_sv), ("GND", y_sg)):
        wire((CR, y), (tx, y)); text(tx + 0.2, y, n, 9)
    used_by(tx + 6.9, -16.2, ["servo_standard.py", "Extras/propmaker_accel.py"])

    # Pin names inside the connector blocks, next to the wires to the parts
    for y, name in [(y_neo, "Neo"), (y_tg, "G"), (y_t5, "5V"), (y_btn, "Btn"),
                    (y_sp, "+"), (y_sm, "-"),
                    (y_sig, "Sig"), (y_sv, "V+"), (y_sg, "G")]:
        text(CR - 0.3, y, name, 10, "right")

    # ---- Onboard (no wiring) ---------------------------------------------------
    box(RX + 1.0, -38.8, RX + 15.0, -32.0)
    text(RX + 1.4, -33.0, "Onboard, nothing to wire:", 10)
    for i, line in enumerate(["LIS3DH accelerometer: mp3tap.py, Extras/propmaker_accel.py",
                              "Red LED (D13): button_led.py",
                              "NeoPixel (D4): tof_distance.py",
                              "I2S amp (to the speaker terminals): all MP3 examples"]):
        text(RX + 1.4, -34.5 - i * 1.2, line, 9)

    d.save(OUT + ".svg", transparent=False)
    d.save(OUT + ".png", dpi=130, transparent=False)
