import cv2
import numpy as np

class BallKalmanFilter:
    def __init__(self):
        # 4 estados: (x, y, vx, vy), 2 mediciones: (x, y)
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.1

   
    def predict(self):
        prediction = self.kf.predict()
        # prediction es una matriz de 4x1, tomamos los primeros dos elementos
        # Usamos [0][0] porque es un arreglo de arreglos
        pred_x = int(prediction[0][0])
        pred_y = int(prediction[1][0])
        return pred_x, pred_y

    def update(self, x, y):
        measurement = np.array([[np.float32(x)], [np.float32(y)]])
        self.kf.correct(measurement)