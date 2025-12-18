# src/main.py
from buttons import ButtonManager
from lcd import LCDManager
import time

def main():
    buttons = ButtonManager()
    lcd = LCDManager()

    try:
        while True:
            presses = buttons.poll()
            for pin in presses:
                lcd.show(f"Button {pin} Pressed")
                print(f"Button on GPIO {pin} pressed")
            time.sleep(0.01)

    except KeyboardInterrupt:
        buttons.cleanup()
        print("\nExiting cleanly")

if __name__ == "__main__":
    main()
