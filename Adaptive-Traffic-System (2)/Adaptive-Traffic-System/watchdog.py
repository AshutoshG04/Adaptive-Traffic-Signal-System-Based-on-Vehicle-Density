# Path: watchdog.py

import time
import config

class Watchdog:

    def __init__(self):
        self.last_heartbeat = time.time()

    def beat(self):
        self.last_heartbeat = time.time()

    def is_alive(self):
        return time.time() - self.last_heartbeat < config.FAILSAFE_TIMEOUT