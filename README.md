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

### Audio Bring-Up
- Connect USB speaker via OTG.
- Create `audio.py` abstraction:
- play sound
- Add `sounds/` directory and naming convention.
- Map buttons → sound files in `config.py`.

### Full Soundboard Behavior
- Integrate buttons + LCD + audio.

### Zero-Knowledge User Experience
- Auto-start program on boot (systemd service).
- Shutdown via button hold

### Hardware Finalization
- Solder 40-pin header to Pi Zero W.
- Plan enclosure:
- Button layout
- LCD window
- Speaker vents

### TODO 

### Hardware Finalization
- Transition from breadboard enclosure
- Clean wiring and strain relief.
- Plan enclosure:
- Power access

Next step is  **hardware assembly**
