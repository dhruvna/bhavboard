# BhavBoard – Project Status & Roadmap
SECRET SANTA 2025 FOR BHAVIK!

Portable button-based soundboard built on a Raspberry Pi Zero W.

---

## DONE ALREADY

### Development & Workflow
- Raspberry Pi Zero W accessible via SSH
- GitHub repo https://github.com/dhruvna/bhavboard

### Hardware Bring-Up
- GPIO button input system works:
  - Active-LOW inputs
  - Internal pull-ups
  - Debouncing implemented
- Verified with a toggle switch.
- Using 1602A LCD w/ I²C backpack

### Parts Ordered
- Momentary push buttons
- Adafruit Mini External USB 2.0 Speaker
- Micro-USB OTG adapter
- 40-pin GPIO header

### Project Structure + Run Instructions
- Project layout:
- bhavboard/
- - src/
- - - main.py
- - - buttons.py
- - - lcd.py
- - - audio.py
- - - config.py
- - sounds/
- - requirements.txt
- - README.md

- Standardize run procedure:
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `i2cdetect -y 1` should show an address available, ensure LCD driver used this one
- `python src/main.py`

### Buttons
- Need to wire & test real momentary buttons (active-LOW).
- GPIO pin mapping exists in `config.py`.

### LCD
- `lcd.py` abstraction:
- initializes LCD
- shows boot message
- shows last pressed button label (based on mapping in `config.py`)

---

### TODO 

### Audio Bring-Up
- Connect USB speaker via OTG.
- Verify detection (`aplay -l`).
- Choose playback backend (`aplay`, `mpg123`, etc.).
- Create `audio.py` abstraction:
- play sound
- interrupt / ignore policy
- Add `sounds/` directory and naming convention.
- Map buttons → sound files in `config.py`.


### Full Soundboard Behavior
- Integrate buttons + LCD + audio.
- Decide playback behavior:
- interrupt vs non-interrupt
- Handle errors (missing files, no audio device).

### Zero-Knowledge User Experience
- Auto-start program on boot (systemd service).
- Optional shutdown strategy.
- Ensure consistent startup behavior.

### Hardware Finalization
- Solder 40-pin header to Pi Zero W.
- Transition from breadboard to perfboard or enclosure.
- Clean wiring and strain relief.
- Plan enclosure:
- button layout
- LCD window
- speaker vents
- power access

### Optional Enhancements
- Volume control (rotary encoder)
- Multiple sound banks
- Battery monitoring (if moving to LiPo later)

### Resume Point

Next step is  **audio bring-up once parts arrive**
