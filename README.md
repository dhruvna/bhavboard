# BhavBoard – Project Status & Roadmap
SECRET SANTA 2025 FOR BHAVIK!

Portable button-based soundboard built on a Raspberry Pi Zero W.

---

## ✅ Current Status (What’s Done)

### Development & Workflow
- Raspberry Pi Zero W is flashed, booting, and reachable over Wi-Fi.
- SSH access works reliably.
- GitHub repo (`bhavboard`) is set up and cloned on:
  - Windows dev machine
  - Raspberry Pi (`~/bhavboard`)
- Development workflow:
  - Edit locally → commit/push
  - Pull on Pi → run/test

### Python Environment
- Project uses a local virtual environment (`.venv`) due to PEP 668.
- Virtual environment is created and usable.
- RPLCD is installed inside the venv.
- All project code is intended to run inside the venv.

### Hardware Bring-Up
- GPIO button input system works:
  - Active-LOW inputs
  - Internal pull-ups
  - Edge detection (HIGH → LOW)
  - Debouncing implemented
- Verified with a toggle switch.
- I²C is enabled on the Pi.
- 1602A LCD + I²C backpack works reliably.

### Architecture Decisions
- Clean separation of concerns:
  - Buttons emit events
  - Application logic handles state
  - Outputs (LCD now, audio later) consume events
- Designed to scale up to 9 buttons.
- LCD-first, audio-second development order.

### Parts Ordered
- Momentary push buttons
- Adafruit Mini External USB 2.0 Speaker (USB audio device)
- Micro-USB OTG adapter
- 40-pin GPIO header

---

## ⏳ Remaining Work (Roadmap)

### Phase 1 – Repo Structure & Baseline
- Ensure clean project layout:

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

---

### Phase 2 – Buttons (Final Hardware)
- Wire real momentary buttons (active-LOW).
- Start with 2–3 buttons, but reserve pins for up to 9.
- Tune debounce timing if needed.
- Finalize GPIO pin map in `config.py`.

---

### Phase 3 – LCD Integration
- Create `lcd.py` abstraction:
- init LCD
- show boot message
- show ready state
- show last pressed button label
- Add button → label mapping in `config.py`.
- Integrate LCD updates into `main.py`.

---

### Phase 4 – Audio Bring-Up
- Connect USB speaker via OTG.
- Verify detection (`aplay -l`).
- Choose playback backend (`aplay`, `mpg123`, etc.).
- Create `audio.py` abstraction:
- play sound
- interrupt / ignore policy
- Add `sounds/` directory and naming convention.
- Map buttons → sound files in `config.py`.

---

### Phase 5 – Full Soundboard Behavior
- Integrate buttons + LCD + audio.
- Decide playback behavior:
- interrupt vs non-interrupt
- Handle errors (missing files, no audio device).

---

### Phase 6 – Zero-Knowledge User Experience
- Auto-start program on boot (systemd service).
- Optional shutdown strategy.
- Ensure consistent startup behavior.

---

### Phase 7 – Hardware Finalization
- Solder 40-pin header to Pi Zero W.
- Transition from breadboard to perfboard or enclosure.
- Clean wiring and strain relief.
- Plan enclosure:
- button layout
- LCD window
- speaker vents
- power access

---

### Phase 8 – Optional Enhancements
- LEDs per button
- Volume control (rotary encoder)
- Multiple sound banks
- Battery monitoring (if moving to LiPo later)

---

## Notes
- Prototype with headers and breadboard first.
- Avoid soldering directly to Pi GPIO pads.
- All non-apt Python dependencies go in `.venv`.

---

## Resume Point
Next step is **LCD integration into project code**, followed by **audio bring-up once parts arrive**.
