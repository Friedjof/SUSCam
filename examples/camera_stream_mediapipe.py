"""
+---------------------------------------------------------------+
|           Kamera-Stream Beispiel mit MediaPipe                |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera und zeigt       |
| den Live-Stream im Fenster an. Hände werden mit MediaPipe     |
| erkannt und im Bild markiert.                                 |
|                                                               |
| - Die Kamera-IP wird aus einer Umgebungsvariable gelesen.     |
| - Bilder werden mit OpenCV angezeigt.                         |
| - Mit der Taste 'q' kann das Fenster geschlossen werden.      |
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

# Initialisiere MediaPipe-Komponenten für Handerkennung und Zeichnen
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Callback-Funktion für empfangene Nachrichten von der Kamera
def my_msg_callback(msg):
    print("Neue Nachricht:", msg)

# Callback-Funktion für empfangene Bilder von der Kamera
def my_img_callback(img):
    # Bild von PIL.Image zu NumPy-Array konvertieren
    img_np = np.array(img)
    # Farbkanäle von RGB (PIL) zu BGR (OpenCV) umwandeln
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # MediaPipe Hands-Objekt für die Handerkennung erzeugen
    # Wird für jedes Bild neu erzeugt (alternativ: global initialisieren für Effizienz)
    with mp_hands.Hands(
        static_image_mode=False,         # Für Videostreams: False
        max_num_hands=2,                # Maximal 2 Hände erkennen
        min_detection_confidence=0.5     # Mindest-Konfidenz für Erkennung
    ) as hands:
        # Bild für MediaPipe von BGR zurück zu RGB konvertieren
        results = hands.process(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        # Wenn mindestens eine Hand erkannt wurde
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Zeichnet die erkannten Hand-Landmarks und Verbindungen ins Bild
                mp_drawing.draw_landmarks(
                    img_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

    # Zeigt das aktuelle Bild mit erkannten Händen im Fenster an
    cv2.imshow("Kamera-Stream mit MediaPipe", img_bgr)
    # Wartet kurz auf Tastendruck, damit das Fenster aktualisiert wird
    key = cv2.waitKey(1)
    # Wenn die Taste 'q' gedrückt wird, Fenster schließen und Programm beenden
    if key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)

# Hauptfunktion: Verbindet sich mit der Kamera und startet den Stream
async def main():
    sus_ip = os.getenv("SUS_IP", "127.0.0.1")  # Kamera-IP aus Umgebungsvariable
    cam = Camera(sus_ip)                       # Kamera-Objekt erzeugen

    cam.set_msg_callback(my_msg_callback)      # Setzt Callback für Nachrichten
    cam.set_img_callback(my_img_callback)      # Setzt Callback für Bilder

    await cam.connect()                        # Stellt Verbindung zur Kamera her
    while True:
        await asyncio.sleep(1)                 # Hält das Programm am Laufen

# Startet das Skript, wenn es direkt ausgeführt wird
if __name__ == "__main__":
    asyncio.run(main())
