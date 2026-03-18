# Path: traffic_engine.py

import config
import time

class TrafficEngine:

    def __init__(self):
        self.counts = [0,0,0,0]
        self.active_lane = 0
        self.green_timer = 0
        self.last_switch = time.time()

    def update_counts(self, cam_id, count):
        self.counts[cam_id] = count

    def calculate(self):
        now = time.time()

        if now - self.last_switch > self.green_timer:
            self.active_lane = self.counts.index(max(self.counts))
            vehicles = self.counts[self.active_lane]

            green = config.BASE_GREEN_TIME + vehicles * config.TIME_MULTIPLIER
            green = max(config.MIN_GREEN_TIME, green)
            green = min(config.MAX_GREEN_TIME, green)

            self.green_timer = green
            self.last_switch = now

        remaining = int(self.green_timer - (now - self.last_switch))

        total = sum(self.counts)

        if total < 10:
            density = "LOW"
        elif total < 25:
            density = "MEDIUM"
        else:
            density = "HIGH"

        return {
            "counts": self.counts,
            "active_lane": self.active_lane,
            "remaining": max(0, remaining),
            "density": density
        }