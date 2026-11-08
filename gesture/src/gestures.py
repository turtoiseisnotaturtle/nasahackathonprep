import math
import time
from collections import deque

class GestureDetector:
    def __init__(self):
        # Pinch state tracker
        self.is_pinching = False

        # Swipe tracking window (stores last 10 X coordinates)
        self.x_history = deque(maxlen=10)
        self.last_swipe_time = 0
        self.swipe_cooldown = 0.6  # Seconds before another swipe fires

        # Pointer smoothing (Low-Pass Filter)
        self.smoothed_x = None
        self.smoothed_y = None
        self.alpha = 0.3  # Lower values = smoother, higher = more responsive

    def process_frame(self, landmarks):
        if not landmarks:
            return []

        events = []
        now = time.time()

        thumb = landmarks['thumb']
        index = landmarks['index']
        wrist = landmarks['wrist']

        # ------------------------------------------
        # 1. Pinch State Machine Implementation
        # ------------------------------------------
        dist = math.hypot(index[0] - thumb[0], index[1] - thumb[1])
        if dist < 0.05:  # Close enough to consider a pinch
            if not self.is_pinching:
                self.is_pinching = True
                events.append(('PINCH_START', None))
            else:
                events.append(('PINCH_HOLD', None))
        else:
            if self.is_pinching:
                self.is_pinching = False
                events.append(('PINCH_RELEASE', None))

        # ------------------------------------------
        # 2. Swipe Detection Implementation
        # ------------------------------------------
        self.x_history.append(wrist[0])
        if len(self.x_history) == 10 and (now - self.last_swipe_time) > self.swipe_cooldown:
            delta_x = self.x_history[-1] - self.x_history[0]
            if delta_x > 0.15:  # Hand moved rapidly to the right
                events.append(('SWIPE_RIGHT', None))
                self.last_swipe_time = now
                self.x_history.clear()
            elif delta_x < -0.15:  # Hand moved rapidly to the left
                events.append(('SWIPE_LEFT', None))
                self.last_swipe_time = now
                self.x_history.clear()

        # ------------------------------------------
        # 3. Pointer Smoothing Implementation
        # ------------------------------------------
        if self.smoothed_x is None:
            self.smoothed_x, self.smoothed_y = index[0], index[1]
        else:
            self.smoothed_x = self.alpha * index[0] + (1 - self.alpha) * self.smoothed_x
            self.smoothed_y = self.alpha * index[1] + (1 - self.alpha) * self.smoothed_y

        events.append(('POINTER', (self.smoothed_x, self.smoothed_y)))
        return events