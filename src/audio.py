#src/audio.py

import subprocess
import os

class AudioManager:
    def __init__(self):
        self.current_process = None

    def play(self, filepath):
        if not os.path.exists(filepath):
            print(f"[AUDIO] File not found: {filepath}")
            return
        
        # Stop current audio if playing
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
        
        try:
            self.current_process = subprocess.Popen(
                ["aplay", filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"[AUDIO] Playback error: {e}")

    def is_playing(self) -> bool:
        return self.current_process and self.current_process.poll() is None