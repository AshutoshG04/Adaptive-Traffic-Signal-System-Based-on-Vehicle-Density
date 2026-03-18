import cv2
import time
import threading
from flask import Flask, render_template, Response, jsonify

import config
from vision_engine import VisionEngine
from traffic_controller import TrafficController
from signal_state_machine import SignalStateMachine
from hardware_interface import HardwareInterface
from watchdog import Watchdog
from tracker_engine import SimpleTracker

app = Flask(__name__)

vision = VisionEngine()
controller = TrafficController()
state_machine = SignalStateMachine()
hardware = HardwareInterface()
watchdog = Watchdog()

cameras = [cv2.VideoCapture(p) for p in config.VIDEO_PATHS]
latest_frames = [None] * 4

trackers = [SimpleTracker() for _ in range(4)]

# smooth tracking cache
last_detections = [None] * 4
last_tracked = [None] * 4

frame_counter = 0


def process_cameras():
    global frame_counter

    while True:
        for i in range(4):

            ret, frame = cameras[i].read()

            if not ret:
                cameras[i].set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # Run YOLO only every FRAME_SKIP frames
            if frame_counter % config.FRAME_SKIP == 0:
                detections = vision.detect(frame)
                last_detections[i] = detections

                tracked = trackers[i].update(detections)
                last_tracked[i] = tracked
            else:
                tracked = last_tracked[i] or []

            # Update queue count using tracked objects
            controller.update_queue(i, len(tracked))

            # Draw bounding boxes
            for obj in tracked:
                x1, y1, x2, y2 = obj["bbox"]
                oid = obj["id"][:4]

                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 255, 0), 2)

                cv2.putText(
                    frame,
                    f"Car {oid}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # Professional vehicle count UI
            cv2.rectangle(frame, (10, 10), (230, 60), (0, 0, 0), -1)

            cv2.putText(
                frame,
                f"Vehicles: {len(tracked)}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            latest_frames[i] = frame

        frame_counter += 1
        watchdog.beat()
        time.sleep(0.03)


threading.Thread(target=process_cameras, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/traffic_data")
def traffic_data():

    if not watchdog.is_alive():
        hardware.fallback_fixed_mode()

    next_lane = controller.select_next_lane()
    controller.update_waiting(state_machine.current_lane)

    if state_machine.should_switch():

        vehicles = controller.queue_lengths[next_lane]

        green_time = config.BASE_GREEN + int(vehicles * 2)
        green_time = max(config.MIN_GREEN,
                         min(config.MAX_GREEN, green_time))

        state_machine.switch(next_lane, green_time)
        hardware.set_signal(next_lane)

    remaining = int(
        state_machine.green_duration -
        (time.time() - state_machine.phase_start)
    )

    return jsonify({
        "active_lane": state_machine.current_lane,
        "queues": [int(q) for q in controller.queue_lengths],
        "remaining": max(0, remaining),
        "density": sum(controller.queue_lengths)
    })


@app.route("/video_feed/<int:cam_id>")
def video_feed(cam_id):

    def generate():
        while True:
            frame = latest_frames[cam_id]
            if frame is None:
                continue

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   frame_bytes + b"\r\n")

    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=False)