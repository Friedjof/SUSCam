# SUSCam 👁️🎥

**SUSCam** ist ein experimentelles Projekt zur Echtzeit-Personenerkennung und Kamerafernsteuerung mit Python, OpenCV und [MediaPipe](https://chuoling.github.io/mediapipe/) – entwickelt für den Workshop „SUSCam“ beim [ASM25](https://www.muc.ccc.de/asm:25:start) des Chaos Computer Club München.

Ziel ist es, in kurzer Zeit einen funktionierenden Bildverarbeitungs-Workflow aufzubauen, mit dem Teilnehmer*innen visuelle Daten auswerten und gleichzeitig eine Kamera live per WebSocket steuern können. Die Anwendung ist bewusst offen gestaltet – zum Hacken, Erweitern und Infragestellen.

> Sollte die externe Kamera nicht verfügbar sein, wird automatisch auf eine lokale Webcam umgeschaltet. Die Schnittstellen bleiben dabei gleich – allerdings sind dann motorisierte Funktionen deaktiviert.

## 🎯 Mediapipe

[MediaPipe](https://chuoling.github.io/mediapipe/) ist eine Open-Source-Bibliothek von Google für Echtzeit-Computer-Vision-Anwendungen. Sie bringt leistungsfähige Module wie Hand-, Gesichts- und Körpererkennung direkt in Python-Projekte – ohne tiefes Machine-Learning-Wissen.

Im Rahmen dieses Projekts dient MediaPipe zur schnellen Visualisierung und Analyse von Kameradaten – ideal für interaktive Anwendungen wie „Person verfolgen“, „Hand zeigen = Kamera schwenkt“ oder eigene Ideen.

**Weitere Ressourcen:**

* [Setup-Anleitung für Python](https://ai.google.dev/edge/mediapipe/solutions/setup_python)
* [Gesture Recognition Guide](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
* [MediaPipe auf PyPI](https://pypi.org/project/mediapipe/)

---

## 🕹️ Kamerafernsteuerung via WebSocket

Die Kamera im Projekt kann live über einfache WebSocket-Kommandos gesteuert werden – etwa zur Positionierung, Frame-Abfrage oder Statusinfo.

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
| `light_on/off`        | (Derzeit deaktiviert) Lichtsteuerung|

Das Steuerprotokoll ist einfach gehalten – ideal für eigene Steuerungs-Apps, UIs oder Automatisierungen. Die Details findest du in [`tools/cam.py`](tools/cam.py).

---

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
    └── cam.py               # Kamera-Klasse für Steuerung & Streaming
````

> Für Umgebungsvariablen gibt es eine `.env`-Datei (siehe `.env.example` für Vorlage).

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

> Alle Skripte nutzen automatisch die in `.env` konfigurierte IP-Adresse.

## 📷 Bonus: Virtuelle Kamera

Mit [pyvirtualcam](https://pypi.org/project/pyvirtualcam/) kann der Kamerastream als virtuelle Webcam bereitgestellt werden. So können andere Anwendungen (z.B. Videokonferenz-Tools) den Live-Stream nutzen.

### Ubuntu

```bash
sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="SUSCam Virtual Camera" exclusive_caps=1
pip install pyvirtualcam
```

### Windows

```bash
pip install pyvirtualcam
```

## 🔐 Hinweise

* Dieses Projekt ist ein Lern- und Diskussionswerkzeug – kein fertiges Produkt.
* Datenschutz und ethische Aspekte sollten bei eigenen Anwendungen aktiv mitgedacht werden.
* Technische Störungen (Netzwerk, Kamera, Betriebssystem-Inkompatibilitäten) können vorkommen – es gibt Fallbacks.

## 📝 Lizenz
Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Du kannst es frei nutzen, modifizieren und weiterverbreiten.

## 🙋 Mitmachen & Feedback

Dieses Projekt entstand im Rahmen des Workshops „SUSCam“ beim ASM25.
Fragen, Ideen oder Erweiterungen? → Öffne ein [Issue](https://github.com/Friedjof/SUSCam/issues) oder sprich mich beim ASM25 direkt an.