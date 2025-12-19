# src/main.py
from config import BUTTON_MAPPING
from buttons import ButtonManager
from audio import AudioManager
from lcd import LCDManager
import time

def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    audio = AudioManager()
    lcd.show("BhavBoard", "Initialized")
    time.sleep(2)
    lcd.show("Push a button", "to begin!")

    try:
        while True:
            presses = buttons.poll()
            for pin in presses:
                lcd.show(f"Playing: ", f"{BUTTON_MAPPING[pin]['label']}")
                audio.play(f"sounds/{BUTTON_MAPPING[pin]['sound']}")
            time.sleep(0.01)

    except KeyboardInterrupt:
        buttons.cleanup()
        lcd.show("Exiting cleanly")
        time.sleep(1)
        lcd.clear()

if __name__ == "__main__":
    main()
