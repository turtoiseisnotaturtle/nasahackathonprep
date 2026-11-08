import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'models', 'hand_landmarker.task')

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.cap = cv2.VideoCapture(0)

    def get_frame_landmarks(self, timestamp_ms):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None, None

        # Convert image format BGR -> RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Explicitly build mp.Image from contiguous numpy array
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect hand landmarks using timestamp in milliseconds
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks and len(result.hand_landmarks) > 0:
            hand = result.hand_landmarks[0]
            wrist = hand[0]
            thumb_tip = hand[4]
            index_tip = hand[8]
            return frame, {
                'wrist': (wrist.x, wrist.y),
                'thumb': (thumb_tip.x, thumb_tip.y),
                'index': (index_tip.x, index_tip.y)
            }

        return frame, None

    def release(self):
        self.cap.release()