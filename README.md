# 🚀 Real-Time Object Tracking & Counting with YOLOv8

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow.svg)

A production-grade, modular computer vision application that performs real-time object detection, tracking, and directional counting using **Ultralytics YOLOv8** and **OpenCV**.

---

## 📖 Overview

This project provides a robust solution for tracking objects (such as people, vehicles, etc.) as they cross a virtual horizontal line. It accurately counts how many unique objects moved "up" and how many moved "down," displaying these metrics alongside real-time FPS and bounding boxes.

### Key Features
- **Real-Time Inference:** Fast object detection using the lightweight YOLOv8 Nano model.
- **Robust Tracking:** Assigns unique IDs to objects to prevent double-counting.
- **Directional Counting:** Tracks whether an object crossed a virtual line moving upwards or downwards.
- **Modular Architecture:** Cleanly separated concerns (configuration, tracking logic, and rendering).
- **Fallback Mechanism:** Automatically falls back to webcam input if the specified video file is unavailable.
- **MySQL & Roboflow Ready:** Configuration file includes hooks for storing data in MySQL and loading custom models via Roboflow.

---

## 🏗️ Architecture

The codebase is organized into modular components for maintainability and scalability:

- `main.py`: The entry point. Handles the video ingestion loop, YOLO inference, and UI rendering.
- `tracker.py`: Contains the `ObjectTracker` class. Manages the history of object coordinates and determines line-crossing events.
- `config.py`: Centralized configuration. Manages API keys, model thresholds, database credentials, and spatial line coordinates.
- `requirements.txt`: Project dependencies.

---

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/object-tracking-counter.git
cd object-tracking-counter
```

### 2. Create a Virtual Environment (Optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Review and edit `config.py` to match your environment. 
- Adjust `COUNTING_LINE_Y` to fit your video resolution.
- Set `VIDEO_SOURCE` to a local `.mp4` file or `0` for the webcam.
- Add a `.env` file if you prefer not to hardcode credentials like your MySQL password or Roboflow API key.

---

## 🚀 Usage

Run the application with:
```bash
python main.py
```

### Controls
- **Press `q`** to quit the video stream and exit the application.

---

## 💡 Future Enhancements
- **Database Integration:** Push counting data directly to the configured MySQL database.
- **Polygon Counting Zones:** Replace the single line with complex polygon regions using `shapely`.
- **Custom Model Deployment:** Pull weights dynamically from Roboflow using the provided `ROBOFLOW_API_KEY`.

---
*Developed as part of a computer vision engineering portfolio.*
