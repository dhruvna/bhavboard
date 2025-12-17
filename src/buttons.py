# src/buttons.py
import RPi.GPIO as GPIO
import time
from config import BUTTON_PINS, DEBOUNCE_MS

class ButtonManager:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.last_state = {}
        self.last_time = {}

        for pin in BUTTON_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.last_state[pin] = GPIO.input(pin)
            self.last_time[pin] = 0

    def poll(self):
        """Return list of pins that were newly pressed"""
        pressed = []
        now = time.time() * 1000  # ms

        for pin in BUTTON_PINS:
            state = GPIO.input(pin)

            if self.last_state[pin] == 1 and state == 0:
                if now - self.last_time[pin] > DEBOUNCE_MS:
                    pressed.append(pin)
                    self.last_time[pin] = now

            self.last_state[pin] = state

        return pressed

    def cleanup(self):
        GPIO.cleanup()
