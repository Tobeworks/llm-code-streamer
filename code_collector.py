import os
import argparse
from pathlib import Path
from typing import List, Set
from datetime import datetime

def collect_files(
    source_dir: str, 
    extensions: List[str], 
    output_file: str,
    exclude_dirs: Set[str] = {
        'node_modules', '.git', 'dist', 'build', 
        'lib', 'libs', 'venv', '.venv', 'env',
        '.env', '__pycache__', 'egg-info',
        '.pytest_cache', '.mypy_cache', '.coverage',
        'htmlcov', '.tox', '.eggs'
    }
) -> None:
    """
    Sammelt alle Dateien mit bestimmten Endungen und schreibt sie in eine Textdatei.
    
    Args:
        source_dir: Quellverzeichnis zum Durchsuchen
        extensions: Liste der Dateiendungen (z.B. ['.astro', '.vue'])
        output_file: Pfad zur Ausgabedatei
        exclude_dirs: Set von Verzeichnissen, die übersprungen werden sollen
    """
    source_path = Path(source_dir).resolve()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # Header mit Metadaten
        out.write(f"# Gesammelte Dateien aus {source_path}\n")
        out.write(f"# Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"# Gesuchte Endungen: {', '.join(extensions)}\n")
        out.write(f"# Start-Zeitstempel: {datetime.now().isoformat()}\n\n")
        
        for root, dirs, files in os.walk(source_path):
            # Überspringe ausgeschlossene Verzeichnisse
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            path = Path(root)
            
            # Filtere Dateien nach Endungen
            matching_files = [
                f for f in files 
                if any(f.endswith(ext) for ext in extensions)
            ]
            
            for file in matching_files:
                file_path = path / file
                rel_path = file_path.relative_to(source_path)
                
                # Trennzeile und Dateipfad als Kommentar
                out.write("\n" + "#" * 80 + "\n")
                out.write(f"# Datei: {rel_path}\n")
                out.write("#" * 80 + "\n\n")
                
                # Dateiinhalt
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        out.write(content)
                        if not content.endswith('\n'):
                            out.write('\n')
                except Exception as e:
                    out.write(f"# Fehler beim Lesen der Datei: {e}\n")
        
        # End-Zeitstempel
        out.write("\n" + "#" * 80 + "\n")
        out.write(f"# Ende-Zeitstempel: {datetime.now().isoformat()}\n")

def generate_filename(source_dir: str) -> str:
    """
    Generiert einen Dateinamen mit Projektnamen und Zeitstempel.
    
    Args:
        source_dir: Pfad zum Quellverzeichnis
    
    Returns:
        String: Generierter Dateiname
    """
    # Extrahiere den Projektnamen (letzter Ordnername)
    project_name = Path(source_dir).resolve().name
    # Erstelle Zeitstempel (Format: YYYYMMDD_HHMMSS)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"code_collection_{project_name}_{timestamp}.txt"

def main():
    parser = argparse.ArgumentParser(
        description='Sammelt Code-Dateien in eine einzelne Textdatei für LLM-Kontext'
    )
    parser.add_argument(
        'source_dir',
        help='Quellverzeichnis zum Durchsuchen'
    )
    parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        required=True,
        help='Liste der Dateiendungen (z.B. .astro .vue)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Optionaler benutzerdefinierter Ausgabedateiname'
    )
    parser.add_argument(
        '--exclude-dirs',
        nargs='+',
        default=[
            'node_modules', '.git', 'dist', 'build',
            'lib', 'libs', 'venv', '.venv', 'env',
            '.env', '__pycache__', 'egg-info',
            '.pytest_cache', '.mypy_cache', '.coverage',
            'htmlcov', '.tox', '.eggs'
        ],
        help='Zu überspringende Verzeichnisse'
    )
    
    args = parser.parse_args()
    
    # Wenn kein Ausgabedateiname angegeben wurde, generiere einen
    output_file = args.output if args.output else generate_filename(args.source_dir)
    
    collect_files(
        args.source_dir,
        args.extensions,
        output_file,
        set(args.exclude_dirs)
    )

if __name__ == "__main__":
    main()