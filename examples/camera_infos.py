"""
+---------------------------------------------------------------+
|         Kamera-Info Beispiel mit Python und asyncio           |
|---------------------------------------------------------------|
| Dieses Skript verbindet sich mit einer Kamera, liest Infos    |
| wie Position, Limits und Client-Anzahl aus und gibt sie aus.  |
| Danach wird das Programm beendet.                             |
+---------------------------------------------------------------+
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from tools.cam import Camera

load_dotenv()  # Umgebungsvariablen laden


async def main():
    sus_ip = os.getenv("SUS_IP", "127.0.0.1")
    cam = Camera(sus_ip)
    await cam.connect()

    pos = await cam.get_pos()
    print("Aktuelle Position:", pos)

    limits = await cam.get_limits()
    print("Positions-Limits:", limits)

    clients = await cam.client_count()
    print("Anzahl verbundener Clients:", clients)

    await cam.close()  # Stelle sicher, dass dies eine async def ist!


if __name__ == "__main__":
    asyncio.run(main())
