# src/main.py
from config import BUTTON_MAPPING
from buttons import ButtonManager
from audio import AudioManager
from lcd import LCDManager
import time
import subprocess

# ===== Hold behavior config =====
MIXER_CONTROL = "PCM"   
VOL_STEP = 5            # per tick
VOL_REPEAT_SEC = 0.15      # how fast volume changes while held
SHUTDOWN_HOLD_SEC = 5.0    # how long to hold Button 2 to shutdown
SHUTDOWN_DISPLAY_DELAY = 1.0  # seconds before showing shutdown UI

def set_volume(delta: str):
    # delta of +- VOL_STEP"
    subprocess.run(
        ["amixer", "-q", "sset", MIXER_CONTROL, delta],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def shutdown_now(lcd: LCDManager):
    lcd.show("Shutting down", "Byebye Bhav :)")
    time.sleep(0.5)
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    audio = AudioManager()

    subprocess.run( # 
        ["amixer", "-q", "sset", MIXER_CONTROL, "50%"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    VOLUME = 50 # initial volume percentage

    lcd.show("BhavBoard", "Initialized")
    time.sleep(1.5)
    lcd.show("Push a button", "to begin!")
    
    # pin -> time (when hold started)
    hold_start = {}
    # pin -> time (when we last applied repeating action)
    last_repeat = {}
        
    try:
        while True:

            now = time.monotonic()

            # ---- Edge-triggered sound playback ----
            presses = buttons.poll()
            for pin in presses:
                cfg = BUTTON_MAPPING[pin]
                lcd.show("Playing:", cfg["label"])
                audio.play(f"sounds/{cfg['sound']}")

            # ---- Level-triggered hold behaviors ----
            pressed_now = set(buttons.get_pressed())

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
            
            # Handle repeating actions for held buttons
            for pin, t0 in hold_start.items():
                cfg = BUTTON_MAPPING[pin]
                idx = cfg["index"]
                held_for = now - t0

                # Shutdown (Button 2 when held, includes countdown)
                if idx == 2:
                    if held_for >= SHUTDOWN_DISPLAY_DELAY:
                        remaining = int(SHUTDOWN_HOLD_SEC - held_for + 0.999)
                        
                    if remaining >= 0 and held_for < SHUTDOWN_HOLD_SEC:
                        # Update countdown (don’t spam too hard)
                        if now - last_repeat[pin] >= 0.5:
                            lcd.show("Hold to power off", f"Shutting in {remaining}")
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
                
                time.sleep(0.05) # small delay to avoid busy loop

    except KeyboardInterrupt:
        buttons.cleanup()
        lcd.show("Exiting cleanly")
        time.sleep(1)
        lcd.clear()

if __name__ == "__main__":
    main()
