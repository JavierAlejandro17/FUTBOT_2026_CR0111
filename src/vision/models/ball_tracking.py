import cv2  #Cargamos librerias necesarias
import numpy as np


def main(): #Creamos una función, la primera para hacer pruebas de detección del balón
    # Inicializar la cámara 0, por defecto es la de la computadora
    cap = cv2.VideoCapture(0) #definimos la variable cap, que será la captura de video de nuestra camara

    # Definir el rango de color del balón ( Naranja en HSV)
    # Estos valores se deben ajustar según la iluminación de la cancha, hacer pruebas futuras
    orange_lower = np.array([5, 150, 150]) #ver https://es.wikipedia.org/wiki/Modelo_de_color_HSV para entender el modelo HSV
    orange_upper = np.array([15, 255, 255]) #Se escala el modelo a valores de 0 a 255 que equivale a 8 bits de informacion

    while True: #Que se ejecute sin parar
        ret, frame = cap.read() #ret = detección en booleano, 1 se detecta, 0 no se detecta, barrera de seguridad de camara frame = arreglo de pixeles Si tu resolución es 640x480, es una matriz de $640 \times 480$ píxeles, donde cada píxel tiene 3 valores: Azul, Verde y Rojo (BGR).
        if not ret: #sino se detecta la camara, todo se muere
            break

        # 1. Convertir a espacio de color HSV (más robusto que RGB)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Pasa de RGB por defecto a HSV es con libreria de opencv

        # 2. MÁSCAR
        mask = cv2.inRange(hsv, orange_lower, orange_upper) #Solo deja pasar la información de la imagen en el rango especificado

        # 3. Limpiar ruido (Erosión y Dilatación)
        mask = cv2.erode(mask, None, iterations=2) #filtro de promedio para eliminar picos de alta frecuencia o ruido de vision no deseado.
        mask = cv2.dilate(mask, None, iterations=2)#Agranda las zonas blancas que quedaron. Si el balón tenía "huecos" negros por un reflejo, la dilatación los rellena para que el objeto se vea sólido otra vez.

        # 4. Encontrar contornos
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Solo guarda un contorno por objeto y se APROXIMA a la figura más simple respecto a la geometría

        if len(contours) > 0: #Valida que existe un contorno y tiene una longitud mayor a cero
            # Encontrar el contorno más grande (el balón)
            c = max(contours, key=cv2.contourArea) #Tomamos la circunferencia del balon como el maximo contorno
            ((x, y), radius) = cv2.minEnclosingCircle(c) #Geometrización

            if radius > 10: #Threshold
                # Dibujar el círculo y el centro en el frame
                cv2.circle(frame, (int(x), int(y)),
                           int(radius), (255, 0, 0), 2)
                cv2.putText(frame, "BALON", (int(x-10), int(y-10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Aquí es donde enviarías la 'x' a la lógica de motores
                print(f"Balón detectado en X: {x}")

        # Mostrar los resultados
        cv2.imshow("FUTBOT Vision", frame)
        cv2.imshow("Mascara", mask)

        # Escuchar teclado: Si presionas 'q' o 'ESC', se cierra
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27: # 27 = tecla ESC ord('q'): Convierte el carácter 'q' a su valor numérico ASCII.
            print("Cerrando sistema de visión...")
            break

    cap.release() #Corta comunicación de CÓDIGO -- CÁMARA
    cv2.destroyAllWindows() # Cierra todas las ventanas
    for i in range(5):
        cv2.waitKey(1)


if __name__ == "__main__":  #Si el script se ejecuta directamente, entonces ejecutar, sino esperar ordenes
    main()
