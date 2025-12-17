# config.py
'''
Buttons are BCM Numbered (5 means GPIO5, not Pin 5)
'''
BUTTON_PINS = [
    5,   # Button 1
    6,   # Button 2
    13,  # Button 3
    19,  # Button 4
    26,  # Button 5
    12,  # Button 6
    16,  # Button 7
    20,  # Button 8
    21,  # Button 9
]

BUTTON_LABELS = {
    5:  "Sound 1",
    6:  "Sound 2",
    13: "Sound 3",
    19: "Sound 4",
    26: "Sound 5",
    12: "Sound 6",
    16: "Sound 7",
    20: "Sound 8",
    21: "Sound 9"
}

DEBOUNCE_MS = 200 # Debounce window that helps prevent false double-triggers
