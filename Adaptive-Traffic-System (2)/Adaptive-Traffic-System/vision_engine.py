# Path: vision_engine.py

from ultralytics import YOLO
import config
import torch


class VisionEngine:

    def __init__(self):

        # Select device automatically
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[VISION] Running on {self.device.upper()}")

        # Load model
        self.model = YOLO(config.MODEL_PATH)

        # Move to GPU
        self.model.to(self.device)

        print("[VISION] Model loaded successfully.")

    def detect(self, frame):

        h, w, _ = frame.shape

        # Bottom 60% ROI
        roi = frame[int(h * 0.4):h, :]

        # Let Ultralytics handle FP16 internally
        results = self.model.predict(
            source=roi,
            conf=config.CONFIDENCE_THRESHOLD,
            device=self.device,
            imgsz=384,
            half=(self.device == "cuda"),   # Automatic FP16
            stream=True,
            verbose=False
        )

        detections = []

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])
                label = self.model.names[cls]

                if label in config.VEHICLE_CLASSES:

                    x1, y1, x2, y2 = box.xyxy[0]
                    y_offset = int(h * 0.4)

                    detections.append({
                        "bbox": [
                            int(x1),
                            int(y1 + y_offset),
                            int(x2),
                            int(y2 + y_offset)
                        ],
                        "label": label
                    })

        return detections