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
        self.lcd.clear()
        self.lcd.write_string(line1)
        if line2:
            self.lcd.crlf()
            self.lcd.write_string(line2)
        time.sleep(0.25)  # small delay to ensure the message is displayed

    def clear(self):
        self.lcd.clear()

