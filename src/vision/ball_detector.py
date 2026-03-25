import cv2
import numpy as np

class BallDetector:
    def __init__(self):
        # Rango Naranja (Ajustable)
        self.low_orange = np.array([5, 150, 150])
        self.high_orange = np.array([15, 255, 255])

    def detect(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.low_orange, self.high_orange)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10:
                return int(x), int(y), int(radius)
        return None