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
        d.add(elm.Label().at((x, y)).label(s, halign=ha, valign=va, fontsize=size))

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
    r = d.add(elm.Resistor().at(node).down().label("Resistor", loc="bottom"))
    d.add(elm.Ground().at(r.end))
    wire(node, (13, node[1])); wire((13, node[1]), (13, y)); wire((13, y), lpin("A1", y))

    # ---- D24: touch pad -------------------------------------------------------
    y = -14.5
    wire(lpin("D24", y), (10, y))
    d.add(elm.Dot().at((10, y)))
    wire((10, y), (10, y + 1.0)); d.add(elm.Dot(open=True).at((10, y + 1.0)))
    text(10.4, y + 1.0, "Touch pad (foil / wire)", 10)
    used_by(9.6, y + 0.4, ["touch.py"], "right")
    r = d.add(elm.Resistor().at((10, y)).down().label("1MΩ", loc="bottom"))
    d.add(elm.Ground().at(r.end))

    # ---- D5 / D6: HC-SR04 -----------------------------------------------------
    sx = {"VCC": 0.8, "Trig": 2.0, "Echo": 3.2, "GND": 4.4}
    box(0, -27.0, 5.2, -24.8)
    text(2.6, -25.4, "HC-SR04", 11, "center")
    used_by(0.1, -23.0, ["hcsr04_distance.py"])
    for n, x in sx.items():
        text(x, -26.5, n, 10, "center"); wire((x, -27.0), (x, -27.4))
    wire((sx["Echo"], -27.4), (sx["Echo"], -28.4))
    r1 = d.add(elm.Resistor().at((sx["Echo"], -28.4)).down().label("10kΩ", loc="bottom"))
    d.add(elm.Dot().at(r1.end)); j = r1.end
    r2 = d.add(elm.Resistor().at(j).down().label("10kΩ", loc="bottom"))
    d.add(elm.Ground().at(r2.end))
    y_d5 = -27.9
    wire((sx["Trig"], -27.4), (sx["Trig"], y_d5)); wire((sx["Trig"], y_d5), lpin("D5", y_d5))
    wire(j, lpin("D6", j[1]))
    wire((sx["VCC"], -27.4), (sx["VCC"], -33.2)); d.add(elm.Dot(open=True).at((sx["VCC"], -33.2)))
    text(sx["VCC"] + 0.3, -33.2, "USB 5V pin", 10)
    wire((sx["GND"], -27.4), (sx["GND"], -29.4)); d.add(elm.Ground().at((sx["GND"], -29.4)))

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
            if kind == "5v":
                wire((CX, y), (CX - 0.8, y)); d.add(elm.Vdd().at((CX - 0.8, y)).label("5V", loc="top"))
            elif kind == "3v3":
                wire((CX, y), (CX - 0.8, y)); d.add(elm.Vdd().at((CX - 0.8, y)).label("3V3", loc="top"))
            elif kind == "gnd":
                wire((CX, y), (CX - 0.8, y)); d.add(elm.Ground().at((CX - 0.8, y)))

    # Terminal block: Neo, G, 5V, Btn, speaker +, speaker -
    y_neo, y_tg, y_t5, y_btn, y_sp, y_sm = -1.5, -3.5, -5.5, -7.5, -9.5, -11.0
    connector("Terminal block", 0.0, -12.5,
              [("Neo", y_neo, "sig"), ("G", y_tg, "gnd"), ("5V", y_t5, "5v"),
               ("Btn", y_btn, "sig"), ("+", y_sp, "sig"), ("-", y_sm, "sig")])
    # Servo header: Sig, V+, G
    y_sig, y_sv, y_sg = -17.0, -18.8, -20.6
    connector("Servo header", -15.0, -22.0,
              [("Sig", y_sig, "sig"), ("V+", y_sv, "5v"), ("G", y_sg, "gnd")])
    # STEMMA QT: GND, 3V3, SDA, SCL
    y_qg, y_q3, y_qsda, y_qscl = -24.0, -25.6, -27.2, -28.8
    connector("STEMMA QT", -22.8, -30.0,
              [("GND", y_qg, "gnd"), ("3V3", y_q3, "3v3"),
               ("SDA", y_qsda, "sig"), ("SCL", y_qscl, "sig")])

    # Plain wires from the Feather pins to the connector blocks
    for name, y in [("EXTERNAL_NEOPIXELS", y_neo), ("EXTERNAL_BUTTON", y_btn),
                    ("AMP +", y_sp), ("AMP -", y_sm), ("EXTERNAL_SERVO", y_sig),
                    ("SDA", y_qsda), ("SCL", y_qscl)]:
        wire(feather_pin(name, y), (CX, y))

    # ---- External parts, wired to the connector blocks -------------------------
    # NeoPixel ring / strip: Neo, G, 5V
    box(tx, -0.6, tx + 6.5, -6.4)
    text(tx + 4.4, -3.5, "NeoPixel\nRing or strip", 11, "center")
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

    # VL53L1X on a STEMMA QT cable
    box(tx, -23.4, tx + 6.5, -29.4)
    text(tx + 4.4, -26.4, "VL53L1X", 11, "center")
    for n, y in (("GND", y_qg), ("3V3", y_q3), ("SDA", y_qsda), ("SCL", y_qscl)):
        wire((CR, y), (tx, y)); text(tx + 0.2, y, n, 9)
    used_by(tx + 6.9, -24.2, ["tof_distance.py"])

    # Pin names inside the connector blocks, next to the wires to the parts
    for y, name in [(y_neo, "Neo"), (y_tg, "G"), (y_t5, "5V"), (y_btn, "Btn"),
                    (y_sp, "+"), (y_sm, "-"),
                    (y_sig, "Sig"), (y_sv, "V+"), (y_sg, "G"),
                    (y_qg, "GND"), (y_q3, "3V3"), (y_qsda, "SDA"), (y_qscl, "SCL")]:
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
