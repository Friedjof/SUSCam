"""
+---------------------------------------------------------------+
|           Kamera-Stream Beispiel mit OpenCV und Python        |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera und zeigt       |
| den Live-Stream im Fenster an.                                |
|                                                               |
| - Die Kamera-IP wird aus einer Umgebungsvariable gelesen.     |
| - Bilder werden mit OpenCV angezeigt.                         |
| - Mit der Taste 'q' kann das Fenster geschlossen werden.      |
|                                                               |
| Ideal für Einsteiger, um zu sehen, wie man eine Kamera        |
| ansteuert und Bilder live anzeigen kann.                      |
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

load_dotenv()  # Lädt Umgebungsvariablen aus einer .env-Datei

# Wird aufgerufen, wenn eine Nachricht von der Kamera kommt
def my_msg_callback(msg):
    print("Neue Nachricht:", msg)

# Wird aufgerufen, wenn ein neues Bild von der Kamera kommt
def my_img_callback(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # Bild für OpenCV umwandeln
    cv2.imshow("Kamera-Stream", img_cv)                      # Bild anzeigen
    key = cv2.waitKey(1)                                     # Auf Tastendruck warten
    if key & 0xFF == ord('q'):                               # Bei 'q' beenden
        cv2.destroyAllWindows()
        exit(0)

# Hauptfunktion, startet die Verbindung zur Kamera
async def main():
    sus_ip = os.getenv("SUS_IP", "127.0.0.1")  # IP-Adresse holen, Standard ist localhost
    cam = Camera(sus_ip)                       # Kamera-Objekt erstellen

    cam.set_msg_callback(my_msg_callback)      # Nachricht-Callback setzen
    cam.set_img_callback(my_img_callback)      # Bild-Callback setzen

    await cam.connect()                        # Mit Kamera verbinden
    while True:
        await asyncio.sleep(1)                 # Programm läuft weiter

if __name__ == "__main__":
    asyncio.run(main())                        # Startet das Programm
