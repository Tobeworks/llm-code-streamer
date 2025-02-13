# Code Collector

Ein Python-Tool zum Sammeln von Codedateien in eine einzelne Textdatei, optimiert für die Verwendung mit Large Language Models (LLMs).

## Features

- Sammelt Dateien mit spezifizierten Endungen in eine einzelne Textdatei
- Fügt relative Pfade als Kommentare hinzu
- Schließt standardmäßig bestimmte Verzeichnisse aus (node_modules, .git, etc.)
- Fügt Zeitstempel für Start und Ende der Sammlung hinzu
- Fehlerbehandlung für nicht lesbare Dateien
- Flexible Konfiguration über Kommandozeilenargumente

## Installation

```bash
git clone [repository-url]
cd code-collector
```

## Einrichtung der virtuellen Umgebung

```bash
# Erstellen der virtuellen Umgebung
python -m venv .venv

# Aktivieren der virtuellen Umgebung
# Unter Windows:
.venv\Scripts\activate
# Unter Linux/MacOS:
source .venv/bin/activate

# Installation der Abhängigkeiten (falls in Zukunft welche hinzukommen)
pip install -r requirements.txt
```

## Verwendung

Grundlegende Verwendung:
```bash
python code_collector.py /pfad/zum/projekt -e .astro .vue .react .py
```

Mit benutzerdefinierter Ausgabedatei:
```bash
python code_collector.py /pfad/zum/projekt -e .astro .vue .react .py -o mein_kontext.txt
```

Mit zusätzlichen auszuschließenden Verzeichnissen:
```bash
python code_collector.py /pfad/zum/projekt -e .astro .vue .react .py --exclude-dirs node_modules .git dist build temp
```

## Kommandozeilenargumente

- `source_dir`: Quellverzeichnis zum Durchsuchen
- `-e, --extensions`: Liste der Dateiendungen (z.B. .astro .vue)
- `-o, --output`: Ausgabedatei (Standard: collected_code.txt)
- `--exclude-dirs`: Zu überspringende Verzeichnisse

## Ausgabeformat

Die Ausgabedatei enthält:
- Metadaten (Datum, gesuchte Endungen, Start-Zeitstempel)
- Für jede Datei:
  - Trennzeile
  - Relativer Pfad als Kommentar
  - Dateiinhalt
- End-Zeitstempel

## Anforderungen

- Python 3.6 oder höher
- Standardbibliotheken (os, argparse, pathlib, datetime)

## Lizenz

MIT