"""
+---------------------------------------------------------------+
|                Camera-Klasse für SUSCam-Projekt               |
|---------------------------------------------------------------|
| Diese Bibliothek stellt eine Camera-Klasse bereit, mit der    |
| man eine Kamera über WebSockets steuern und Bilder empfangen  |
| kann. Es gibt auch einen Fallback-Modus für lokale Tests.     |
|                                                               |
| - Kamera bewegen (up, down, left, right, center, set_position)|
| - Bilddaten empfangen (mit Callback)                          |
| - Licht steuern (light_on, light_off)                         |
| - Position und Limits abfragen                                |
|                                                               |
| Ideal für Einsteiger und Fortgeschrittene zur Kamerasteuerung.|
+---------------------------------------------------------------+
"""

import io
import json
from PIL import Image
import asyncio
import websockets
import time

try:
    import cv2
except ImportError:
    cv2 = None

# Positions- und Limit-Konstanten
START_POS_X = 90
MIN_POS_X = 0
MAX_POS_X = 180

START_POS_Y = 45
MIN_POS_Y = 0
MAX_POS_Y = 90


class Camera:
    """
    Klasse zur Steuerung und Abfrage einer Kamera über WebSockets.
    Unterstützt auch einen Fallback-Modus mit der lokalen Webcam.
    """

    def __init__(self, ip, fallback=False):
        """
        Erstellt ein Camera-Objekt.

        Args:
            ip (str): IP-Adresse der Kamera.
            fallback (bool): Fallback-Modus aktivieren (lokale Webcam).
        """
        self.uri = f"ws://{ip}/ws"
        self.ws = None
        self.img_callback = None
        self.msg_callback = None
        self._fallback = fallback
        self.cap = None  # Für Fallback-Modus

        # Position und Limits für Fallback
        self._x = START_POS_X
        self._y = START_POS_Y

    def __del__(self):
        """
        Destruktor: Schließt ggf. offene Verbindungen und gibt Ressourcen frei.
        """
        if self.ws:
            try:
                asyncio.get_event_loop().run_until_complete(self.close())
            except Exception:
                pass
        if self.cap:
            self.cap.release()

    def set_img_callback(self, callback):
        """
        Setzt die Callback-Funktion für empfangene Bilder.

        Args:
            callback (function): Funktion, die ein PIL.Image-Objekt entgegennimmt.
        """
        self.img_callback = callback

    def set_msg_callback(self, callback):
        """
        Setzt die Callback-Funktion für empfangene Nachrichten.

        Args:
            callback (function): Funktion, die eine Nachricht entgegennimmt.
        """
        self.msg_callback = callback

    def _on_message(self, message):
        """
        Interne Methode: Verarbeitet eingehende Nachrichten und ruft die passenden Callbacks auf.
        """
        if isinstance(message, bytes):
            if self.img_callback:
                try:
                    img = Image.open(io.BytesIO(message))
                    self.img_callback(img)
                except Exception as e:
                    print("Fehler beim Laden des Bildes:", e)
        else:
            try:
                data = json.loads(message)
                if self.msg_callback:
                    self.msg_callback(data)
            except Exception:
                if self.msg_callback:
                    self.msg_callback(message)

    async def listen(self):
        """
        Lauscht auf neue Nachrichten/Bilder von der Kamera und ruft die Callbacks auf.
        Im Fallback-Modus werden periodisch Bilder von der lokalen Webcam geholt.
        """
        if self._fallback:
            # Im Fallback-Modus: periodisch Bild holen und Callback aufrufen
            if self.cap and self.img_callback:
                while True:
                    ret, frame = self.cap.read()
                    if ret:
                        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        self.img_callback(img)
                    await asyncio.sleep(0.05)  # ca. 20 FPS
            else:
                while True:
                    await asyncio.sleep(1)
            return
        while True:
            msg = await self.recv()
            self._on_message(msg)

    def loop(self):
        """
        Startet eine Endlosschleife zur Kommunikation mit der Kamera (synchron).
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self.close())

    async def connect(self):
        """
        Stellt die Verbindung zur Kamera her (oder startet Fallback).
        """
        try:
            if self._fallback:
                print("Fallback-Modus aktiviert, keine WebSocket-Verbindung.")
                if cv2:
                    self.cap = cv2.VideoCapture(0)
                asyncio.create_task(self.listen())  # Starte Fallback-Loop!
                return

            print(f"Verbinde zu {self.uri}...")
            print("Versuche, WebSocket-Verbindung herzustellen...")
            self.ws = await websockets.connect(self.uri)
            await self.get_limits()
            await self.get_pos()

            print("WebSocket-Verbindung erfolgreich hergestellt.")

            asyncio.create_task(self.listen())
            print("Starte Listener für Nachrichten und Bilder...")
        except Exception as e:
            print("WebSocket-Verbindung fehlgeschlagen, Fallback-Modus wird aktiviert:", e)
            self._fallback = True
            if cv2:
                self.cap = cv2.VideoCapture(0)
            else:
                print("OpenCV nicht verfügbar, kein Kamerafallback möglich.")
            asyncio.create_task(self.listen())  # Starte Fallback-Loop auch bei Fehler!

    async def send(self, msg):
        """
        Sendet eine Nachricht an die Kamera.

        Args:
            msg (str oder dict): Nachricht oder Befehl.
        """
        if self._fallback:
            print(f"[Fallback] send: {msg}")
            return
        if isinstance(msg, dict):
            await self.ws.send(json.dumps(msg))
        else:
            await self.ws.send(msg)

    async def recv(self):
        """
        Empfängt eine Nachricht von der Kamera.

        Returns:
            str: Empfangene Nachricht.
        """
        if self._fallback:
            print("[Fallback] recv aufgerufen")
            return None
        return await self.ws.recv()

    async def getframe(self):
        """
        Fordert ein aktuelles Bild von der Kamera an.

        Returns:
            PIL.Image oder bytes: Bilddaten.
        """
        if self._fallback and self.cap:
            ret, frame = self.cap.read()
            if ret:
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                return img
            else:
                print("[Fallback] Kein Bild von interner Kamera erhalten.")
                return None
        await self.send("getframe")
        data = await self.recv()
        return data

    async def center(self):
        """
        Zentriert die Kamera (Position auf Mittelstellung).
        """
        if self._fallback:
            self._x = START_POS_X
            self._y = START_POS_Y
            print(f"[Fallback] center: x={self._x}, y={self._y}")
            return
        await self.send("center")

    async def up(self):
        """
        Bewegt die Kamera nach oben.
        """
        if self._fallback:
            if self._y > MIN_POS_Y:
                self._y = max(MIN_POS_Y, self._y - 1)
            print(f"[Fallback] up: x={self._x}, y={self._y}")
            return
        await self.send("up")

    async def down(self):
        """
        Bewegt die Kamera nach unten.
        """
        if self._fallback:
            if self._y < MAX_POS_Y:
                self._y = min(MAX_POS_Y, self._y + 1)
            print(f"[Fallback] down: x={self._x}, y={self._y}")
            return
        await self.send("down")

    async def left(self):
        """
        Bewegt die Kamera nach links.
        """
        if self._fallback:
            if self._x > MIN_POS_X:
                self._x = max(MIN_POS_X, self._x - 1)
            print(f"[Fallback] left: x={self._x}, y={self._y}")
            return
        await self.send("left")

    async def right(self):
        """
        Bewegt die Kamera nach rechts.
        """
        if self._fallback:
            if self._x < MAX_POS_X:
                self._x = min(MAX_POS_X, self._x + 1)
            print(f"[Fallback] right: x={self._x}, y={self._y}")
            return
        await self.send("right")

    async def get_pos(self):
        """
        Fragt die aktuelle Position der Kamera ab.

        Returns:
            dict: Aktuelle Position (x, y).
        """
        if self._fallback:
            print(f"[Fallback] get_pos: x={self._x}, y={self._y}")
            return {"x": self._x, "y": self._y}
        await self.send("get_pos")
        msg = await self.recv()
        return json.loads(msg)

    async def client_count(self):
        """
        Fragt die Anzahl der verbundenen Clients ab.

        Returns:
            int: Anzahl der Clients.
        """
        if self._fallback:
            print("[Fallback] client_count")
            return 1
        await self.send("client_count")
        msg = await self.recv()
        return json.loads(msg)

    async def get_limits(self):
        """
        Fragt die Positionsgrenzen der Kamera ab.

        Returns:
            dict: Limits für x und y.
        """
        if self._fallback:
            print("[Fallback] get_limits")
            return {
                "x_min": MIN_POS_X, "x_max": MAX_POS_X,
                "y_min": MIN_POS_Y, "y_max": MAX_POS_Y
            }
        await self.send("get_limits")
        msg = await self.recv()
        return json.loads(msg)

    async def light_on(self):
        """
        Schaltet das Licht der Kamera ein.
        """
        if self._fallback:
            print("[Fallback] light_on")
            return
        await self.send("light_on")

    async def light_off(self):
        """
        Schaltet das Licht der Kamera aus.
        """
        if self._fallback:
            print("[Fallback] light_off")
            return
        await self.send("light_off")

    async def set_position(self, x, y):
        """
        Setzt die Kamera auf eine bestimmte Position.

        Args:
            x (int): Zielposition X.
            y (int): Zielposition Y.
        """
        print(f"Setze Kamera-Position auf x={x}, y={y} ...")
        if self._fallback:
            self._x = min(MAX_POS_X, max(MIN_POS_X, x))
            self._y = min(MAX_POS_Y, max(MIN_POS_Y, y))
            print(f"[Fallback] set_position: x={self._x}, y={self._y}")
            return
        await self.send({"x": x, "y": y})
        print("Positionsbefehl gesendet.")

    async def close(self):
        """
        Schließt die Verbindung zur Kamera und gibt Ressourcen frei.
        """
        print("Schließe Kamera-Verbindung...")
        if self._fallback:
            if self.cap:
                print("[Fallback] Webcam wird freigegeben.")
                self.cap.release()
            print("[Fallback] Verbindung geschlossen.")
            return
        await self.ws.close()
        print("WebSocket-Verbindung geschlossen.")

    def is_fallback(self):
        """
        Gibt zurück, ob der Fallback-Modus aktiv ist.

        Returns:
            bool: True, wenn Fallback aktiv ist.
        """
        print(f"Fallback-Modus aktiv: {self._fallback}")
        return self._fallback
