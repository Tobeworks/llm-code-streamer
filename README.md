# Code Collector

Ein Python-Tool zum Sammeln von Codedateien in eine einzelne Textdatei oder mehrere Chunks, optimiert für die Verwendung mit Large Language Models (LLMs).

## Features

- Sammelt Dateien mit spezifizierten Endungen
- Fügt relative Pfade als Kommentare hinzu
- Schließt standardmäßig bestimmte Verzeichnisse aus (node_modules, .git, etc.)
- Fügt Zeitstempel für Start und Ende der Sammlung hinzu
- Unterstützt Aufteilung in Chunks mit definierter maximaler Größe
- Automatische Generierung von Dateinamen mit Projektnamen und Zeitstempel
- Fehlerbehandlung für nicht lesbare Dateien

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

### Grundlegende Verwendung
```bash
# Sammelt alle .py Dateien in eine einzelne Datei
python code_collector.py /pfad/zum/projekt -e .py

# Mehrere Dateiendungen
python code_collector.py /pfad/zum/projekt -e .astro .vue .jsx
```

### Chunk-basierte Verwendung
```bash
# Teilt die Ausgabe in 4MB große Chunks auf (4096 KB)
python code_collector.py /pfad/zum/projekt -e .py -c 4096

# 2MB Chunks mit benutzerdefiniertem Namen
python code_collector.py /pfad/zum/projekt -e .py -c 2048 -o projekt_basis
```

### Benutzerdefinierte Ausschlüsse
```bash
# Zusätzliche Verzeichnisse ausschließen
python code_collector.py /pfad/zum/projekt -e .py --exclude-dirs node_modules .git temp cache
```

## Ausgabeformat

### Einzeldatei
Die Ausgabedatei enthält:
- Metadaten (Datum, gesuchte Endungen)
- Start-Zeitstempel
- Für jede Datei:
  - Trennzeile
  - Relativer Pfad als Kommentar
  - Dateiinhalt
- End-Zeitstempel

### Chunks
Jeder Chunk enthält:
- Chunk-Nummer und Zeitstempel
- Dateien bis zur maximalen Chunk-Größe
- Trennlinien zwischen Dateien
- Relative Pfade als Kommentare

## Dateinamenformat

### Einzeldatei
```
code_collection_[projektname]_[YYYYMMDD_HHMMSS].txt
```

### Chunks
```
code_collection_[projektname]_[YYYYMMDD_HHMMSS]_chunk001.txt
code_collection_[projektname]_[YYYYMMDD_HHMMSS]_chunk002.txt
...
```

## Standardmäßig ausgeschlossene Verzeichnisse

- Versionskontrolle: `.git`
- Build-Verzeichnisse: `dist`, `build`
- Abhängigkeiten: `node_modules`, `lib`, `libs`
- Python-spezifisch:
  - Virtuelle Umgebungen: `venv`, `.venv`, `env`, `.env`
  - Cache: `__pycache__`, `.pytest_cache`, `.mypy_cache`
  - Test & Coverage: `.coverage`, `htmlcov`, `.tox`
  - Paket-Info: `egg-info`, `.eggs`

## Kommandozeilenargumente

- `source_dir`: Quellverzeichnis zum Durchsuchen
- `-e, --extensions`: Liste der Dateiendungen (z.B. .astro .vue)
- `-o, --output`: Optionaler benutzerdefinierter Ausgabedateiname
- `-c, --chunk-size`: Maximale Größe pro Chunk in KB (z.B. 4096 für 4MB)
- `--exclude-dirs`: Zu überspringende Verzeichnisse

## Anforderungen

- Python 3.6 oder höher
- Standardbibliotheken (os, argparse, pathlib, datetime)

## Lizenz

MIT