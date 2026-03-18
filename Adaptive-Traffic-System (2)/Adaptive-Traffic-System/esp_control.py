import serial
import time

esp=None

try:
    esp = serial.Serial("COM5",115200,timeout=1)
    time.sleep(2)
    print("✅ ESP Connected")
except:
    print("❌ ESP Not Connected")


last_sent_lane = None


def send_lane(lane):

    global last_sent_lane

    if esp is None:
        return

    # Prevent spam sending
    if lane == last_sent_lane:
        return

    try:
        msg=f"{lane}\n"
        esp.write(msg.encode())
        print(f"Lane Sent → {lane}")

        last_sent_lane = lane

    except Exception as e:
        print("ESP Error:",e)