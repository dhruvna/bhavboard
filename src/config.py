# config.py
'''
Buttons are BCM Numbered (5 means GPIO5, not Pin 5)
'''
BUTTON_MAPPING = {
    5:  {
        "index": 1,
        "label": "Sound 1",
        "sound": "sound1.wav"
    },
    6:  {
        "index": 2,
        "label": "Sound 2",
        "sound": "sound2.wav"
    },
    13: {
        "index": 3,
        "label": "Sound 3",
        "sound": "sound3.wav"
    },
    19: {
        "index": 4,
        "label": "Sound 4",
        "sound": "sound4.wav"
    },
    26: {
        "index": 5,
        "label": "Sound 5",
        "sound": "sound5.wav"
    },
    12: {
        "index": 6,
        "label": "Sound 6",
        "sound": "sound6.wav"
    },
    16: {
        "index": 7,
        "label": "Sound 7",
        "sound": "sound7.wav"
    },
    20: {
        "index": 8,
        "label": "Sound 8",
        "sound": "sound8.wav"
    },
    21: {
        "index": 9,
        "label": "Sound 9",
        "sound": "sound9.wav"
    }
}

DEBOUNCE_MS = 200 # Debounce window that helps prevent false double-triggers