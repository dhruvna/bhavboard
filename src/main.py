# src/main.py
from config import BUTTON_MAPPING
from buttons import ButtonManager
from lcd import LCDManager
import time

def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    lcd.show("BhavBoard", "Initialized")
    time.sleep(2)
    lcd.show("Push a button", "to begin!")

    try:
        while True:
            presses = buttons.poll()
            for pin in presses:
                lcd.show(f"Button {pin} Pressed")
                time.sleep(1)
                lcd.show(f"Playing: ", f"{BUTTON_MAPPING[pin]['label']}")
                # Code to play the sound file
            time.sleep(0.01)

    except KeyboardInterrupt:
        buttons.cleanup()
        lcd.show("Exiting cleanly")
        lcd.clear()

if __name__ == "__main__":
    main()
