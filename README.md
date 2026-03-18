# 🚦 AI-Based Adaptive Traffic Signal Control System

## 📌 Overview
This project presents an **AI-based adaptive traffic signal control system** that dynamically adjusts traffic signal timing using real-time vehicle detection. The system leverages **YOLOv8 object detection** to analyze traffic density from live video feeds and optimize signal allocation.

---

## 🎯 Problem Statement
Traditional traffic signals operate on fixed timing, leading to:
- Traffic congestion
- Increased waiting time
- Fuel wastage
- Poor emergency handling

This project solves these issues by introducing **real-time, data-driven signal control**.

---

## ⚙️ Key Features
- 🚗 Real-time vehicle detection using YOLOv8
- 📊 Dynamic traffic density estimation
- ⏱️ Adaptive signal timing based on vehicle count
- 🔁 Vehicle tracking to avoid duplicate counting
- 🚑 Emergency vehicle detection (ambulance priority)
- 🛑 Fail-safe system (fallback to fixed timing)

---

## 🧠 Tech Stack
- **Programming:** Python  
- **AI/ML:** YOLOv8 (Ultralytics), CNN  
- **Computer Vision:** OpenCV  
- **Backend:** Flask  
- **Frontend:** HTML, CSS, JavaScript  

---

## 🏗️ System Architecture
Camera Input → OpenCV → YOLOv8 Model → Vehicle Detection →
Tracking & Counting → Traffic Algorithm → Flask Backend → Dashboard Output

---

## 🔍 How It Works

1. **Video Capture:** Traffic video is captured using cameras.
2. **Frame Processing:** Frames are processed using OpenCV.
3. **Vehicle Detection:** YOLOv8 detects vehicles with bounding boxes and class labels.
4. **Tracking:** Vehicles are tracked to prevent duplicate counting.
5. **Queue Estimation:** Traffic density is calculated using smoothing techniques.
6. **Decision Making:** Lane priority is calculated based on vehicle count and waiting time.
7. **Signal Control:** Green signal time is dynamically adjusted.

---

## 📈 Sample Logic

- **Priority Calculation:**
Priority = α × Queue + β × Waiting Time
- **Green Time Calculation:**
GreenTime = BaseTime + (Vehicles × 2)

---

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AshutoshG04/Adaptive-Traffic-Signal-System-Based-on-Vehicle-Density.git
cd Adaptive-Traffic-System
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
python app.py

📁 Project Structure
Adaptive-Traffic-System/
│
├── app.py
├── vision_engine.py
├── traffic_controller.py
├── tracker_engine.py
├── queue_estimator.py
├── detection.py
├── config.py
│
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .gitignore

📊 Results

Achieved ~85% vehicle detection accuracy
Improved traffic flow using adaptive signal timing
Reduced unnecessary waiting time

🔮 Future Enhancements

Integration with IoT-based traffic signals (ESP32/PLC)
Multi-intersection traffic coordination
Cloud deployment for smart city integration
Real-time analytics dashboard

👨‍💻 Author

Ashutosh Ghodke
GitHub: https://github.com/AshutoshG04

⭐ If you like this project
Give it a ⭐ on GitHub!
