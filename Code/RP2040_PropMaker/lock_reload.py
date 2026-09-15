# =============================================================================
# lock_reload.py  -  demonstrating (and stopping) phantom auto-reloads
# =============================================================================
#
# The problem:
#   CircuitPython restarts code.py whenever the CIRCUITPY filesystem is
#   written. On macOS the OS writes to the drive on its own -- updating
#   extended attributes such as com.apple.lastuseddate#PS, which spill into
#   "._" AppleDouble sidecar files on FAT. Merely previewing a file with
#   Quick Look is enough to reboot the board, with no code change at all.
#
# The workaround:
#   Set lock_reload = True to turn auto-reload off, so the board ignores
#   filesystem writes. Reload deliberately instead: press "r" in the serial
#   console, or reset the board.
#
# How to demonstrate it:
#   1. Copy this file to CIRCUITPY as code.py and open a serial console.
#   2. Set lock_reload = False. Watch the uptime counter climb.
#   3. In the Finder, select any file on CIRCUITPY and press space for a
#      Quick Look preview. The uptime resets to 0 and the run reason prints
#      as AUTO_RELOAD -- nothing was edited, but the board restarted.
#   4. Set lock_reload = True and repeat step 3. The counter keeps climbing.
#   5. Press "r" or Ctrl-D in the console to confirm you can still reload
#      on demand.
#
# Built with Claude Code (Opus 5) on 2026-09-15.
# Developed/tested by Michael Ang https://michaelang.com
# =============================================================================
print("lock_reload")

import sys
import time
import supervisor

# ---- Set true to stop macOS metadata writes from restarting the board -----
lock_reload = True
# ----------------------------------------------------------------------------

if lock_reload:
    print("Locking reload")
    supervisor.runtime.autoreload = False
    print("Auto-reload is OFF")
    print("Manually reset after code changes, or send 'r' or Ctrl-D in serial terminal to reload")
else:
    supervisor.runtime.autoreload = True
    print("Auto-reload is ON")
    print("Use MacOS Quick Look preview (spacebar) on a file in CIRCUITPY to trigger a reload")

# AUTO_RELOAD here means a filesystem write restarted us, not a real reset.
print("run reason:", supervisor.runtime.run_reason)
print("auto-reload enabled:", supervisor.runtime.autoreload)
print("Send 'r' or Ctrl-D in serial monitor to reload on demand.")
print()

NS_PER_SEC = 1000000000
start = time.monotonic_ns()
next_tick = start

RELOAD_KEYS = ("r", "R", "\x04")     # "r", or Ctrl-D (EOT), as at the REPL

def check_keys():
    """Non-blocking: consume pending serial input and act on it."""
    while supervisor.runtime.serial_bytes_available:
        key = sys.stdin.read(1)
        if key in RELOAD_KEYS:
            print("reloading...")
            supervisor.reload()


while True:
    check_keys()

    # Heartbeat once a second. If this counter jumps back to 0, something
    # wrote to the filesystem and auto-reload restarted the program.
    now = time.monotonic_ns()
    if now >= next_tick:
        print("uptime: {:d}s".format((now - start) // NS_PER_SEC))
        next_tick += NS_PER_SEC
