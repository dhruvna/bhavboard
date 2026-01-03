from RPLCD.i2c import CharLCD
import time

class LCDManager:
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x27,
            port=1,
            cols=16,
            rows=2
        )

        self.clear()

    def show(self, line1="", line2=""):
        try:
            # If we previously disabled backlight/display, re-enable
            if hasattr(self.lcd, "backlight_enabled"):
                self.lcd.backlight_enabled = True
            if hasattr(self.lcd, "display_enabled"):
                self.lcd.display_enabled = True

            self.lcd.clear()
            self.lcd.write_string(line1)
            if line2:
                self.lcd.crlf()
                self.lcd.write_string(line2)
            time.sleep(0.25)  # small delay to ensure the message is displayed
        except OSError as e:
            print(f"[LCD] I2C Error: {e}")

    def clear(self):
        try:
            self.lcd.clear()
        except OSError as e:
            print(f"[LCD] I2C Error: {e}")

    def off(self):
        try:
            self.lcd.clear()
            # These attributes exist on many RPLCD backends; guard so we never crash if absent.
            if hasattr(self.lcd, "backlight_enabled"):
                self.lcd.backlight_enabled = False
            if hasattr(self.lcd, "display_enabled"):
                self.lcd.display_enabled = False
            time.sleep(0.1)
        except OSError as e:
            print(f"[LCD] I2C Error: {e}")
        except Exception as e:
            print(f"[LCD] off() error: {e}")

