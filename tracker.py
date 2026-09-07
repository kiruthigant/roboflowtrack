"""
Tracker module for managing object tracking and line crossing logic.
"""
from typing import Dict, List, Tuple, Any

class ObjectTracker:
    def __init__(self, line_y: int):
        """
        Initialize the ObjectTracker.

        Args:
            line_y (int): The y-coordinate of the horizontal counting line.
        """
        self.line_y = line_y
        self.track_history: Dict[int, List[Tuple[int, int]]] = {}
        self.counted_ids: set = set()
        self.count_up: int = 0
        self.count_down: int = 0

    def update(self, boxes: Any, track_ids: List[int]) -> Tuple[int, int]:
        """
        Update the tracker with new detections and check for line crossings.

        Args:
            boxes: The bounding boxes from YOLOv8 (xyxy format).
            track_ids (List[int]): The tracking IDs for the bounding boxes.

        Returns:
            Tuple[int, int]: Current count of objects moving (up, down).
        """
        if track_ids is None or len(track_ids) == 0:
            return self.count_up, self.count_down

        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = box.tolist()
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Store track history
            if track_id not in self.track_history:
                self.track_history[track_id] = []
            
            self.track_history[track_id].append((center_x, center_y))

            # Keep only the last 30 positions
            if len(self.track_history[track_id]) > 30:
                self.track_history[track_id].pop(0)

            # Line crossing logic
            if len(self.track_history[track_id]) >= 2:
                prev_y = self.track_history[track_id][-2][1]
                curr_y = self.track_history[track_id][-1][1]

                if track_id not in self.counted_ids:
                    # Check if it crossed the line
                    if prev_y < self.line_y and curr_y >= self.line_y:
                        # Moved down
                        self.count_down += 1
                        self.counted_ids.add(track_id)
                    elif prev_y > self.line_y and curr_y <= self.line_y:
                        # Moved up
                        self.count_up += 1
                        self.counted_ids.add(track_id)

        return self.count_up, self.count_down
