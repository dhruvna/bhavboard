# src/main.py
from buttons import ButtonManager
from lcd import LCDManager
import time

def main():
    buttons = ButtonManager()
    lcd = LCDManager()
    time.sleep(2)
    lcd.show("Button 1", "GPIO 5")
    time.sleep(2)
    lcd.show("Playing:", "sound1.wav")
    print("BhavBoard button test running...")

    try:
        while True:
            presses = buttons.poll()
            for pin in presses:
                print(f"Button on GPIO {pin} pressed")
            time.sleep(0.01)

    except KeyboardInterrupt:
        buttons.cleanup()
        print("\nExiting cleanly")

if __name__ == "__main__":
    main()
