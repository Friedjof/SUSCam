# SUSCam 👀🎥

**SUSCam** ist ein praktisches Projekt zur Echtzeit-Personenerkennung mit Python, OpenCV und MediaPipe – inklusive WebSocket-gesteuerter Kamera.  

Ursprünglich entwickelt für den Workshop beim [ASM25](https://www.muc.ccc.de/asm:25:start), erlaubt es, schnell mit Kamerastreams zu experimentieren, Objekte zu erkennen und die Kamera zu bewegen. Es ist bewusst einfach gehalten und lädt zum Hacken und Weiterentwickeln ein.

> Sollte die externe Kamera nicht verfügbar sein, wird automatisch auf eine lokale Webcam umgeschaltet. Die Schnittstellen bleiben dabei gleich. Natürlich sind dann die Funktionen zur Motorkontrolle deaktiviert.

## 🎯 Mediapipe

[MediaPipe](https://chuoling.github.io/mediapipe/) ist eine Open-Source-Bibliothek von Google, die Echtzeit-Computer-Vision-Anwendungen ermöglicht. Sie bietet vorgefertigte Lösungen für Aufgaben wie Hand-, Gesichts- und Körpererkennung sowie Gestenerkennung.

In diesem Projekt nutzen wir MediaPipe, um visuelle Merkmale wie Hände oder Gesichter im Kamerabild zu erkennen und zu verfolgen. Dies ermöglicht es, interaktive Anwendungen zu entwickeln, bei denen die Kamera beispielsweise automatisch auf erkannte Objekte reagieren kann.

**Weitere Ressourcen:**

* Offizielle Python-Setup-Anleitung: [MediaPipe Python Setup Guide](https://ai.google.dev/edge/mediapipe/solutions/setup_python)
* Gestenerkennung mit MediaPipe: [Gesture Recognition Guide](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
* MediaPipe auf PyPI: [mediapipe](https://pypi.org/project/mediapipe/)

## 📦 Projektstruktur

```plaintext
SUSCam/
├── .env                     # Umgebungsvariablen (z.B. Kamera-IP)
├── app.py                   # Hauptstream-Anwendung mit OpenCV
├── requirements.txt         # Python-Abhängigkeiten
├── examples/                # Beispielskripte für Nutzung & Steuerung
│   ├── camera_infos.py
│   ├── camera_stream_mediapipe.py
│   ├── camera_stream_opencv.py
│   └── move_camera.py
└── tools/
    ├── cam.py               # Kamera-Klasse für Steuerung & Streaming
````

---

## ▶️ Schnellstart

1. Python-Umgebung vorbereiten:

```bash
git clone https://github.com/Friedjof/SUSCam.git
cd SUSCam
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. `.env`-Datei anpassen:

```env
SUS_IP=192.168.XXX.XXX
```

3. Beispiele ausführen:

```bash
python examples/camera_stream_opencv.py
```

## 🎓 Beispiele (kurz erklärt)

| Script                       | Zweck                                                   |
| ---------------------------- | ------------------------------------------------------- |
| `camera_infos.py`            | Liest Position, Limits und Clientanzahl über WebSocket. |
| `camera_stream_opencv.py`    | Zeigt den Live-Stream der Kamera mit OpenCV.            |
| `camera_stream_mediapipe.py` | Erweitert um Handerkennung via MediaPipe.               |
| `move_camera.py`             | Führt Bewegungsbefehle aus (links, rechts, usw.).       |

Alle Skripte greifen automatisch auf die in `.env` konfigurierte Kamera zu.

## 🌐 WebSocket-API

Die Kamera kann über folgende Befehle gesteuert oder abgefragt werden:

| Befehl                | Funktion                            |
| --------------------- | ----------------------------------- |
| `getframe`            | Aktuelles Kamerabild senden         |
| `center`              | Kamera auf Startposition setzen     |
| `up/down`             | Kamera vertikal bewegen             |
| `left/right`          | Kamera horizontal bewegen           |
| `get_pos`             | Gibt aktuelle Position als JSON     |
| `get_limits`          | Gibt X/Y-Grenzen als JSON zurück    |
| `client_count`        | Gibt Anzahl verbundener Clients     |
| `{"x": 100, "y": 50}` | Direkte Positionssteuerung via JSON |

*(`light_on` / `light_off` sind derzeit deaktiviert)*

## 🔐 Hinweise

* Alle Skripte sind als Lernmaterial gedacht.
* Der Zugriff auf die Kamera erfolgt über ein einfaches WebSocket-Protokoll.
* Achte bei eigenen Projekten auf Datenschutz und ethische Aspekte.

## 🙋 Kontakt & Mitmachen

Dieses Projekt entstand im Rahmen eines Workshops beim Chaos Computer Club München.
Fragen oder Ideen? → Issues oder Pull Requests willkommen.
