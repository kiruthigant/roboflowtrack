"""
Configuration settings for the Object Tracking Counter project.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- ROBOFLOW GATEWAY ---
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "")
ROBOFLOW_WORKSPACE = os.getenv("ROBOFLOW_WORKSPACE", "")
ROBOFLOW_PROJECT = os.getenv("ROBOFLOW_PROJECT", "")
ROBOFLOW_VERSION = int(os.getenv("ROBOFLOW_VERSION", "8"))

# --- STORAGE ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "warehousescandb")

# --- MODEL SETTINGS ---
YOLO_MODEL_WEIGHTS = "yolov8n.pt"  # Use Ultralytics YOLOv8 nano model
CONFIDENCE_THRESHOLD = 0.5

# --- VIDEO SETTINGS ---
VIDEO_SOURCE = "test_video.mp4" # Can be a path to an mp4 file or 0 for webcam
FALLBACK_VIDEO_SOURCE = 0

# --- COUNTING LINE SETTINGS ---
# Define a horizontal counting line. Format: (x1, y1), (x2, y2)
# Ensure to adjust these values based on your video resolution
COUNTING_LINE_Y = 300 # The Y-coordinate for the horizontal line
COUNTING_LINE_START_X = 100
COUNTING_LINE_END_X = 1000

# Classes to track (e.g., 0 for person, 2 for car)
# Set to None to track all classes
TARGET_CLASSES = [0, 2] 
