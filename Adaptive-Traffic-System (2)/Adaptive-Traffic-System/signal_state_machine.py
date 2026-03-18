# Path: signal_state_machine.py

import time
import config

class SignalStateMachine:

    def __init__(self):
        self.current_lane = 0
        self.phase_start = time.time()
        self.green_duration = config.BASE_GREEN

    def should_switch(self):
        return time.time() - self.phase_start > self.green_duration

    def switch(self, next_lane, duration):
        self.current_lane = next_lane
        self.green_duration = duration
        self.phase_start = time.time()