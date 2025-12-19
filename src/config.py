# config.py
'''
Buttons are BCM Numbered (5 means GPIO5, not Pin 5)
'''
BUTTON_MAPPING = {
    5:  {
        "index": 1,
        "label": "Merry Bhavmas",
        "sound": "bhavmas.wav"
    },
    6:  {
        "index": 2,
        "label": "Bhavtrosballs",
        "sound": "bhavtros_balls.wav"
    },
    13: {
        "index": 3,
        "label": "Happy Birthday",
        "sound": "birthday.wav"
    },
    19: {
        "index": 4,
        "label": "Fly Me to the Pooooo",
        "sound": "FLYMETOTHEPOO.wav"
    },
    26: {
        "index": 5,
        "label": "IRAQ",
        "sound": "iraq.wav"
    },
    12: {
        "index": 6,
        "label": "THEY BE LIKE",
        "sound": "they_be_like.wav"
    },
    16: {
        "index": 7,
        "label": "يها الفارس",
        "sound": "Zaahen1.wav"
    },
    20: {
        "index": 8,
        "label": "لست بآثم",
        "sound": "Zaahen2.wav"
    },
    21: {
        "index": 9,
        "label": "إن وِزر هذا العنف",
        "sound": "Zaahen3.wav"
    }
}

DEBOUNCE_MS = 200 # Debounce window that helps prevent false double-triggers