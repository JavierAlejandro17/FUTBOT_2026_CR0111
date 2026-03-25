from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
cap = cv2.VideoCapture(0)

# Variables globales para telemetría
ball_x = 0
robot_status = "IDLE"

def gen_frames():
    global ball_x
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # --- AQUÍ VA TU LÓGICA DE VISIÓN EXISTENTE ---
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # (Simplificado para el ejemplo)
            lower = np.array([5, 150, 150])
            upper = np.array([15, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Buscamos contornos y actualizamos ball_x para la telemetría
            contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
            if contours:
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                ball_x = x + (w//2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Codificar el frame en JPEG para enviarlo por la web
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Página principal que muestra el video y los datos
    return f"""
    <html>
        <head><title>FUTBOT 2026 Monitor</title></head>
        <body>
            <h1>Panel de Monitoreo - Robot UPIITA</h1>
            <img src="/video_feed" width="50%">
            <hr>
            <h3>Telemetría en tiempo real:</h3>
            <p>Posición Balón X: <b>{ball_x}</b></p>
            <p>Estado del Robot: <b>{robot_status}</b></p>
            <script>setTimeout(function(){{location.reload();}}, 500);</script>
        </body>
    </html>
    """
    

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Ejecutar en la IP de la Raspberry, puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=False)