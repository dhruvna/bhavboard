# src/main.py
from buttons import ButtonManager
import time

def main():
    buttons = ButtonManager()
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
