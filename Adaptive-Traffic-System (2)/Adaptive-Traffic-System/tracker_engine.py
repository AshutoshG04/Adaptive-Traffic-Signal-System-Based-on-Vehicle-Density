import math
import uuid
import time


class SimpleTracker:

    def __init__(self):
        self.objects = {}
        self.last_seen = {}

    def _distance(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def update(self, detections):

        tracked = []
        now = time.time()

        for det in detections:

            x1, y1, x2, y2 = det["bbox"]
            cx, cy = (x1 + x2)//2, (y1 + y2)//2

            matched_id = None

            # improved matching
            for oid, obj in self.objects.items():

                old_cx, old_cy = obj["center"]

                dist = self._distance(
                    (old_cx, old_cy),
                    (cx, cy)
                )

                if dist < 80:
                    matched_id = oid
                    break

            if matched_id is None:
                matched_id = str(uuid.uuid4())

            self.objects[matched_id] = {
                "center": (cx, cy)
            }

            self.last_seen[matched_id] = now

            tracked.append({
                "id": matched_id,
                "bbox": det["bbox"]
            })

        # remove old objects (anti ghost)
        for oid in list(self.last_seen.keys()):
            if now - self.last_seen[oid] > 1:
                del self.last_seen[oid]
                if oid in self.objects:
                    del self.objects[oid]

        return tracked