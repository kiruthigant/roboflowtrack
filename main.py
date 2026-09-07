"""
Main application loop for video processing, object detection, and rendering.
"""
import cv2
import time
from ultralytics import YOLO
import config
from tracker import ObjectTracker

def draw_info(frame, count_up, count_down, fps):
    """
    Draw counts and FPS on the frame.
    """
    # Define text and parameters
    text_up = f"Up: {count_up}"
    text_down = f"Down: {count_down}"
    text_fps = f"FPS: {fps:.1f}"

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color_text = (255, 255, 255)
    color_bg = (0, 0, 0)

    # Put background rectangles and text
    cv2.rectangle(frame, (20, 20), (250, 140), color_bg, -1)
    cv2.putText(frame, text_up, (30, 60), font, font_scale, (0, 255, 0), thickness)
    cv2.putText(frame, text_down, (30, 100), font, font_scale, (0, 0, 255), thickness)
    cv2.putText(frame, text_fps, (30, 130), font, 0.7, color_text, thickness)

    # Draw the counting line
    cv2.line(frame, 
             (config.COUNTING_LINE_START_X, config.COUNTING_LINE_Y), 
             (config.COUNTING_LINE_END_X, config.COUNTING_LINE_Y), 
             (255, 0, 0), 2)
    cv2.putText(frame, "Counting Line", (config.COUNTING_LINE_START_X, config.COUNTING_LINE_Y - 10), 
                font, 0.5, (255, 0, 0), 1)

def main():
    """
    Main execution function.
    """
    # Load YOLOv8 model
    try:
        model = YOLO(config.YOLO_MODEL_WEIGHTS)
        print(f"Loaded model {config.YOLO_MODEL_WEIGHTS} successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Open video source
    video_source = config.VIDEO_SOURCE
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Failed to open {video_source}. Falling back to webcam ({config.FALLBACK_VIDEO_SOURCE}).")
        cap = cv2.VideoCapture(config.FALLBACK_VIDEO_SOURCE)
        if not cap.isOpened():
            print("Failed to open webcam. Exiting.")
            return

    # Initialize tracker
    tracker = ObjectTracker(line_y=config.COUNTING_LINE_Y)

    # Variables for FPS calculation
    prev_time = 0

    print("Starting video processing loop. Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("End of video stream or failed to grab frame.")
            break

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
        prev_time = current_time

        # Run inference and tracking
        # persist=True enables tracking
        results = model.track(frame, persist=True, conf=config.CONFIDENCE_THRESHOLD, classes=config.TARGET_CLASSES, verbose=False)
        
        count_up, count_down = tracker.count_up, tracker.count_down

        if results and len(results) > 0 and results[0].boxes:
            boxes = results[0].boxes.xyxy.cpu()
            
            # tracking IDs might be None if no objects are tracked yet
            track_ids = results[0].boxes.id
            if track_ids is not None:
                track_ids = track_ids.int().cpu().tolist()
                count_up, count_down = tracker.update(boxes, track_ids)

            # Draw bounding boxes
            annotated_frame = results[0].plot()
        else:
            annotated_frame = frame

        # Overlay custom UI elements (counts, line, fps)
        draw_info(annotated_frame, count_up, count_down, fps)

        # Show the frame
        cv2.imshow("Object Tracking Counter", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
