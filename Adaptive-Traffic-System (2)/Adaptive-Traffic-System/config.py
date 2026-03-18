# Path: config.py

VIDEO_PATHS = [
    "videos/cam1.mp4",
    "videos/video5.mp4",
    "videos/cam3.mp4",
    "videos/cam4.mp4"
]

MODEL_PATH = "yolov8n.pt"

VEHICLE_CLASSES = ["car", "truck", "bus", "motorbike"]

CONFIDENCE_THRESHOLD = 0.4

BASE_GREEN = 10
MIN_GREEN = 8
MAX_GREEN = 60

ALPHA = 0.7
BETA = 0.3

FAILSAFE_TIMEOUT = 5
FRAME_SKIP = 3
ROI_RATIO = 0.6   # Bottom 40%