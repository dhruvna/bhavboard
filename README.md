# BhavBoard – Project Status & Roadmap
SECRET SANTA 2025 FOR BHAVIK!

Portable button-based soundboard built on a Raspberry Pi Zero W.

---

### Development & Workflow
- Raspberry Pi Zero W accessible via SSH

- sudo apt update
- sudo apt -y full-upgrade
- sudo reboot

Enable I2C Interface
- sudo raspi-config

Helpful Util Installation
- sudo apt install -y git python3-venv python3-pip i2c-tools alsa-utils

Clone GitHub repo (Make sure you have valid ssh key added)
- cd ~
- git clone git@github.com:dhruvna/bhavboard.git 
- cd bhavboard

Check i2C Bus
- i2cdetect -y 1

Check usb speaker
- aplay -l

Enable autostart systemd
- sudo nano /etc/systemd/system/bhavboard.service

Paste into bhavboard.service
```
[Unit]
Description=BhavBoard Soundboard
After=network.target sound.target
Wants=network.target

[Service]
Type=simple
User=dhruvna
WorkingDirectory=/home/dhruvna/bhavboard
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/dhruvna/bhavboard/.venv/bin/python /home/dhruvna/bhavboard/src/main.py
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

Enable autostart systemd
- sudo systemctl daemon-reload
- sudo systemctl enable bhavboard.service
- sudo systemctl start bhavboard.service

Give python permission to shutoff
sudo visudo

dhruvna ALL=NOPASSWD: /sbin/shutdown, /usr/sbin/shutdown, /bin/systemctl poweroff, /bin/systemctl halt, /bin/systemctl shutdown


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
- Transition from breadboard enclosure
- Clean wiring and strain relief
- Door hinge + latch

