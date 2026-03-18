# Path: hardware_interface.py

class HardwareInterface:

    def __init__(self):
        self.mode = "AI"

    def set_signal(self, lane):
        print(f"[HARDWARE] GREEN → Lane {lane+1}")

    def fallback_fixed_mode(self):
        self.mode = "FIXED"
        print("[HARDWARE] Switching to FIXED TIMING MODE")