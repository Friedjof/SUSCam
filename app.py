"""
+---------------------------------------------------------------+
|           Kamera-Stream Hauptanwendung mit OpenCV             |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera und zeigt       |
| den Live-Stream im Fenster an.                                |
|                                                               |
| - Die Kamera-IP wird aus einer Umgebungsvariable gelesen.     |
| - Bilder werden mit OpenCV angezeigt.                         |
| - Mit der Taste 'q' kann das Fenster geschlossen werden.      |
|                                                               |
| Ideal als Hauptanwendung für den Kamera-Stream.               |
+---------------------------------------------------------------+
"""

import os
import cv2
import asyncio
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from tools.cam import Camera

load_dotenv()  # Lädt Umgebungsvariablen aus einer .env-Datei

# Callback-Funktion für empfangene Nachrichten von der Kamera
def my_msg_callback(msg: str, cam: Camera):
    print("Neue Nachricht:", msg)

# Callback-Funktion für empfangene Bilder von der Kamera
def my_img_callback(img: Image.Image, cam: Camera):
    # Bild von PIL.Image zu NumPy-Array konvertieren und Farbkanäle anpassen
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # Bild im Fenster anzeigen
    cv2.imshow("Kamera-Stream", img_cv)
    # Auf Tastendruck warten, Fenster bei 'q' schließen
    key = cv2.waitKey(1)
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
