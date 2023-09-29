
import mediapipe as mp

class GameSettings:
    def __init__(self):
        self.frameWidth = 1280
        self.frameHeight = 9*self.frameWidth/16
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6)
