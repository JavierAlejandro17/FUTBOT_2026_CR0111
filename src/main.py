import cv2
from vision.ball_detector import BallDetector
from utils.kalman_filter import BallKalmanFilter

def main():
    cap = cv2.VideoCapture(0)
    detector = BallDetector()
    kalman = BallKalmanFilter()

    print("SISTEMA FUTBOT 2026 INICIADO...")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. Detectar balón (Cámara)
        ball_data = detector.detect(frame)

        # 2. Predecir con Kalman (IA)
        pred_x, pred_y = kalman.predict()

        # 3. Actualizar Filtro si hay detección real
        if ball_data:
            x, y, radius = ball_data
            kalman.update(x, y)
            # Dibujar Real
            cv2.circle(frame, (x, y), radius, (255, 0, 0), 2)

        # 4. Feedback Visual
        cv2.circle(frame, (pred_x, pred_y), 7, (0, 255, 0), -1) # Punto Verde IA
        cv2.imshow("FUTBOT MAIN CONTROL", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27: # 'q' o tecla ESC (27)
            print("\n[INFO] Deteniendo el sistema por usuario...")
            break

    # --- LIMPIEZA FINAL ---
    print("[INFO] Liberando cámara y cerrando ventanas...")
    cap.release()
    cv2.destroyAllWindows()
    
    # Pequeño truco para asegurar que las ventanas de OpenCV se cierren en Linux/Pi
    for i in range(5):
        cv2.waitKey(1)

    
if __name__ == "__main__":
    main()