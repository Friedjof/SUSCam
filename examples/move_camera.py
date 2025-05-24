"""
+---------------------------------------------------------------+
|         Kamera bewegen Beispiel mit Python und asyncio        |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera und bewegt      |
| sie nacheinander in alle Richtungen.                          |
|                                                               |
| - Die Kamera-IP wird aus einer Umgebungsvariable gelesen.     |
| - Die Bewegungen werden mit kurzen Pausen ausgeführt.         |
| - Am Ende wird die Kamera wieder zentriert.                   |
|                                                               |
| Ideal für Einsteiger, um zu sehen, wie man eine Kamera        |
| per Code steuern kann.                                        |
+---------------------------------------------------------------+
"""

import sys
import os
import asyncio           # Für asynchrone Steuerung der Kamera
from time import sleep   # Für kurze Pausen zwischen den Bewegungen

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from tools.cam import Camera

load_dotenv()  # Umgebungsvariablen laden

async def main():
    sus_ip = os.getenv("SUS_IP", "127.0.0.1")  # IP-Adresse der Kamera holen
    cam = Camera(sus_ip)                       # Kamera-Objekt erstellen
    await cam.connect()                        # Mit der Kamera verbinden

    print("Kamera verbunden. Starte Bewegungen...")

    print("Bewege Kamera nach rechts...")
    await cam.right()                          # Kamera nach rechts bewegen
    sleep(1)                                   # 1 Sekunde warten
    print("Bewege Kamera nach links...")
    await cam.left()                           # Kamera nach links bewegen
    sleep(1)
    print("Bewege Kamera nach oben...")
    await cam.up()                             # Kamera nach oben bewegen
    sleep(1)
    print("Bewege Kamera nach unten...")
    await cam.down()                           # Kamera nach unten bewegen
    sleep(1)
    print("Centriere Kamera...")
    await cam.center()                         # Kamera zentrieren

if __name__ == "__main__":
    asyncio.run(main())

# Warum asyncio?
# Viele Kamerafunktionen sind asynchron, weil sie auf Antworten warten müssen.
# Mit asyncio kann das Programm weiterlaufen, ohne zu blockieren.
