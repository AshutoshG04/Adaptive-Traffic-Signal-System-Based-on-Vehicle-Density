# Path: detection.py

from ultralytics import YOLO
import config

class VehicleDetector:

    def __init__(self):
        self.model = YOLO("best.pt")

    def detect(self, frame):
        results = self.model(frame, conf=0.4, verbose=False)
        count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]

                if label in config.VEHICLE_CLASSES:
                    count += 1

        annotated = results[0].plot()
        return annotated, count