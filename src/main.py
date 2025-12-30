# src/main.py
from config import BUTTON_MAPPING
from buttons import ButtonManager
from audio import AudioManager
from lcd import LCDManager
import time
import subprocess

def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    audio = AudioManager()
    lcd.show("BhavBoard", "Initialized")
    time.sleep(2)
    lcd.show("Push a button", "to begin!")
    hold_start = None
    HOLD_TIME_SEC = 5

    try:
        while True:
            presses = buttons.poll()
            for pin in presses:
                lcd.show(f"Playing: ", f"{BUTTON_MAPPING[pin]['label']}")
                audio.play(f"sounds/{BUTTON_MAPPING[pin]['sound']}")
            time.sleep(0.01)

            pressed_now = buttons.get_pressed()
            if pressed_now:
                if hold_start is None:
                    hold_start = time.time()
                elif time.time() - hold_start >= HOLD_TIME_SEC:
                    lcd.show("Shutting down in 5", "Please wait...")
                    time.sleep(0.5)
                    lcd.clear()
                    subprocess.run(
                        ["sudo", "/sbin/shutdown", "-h", "now"]
                    )
            else:
                hold_start = None

    except KeyboardInterrupt:
        buttons.cleanup()
        lcd.show("Exiting cleanly")
        time.sleep(1)
        lcd.clear()

if __name__ == "__main__":
    main()
