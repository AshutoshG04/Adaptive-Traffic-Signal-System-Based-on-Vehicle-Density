# traffic_controller.py

import config
import time
from esp_control import send_lane


class TrafficController:

    def __init__(self):
        self.queue_lengths = [0,0,0,0]
        self.waiting_time = [0,0,0,0]
        self.last_lane = -1
        self.last_update = time.time()

    # -----------------------------------
    # Update Queue
    # -----------------------------------
    def update_queue(self, lane, count):

        self.queue_lengths[lane] = (
            0.7 * self.queue_lengths[lane] +
            0.3 * count
        )

    # -----------------------------------
    # Waiting Time
    # -----------------------------------
    def update_waiting(self, active_lane):

        for i in range(4):
            if i != active_lane:
                self.waiting_time[i] += 1
            else:
                self.waiting_time[i] = 0

    # -----------------------------------
    # Priority Formula
    # -----------------------------------
    def compute_priority(self, lane):

        return (
            config.ALPHA * self.queue_lengths[lane] +
            config.BETA * self.waiting_time[lane]
        )

    # -----------------------------------
    # SELECT BEST LANE
    # -----------------------------------
    def select_next_lane(self):

        priorities=[
            self.compute_priority(i) for i in range(4)
        ]

        best_lane = priorities.index(max(priorities))

        # SEND 1..4 (NOT 0..3)
        send_lane(best_lane + 1)

        return best_lane