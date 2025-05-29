"""
+---------------------------------------------------------------+
|               Kamera-Stream mit Gesichtserkennung             |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera (lokale oder    |
| Netzwerkkamera) und zeigt den Live-Stream in einem Fenster    |
| an. Gesichter werden mit MediaPipe Face Detection erkannt     |
| und visualisiert.                                             |
|                                                               |
| Funktionen:                                                   |
| - Erkennung von Gesichtern im Kamera-Feed                     |
| - Anzeige eines Rechtecks um erkannte Gesichter               |
| - Markierung des Gesichtszentrums und Bildmittelpunkts        |
| - Visualisierung der Verbindungslinie zwischen Gesichts-      |
|   und Bildmittelpunkt                                         |
| - Anzeige der Erkennungsgenauigkeit (Konfidenz)               |
| - Statusanzeige im Bild                                       |
|                                                               |
| Steuerung:                                                    |
| - Mit der Taste 'q' kann das Programm beendet werden          |
+---------------------------------------------------------------+
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import asyncio
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from tools.cam import Camera
import mediapipe as mp

load_dotenv()  # Lädt Umgebungsvariablen aus einer .env-Datei

# MediaPipe-Komponenten für Gesichtserkennung initialisieren
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Callback-Funktion für Statusinformationen von der Kamera
def my_msg_callback(msg: str, cam: Camera):
    print("Neue Kamera-Nachricht:", msg)

# Callback-Funktion für Bildverarbeitung
def my_img_callback(img: Image.Image, cam: Camera):
    # Bild von PIL.Image-Format zu NumPy-Array für OpenCV konvertieren
    img_np = np.array(img)
    # Farbkanäle von RGB (PIL-Standard) zu BGR (OpenCV-Standard) umwandeln
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # MediaPipe Face Detection für das aktuelle Bild anwenden
    with mp_face_detection.FaceDetection(
            model_selection=0,  # 0: Nahbereich-Modell für Gesichter nahe an der Kamera
            min_detection_confidence=0.5  # Erkennungsschwellwert (0.0-1.0)
    ) as face_detection:
        # Bild für MediaPipe von BGR zurück zu RGB konvertieren (MediaPipe erwartet RGB)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)

        # Verarbeitung der erkannten Gesichter
        if results.detections:
            for detection in results.detections:
                # Begrenzungsrahmen (Bounding Box) des Gesichts extrahieren
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = img_bgr.shape

                # Relative Koordinaten in absolute Pixelkoordinaten umrechnen
                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                width = int(bboxC.width * w)
                height = int(bboxC.height * h)

                # Grünes Rechteck um das erkannte Gesicht zeichnen
                cv2.rectangle(img_bgr, (x, y), (x + width, y + height), (0, 255, 0), 2)

                # Zentrum des erkannten Gesichts berechnen und als roter Punkt markieren
                face_center_x = x + width // 2
                face_center_y = y + height // 2
                cv2.circle(img_bgr, (face_center_x, face_center_y), 5, (0, 0, 255), -1)

                # Bildmittelpunkt berechnen und als roter Punkt markieren
                img_center_x = img_rgb.shape[1] // 2
                img_center_y = img_rgb.shape[0] // 2
                cv2.circle(img_bgr, (img_center_x, img_center_y), 5, (0, 0, 255), -1)

                # Blaue Linie zwischen Gesichtszentrum und Bildmittelpunkt zeichnen
                cv2.line(img_bgr, (face_center_x, face_center_y), (img_center_x, img_center_y), (255, 0, 0), 2)

                face_diff_x = face_center_x - img_center_x
                face_diff_y = face_center_y - img_center_y

                # Zeigt die Differenz zwischen Gesichtszentrum und Bildzentrum an
                cv2.putText(img_bgr, f"Diff X: {face_diff_x}, Y: {face_diff_y}", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Erkennungsgenauigkeit (Konfidenz) im Bild anzeigen
                confidence = detection.score[0]
                cv2.putText(img_bgr, f"Konfidenz: {confidence:.2f}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Statusmeldung im Bild anzeigen und in Konsole ausgeben
                cv2.putText(img_bgr, "Gesicht erkannt", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Gesicht erkannt!")
        else:
            # Statusmeldung wenn kein Gesicht erkannt wurde
            cv2.putText(img_bgr, "Kein Gesicht erkannt", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Aktuelles Bild mit Visualisierungen im Fenster anzeigen
    cv2.imshow("Kamera-Stream mit Gesichtserkennung", img_bgr)

    # Kurz auf Tastendruck warten (1ms) für Fensteraktualisierung und Nutzerinteraktion
    key = cv2.waitKey(1)
    # Programm beenden wenn 'q' gedrückt wird
    if key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)

# Hauptfunktion: Kameraverbindung herstellen und Verarbeitung starten
async def main():
    sus_ip = os.getenv("SUS_IP", "127.0.0.1") # Standard-IP der Kamera aus Umgebungsvariablen lesen
    cam = Camera(sus_ip)  # Kamera-Objekt mit der angegebenen IP initialisieren

    # Callbacks für Kameranachrichten und Bildverarbeitung registrieren
    cam.set_msg_callback(my_msg_callback)
    cam.set_img_callback(my_img_callback)

    # Verbindung zur Kamera herstellen
    await cam.connect()

    # Programm weiterlaufen lassen, um Callbacks zu ermöglichen
    while True:
        await asyncio.sleep(1)

# Skript direkt ausführen
if __name__ == "__main__":
    asyncio.run(main())
