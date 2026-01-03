# src/main.py
from config import BUTTON_MAPPING
from buttons import ButtonManager
from audio import AudioManager
from lcd import LCDManager
import time
import subprocess
import signal
import sys
import random

# ===== Hold behavior config =====
MIXER_CONTROL = "PCM"   
VOL_STEP = 5            # per tick
VOL_REPEAT_SEC = 0.15      # how fast volume changes while held
SHUTDOWN_HOLD_SEC = 5.0    # how long to hold Button 2 to shutdown

IDLE_LINE1 = "Push a button"
IDLE_LINE2 = "to begin!"

# Button Combos (GPIO BCM Numbered)
COMBO_67 = frozenset({12, 16}) 
COMBO_67_SOUNDS = [
    "67_Austin.wav",
    "67_Bhavik.wav",
    "67_Bhavik2.wav",
    "67_Tristan.wav",
    "67_Dhruv.wav"
]

HELP_COMBO = frozenset({5, 13})  # Buttons 1 + 3
HELP_HOLD_SEC = 1

INSTRUCTION_PAGES = [
    ("How to use:", "Press buttons"),
    ("Volume:", "Hold 1 = Down"),
    ("Volume:", "Hold 3 = Up"),
    ("Power:",  "Hold 2 = Off"),
    ("Tip:",    "Try combos ;)"),
]

def set_volume(delta: str):
    # delta of +- VOL_STEP"
    subprocess.run(
        ["amixer", "-q", "sset", MIXER_CONTROL, delta],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def run_instructions(lcd, pages, delay=1.5): # Show instruction pages line-by-line
    for line1, line2 in pages:
        lcd.show(line1, line2)
        time.sleep(delay)

def shutdown_now(lcd: LCDManager):
    lcd.show("Shutting down", "Byebye Bhav :)")
    time.sleep(0.8)     # let them read it
    lcd.off()           # blank the display while the Pi is halted
    time.sleep(0.2)
    subprocess.run(["sudo", "shutdown", "-h", "now"])


def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    audio = AudioManager()

    def handle_exit(signum, frame):
        try:
            lcd.off()
        finally:
            buttons.cleanup()
            sys.exit(0)

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    
    subprocess.run( # 
        ["amixer", "-q", "sset", MIXER_CONTROL, "50%"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    VOLUME = 50 # initial volume percentage

    lcd.show("BhavBoard", "Initialized")
    time.sleep(1.2)
    # Show instructions on startup
    run_instructions(lcd, INSTRUCTION_PAGES, delay=1.5)
    # Then go to idle
    lcd.show(IDLE_LINE1, IDLE_LINE2)
    
    pending_idle = False
    idle_due_time = 0.0
    was_playing = False

    # Combo Tracking
    active_combos = set()  # combos currently being held 
    help_triggered = False  # for hold-to-help latch

    # Hold Tracking
    # pin -> time (when hold started)
    hold_start = {}
    # pin -> time (when we last applied repeating action)
    last_repeat = {}
        
    try:
        while True:
            now = time.monotonic()

            # ---- Input capture ----
            presses = set(buttons.poll())          # newly pressed pins this tick
            pressed_now = set(buttons.get_pressed())  # pins currently held down

            # Start hold timers for newly pressed pins
            for pin in pressed_now:
                if pin not in hold_start:
                    hold_start[pin] = now
                    last_repeat[pin] = 0.0
            
            # Clear timers for released pins
            for pin in list(hold_start.keys()):
                if pin not in pressed_now:
                    del hold_start[pin]
                    del last_repeat[pin]

            # ---- Help / Instructions combo (hold Vol- + Vol+) ----
            if HELP_COMBO.issubset(pressed_now):
                t0 = min(hold_start.get(p, now) for p in HELP_COMBO)
                if (not help_triggered) and ((now - t0) >= HELP_HOLD_SEC):
                    help_triggered = True

                    # Avoid scheduling idle while we run instructions
                    pending_idle = False
                    was_playing = False

                    run_instructions(lcd, INSTRUCTION_PAGES, delay=1.5)
                    lcd.show(IDLE_LINE1, IDLE_LINE2)

                    # Consume any presses this tick so we don't also play sounds
                    presses.clear()

            else:
                help_triggered = False

            # If help just ran, skip the rest of the loop this tick
            if help_triggered:
                time.sleep(0.05)
                continue

            # ---- Combo detection (rising edge) ----
            combo_fired = None
            combos = [
                ("RANDOM_67", COMBO_67),
            ]

            for name, combo in combos:
                if combo.issubset(pressed_now):
                    if combo not in active_combos:
                        # rising edge: combo just became active
                        active_combos.add(combo)
                        combo_fired = name
                    break

            # Clear combos that are no longer held
            for combo in list(active_combos):
                if not combo.issubset(pressed_now):
                    active_combos.remove(combo)

            # If a combo fired, consume its member presses so singles don't also trigger
            if combo_fired == "RANDOM_67":
                presses -= set(COMBO_67)

            # ---- Handle combo action (if any) ----
            if combo_fired == "RANDOM_67":
                pending_idle = False
                sound = random.choice(COMBO_67_SOUNDS)
                lcd.show("67 Unlocked!", "Good luck :)")
                audio.play(f"sounds/{sound}")
                was_playing = True
            
            # ---- Edge-triggered sound playback ----
            for pin in presses:
                pending_idle = False
                cfg = BUTTON_MAPPING[pin]
                lcd.show("Playing:", cfg["label"])
                audio.play(f"sounds/{cfg['sound']}")
                was_playing = True

            # ---- Level-triggered hold behaviors ----
            # pressed_now = set(buttons.get_pressed())

            # # Start hold timers for newly pressed pins
            # for pin in pressed_now:
            #     if pin not in hold_start:
            #         hold_start[pin] = now
            #         last_repeat[pin] = 0.0
            
            # # Clear timers for released pins
            # for pin in list(hold_start.keys()):
            #     if pin not in pressed_now:
            #         del hold_start[pin]
            #         del last_repeat[pin]
            
            # Handle repeating actions for held buttons
            for pin, t0 in hold_start.items():
                cfg = BUTTON_MAPPING[pin]
                if cfg is None:
                    continue
                idx = cfg["index"]
                held_for = now - t0

                # Shutdown (Button 2 when held, includes countdown)
                if idx == 2:
                    if held_for >= 1:
                        remaining = int(SHUTDOWN_HOLD_SEC - held_for + 0.999)
                        if remaining >= 0 and held_for < SHUTDOWN_HOLD_SEC:
                            # Update countdown (don’t spam too hard)
                            if now - last_repeat[pin] >= 1:
                                lcd.show("Hold for shutoff", f"Off in {remaining}")
                                last_repeat[pin] = now

                    if held_for >= SHUTDOWN_HOLD_SEC:
                        shutdown_now(lcd)
                        return

                # Volume Down (Button 1 while held)
                elif idx == 1:
                    if held_for >= 0.4 and (now - last_repeat[pin] >= VOL_REPEAT_SEC):
                        VOLUME -= VOL_STEP
                        VOLUME = max(10, VOLUME)
                        set_volume(f"{VOLUME}%")
                        lcd.show("Volume Down ", f"Now at {VOLUME}%")
                        last_repeat[pin] = now

                # Volume Up (Button 3 while held)
                elif idx == 3:
                    if held_for >= 0.4 and (now - last_repeat[pin] >= VOL_REPEAT_SEC):
                        VOLUME += VOL_STEP
                        VOLUME = min(100, VOLUME)
                        set_volume(f"{VOLUME}%")
                        lcd.show("Volume Up", f"Now at {VOLUME}%")
                        last_repeat[pin] = now
                
            # ---- Idle display management ----
            playing = audio.is_playing()

            # Detect "audio just finished"
            if was_playing and not playing:
                # Just stopped playing
                pending_idle = True
                idle_due_time = now + 1 # 1 second until idle

            # If we're due to restore idle (and nothing is currently playing), do it
            if pending_idle and (now>=idle_due_time) and not playing and len(pressed_now) == 0:
                # Only restore if no buttons currently held (prevents fighting volume/shutdown text)
                lcd.show(IDLE_LINE1, IDLE_LINE2)
                pending_idle = False

            was_playing = playing

            time.sleep(0.05) # small delay to avoid busy loop

    except KeyboardInterrupt:
        buttons.cleanup()
        lcd.show("Exiting cleanly")
        time.sleep(1)
        lcd.clear()

if __name__ == "__main__":
    main()
