import os
import argparse
import sys
from pathlib import Path
from typing import List, Set, Optional, Tuple
from datetime import datetime

def generate_filename(source_dir: str, chunk_number: Optional[int] = None) -> str:
    """
    Generiert einen Dateinamen mit Projektnamen und Zeitstempel.
    
    Args:
        source_dir: Pfad zum Quellverzeichnis
        chunk_number: Optional, Nummer des Chunks
    
    Returns:
        String: Generierter Dateiname
    """
    project_name = Path(source_dir).resolve().name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"code_collection_{project_name}_{timestamp}"
    if chunk_number is not None:
        return f"{base_name}_chunk{chunk_number:03d}.txt"
    return f"{base_name}.txt"

def write_chunk(file_contents: List[Tuple[str, str]], chunk_size: int, base_filename: str, chunk_number: int) -> None:
    """
    Schreibt einen Chunk von Dateien in eine Ausgabedatei.
    
    Args:
        file_contents: Liste von Tupeln (Pfad, Inhalt)
        chunk_size: Maximale Größe des Chunks in Bytes
        base_filename: Basis für den Ausgabedateinamen
        chunk_number: Nummer des aktuellen Chunks
    """
    output_file = base_filename.replace('.txt', f'_chunk{chunk_number:03d}.txt')
    current_size = 0
    
    with open(output_file, 'w', encoding='utf-8') as out:
        header = f"# Chunk {chunk_number}\n"
        header += f"# Zeitstempel: {datetime.now().isoformat()}\n\n"
        out.write(header)
        current_size = len(header.encode('utf-8'))
        
        for rel_path, content in file_contents:
            file_header = f"\n{'#' * 80}\n# Datei: {rel_path}\n{'#' * 80}\n\n"
            file_content = f"{content}\n"
            
            content_size = len(file_header.encode('utf-8')) + len(file_content.encode('utf-8'))
            if current_size + content_size > chunk_size:
                break
                
            out.write(file_header)
            out.write(file_content)
            current_size += content_size
            
        footer = f"\n{'#' * 80}\n# Ende Chunk {chunk_number}\n"
        out.write(footer)

def collect_files(
    source_dir: str, 
    extensions: List[str], 
    output_file: Optional[str] = None, 
    exclude_dirs: Set[str] = {
        'node_modules', '.git', 'dist', 'build', 'old',
        'lib', 'libs', 'venv', '.venv', 'env',
        '.env', '__pycache__', 'egg-info',
        '.pytest_cache', '.mypy_cache', '.coverage',
        'htmlcov', '.tox', '.eggs'
    },
    chunk_size: Optional[int] = None,
    stdout: bool = False
) -> None:
    """
    Sammelt alle Dateien mit bestimmten Endungen und schreibt sie in eine oder mehrere Textdateien oder stdout.
    
    Args:
        source_dir: Quellverzeichnis zum Durchsuchen
        extensions: Liste der Dateiendungen (z.B. ['.astro', '.vue'])
        output_file: Pfad zur Ausgabedatei (None wenn stdout=True)
        exclude_dirs: Set von Verzeichnissen, die übersprungen werden sollen
        chunk_size: Optional, maximale Größe pro Chunk in Bytes
        stdout: Wenn True, ausgabe an stdout statt Datei
    """
    source_path = Path(source_dir).resolve()
    collected_files = []
    
    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        path = Path(root)
        
        matching_files = [
            f for f in files 
            if any(f.endswith(ext) for ext in extensions)
        ]
        
        for file in matching_files:
            file_path = path / file
            rel_path = file_path.relative_to(source_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    collected_files.append((str(rel_path), content))
            except Exception as e:
                print(f"Fehler beim Lesen von {file_path}: {e}", file=sys.stderr)
    
    if stdout:
        print(f"# Gesammelte Dateien aus {source_path}")
        print(f"# Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"# Gesuchte Endungen: {', '.join(extensions)}")
        print(f"# Start-Zeitstempel: {datetime.now().isoformat()}")
        print()
        
        for rel_path, content in collected_files:
            print(f"{'#' * 80}")
            print(f"# Datei: {rel_path}")
            print(f"{'#' * 80}")
            print()
            print(content)
            if not content.endswith('\n'):
                print()
        
        print(f"{'#' * 80}")
        print(f"# Ende-Zeitstempel: {datetime.now().isoformat()}")
        return
    
    if chunk_size:
        chunk_number = 1
        remaining_files = collected_files
        
        while remaining_files:
            write_chunk(remaining_files, chunk_size, output_file, chunk_number)
            
            current_size = 0
            files_in_chunk = 0
            for rel_path, content in remaining_files:
                file_content = f"\n{'#' * 80}\n# Datei: {rel_path}\n{'#' * 80}\n\n{content}\n"
                content_size = len(file_content.encode('utf-8'))
                if current_size + content_size > chunk_size:
                    break
                current_size += content_size
                files_in_chunk += 1
            
            remaining_files = remaining_files[files_in_chunk:]
            chunk_number += 1
            
    else:
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(f"# Gesammelte Dateien aus {source_path}\n")
            out.write(f"# Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"# Gesuchte Endungen: {', '.join(extensions)}\n")
            out.write(f"# Start-Zeitstempel: {datetime.now().isoformat()}\n\n")
            
            for rel_path, content in collected_files:
                out.write(f"\n{'#' * 80}\n")
                out.write(f"# Datei: {rel_path}\n")
                out.write(f"{'#' * 80}\n\n")
                out.write(content)
                if not content.endswith('\n'):
                    out.write('\n')
            
            out.write(f"\n{'#' * 80}\n")
            out.write(f"# Ende-Zeitstempel: {datetime.now().isoformat()}\n")

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
    parser.add_argument(
        '-c', '--chunk-size',
        type=int,
        help='Maximale Größe pro Chunk in KB (z.B. 4096 für 4MB)'
    )
    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Ausgabe an stdout statt in Datei'
    )
    
    args = parser.parse_args()
    
    output_file = None
    if not args.stdout:
        output_file = args.output if args.output else generate_filename(args.source_dir)
    
    collect_files(
        source_dir=args.source_dir,
        extensions=args.extensions,
        output_file=output_file,
        exclude_dirs=set(args.exclude_dirs),
        chunk_size=args.chunk_size * 1024 if args.chunk_size else None,
        stdout=args.stdout
    )

if __name__ == "__main__":
    main()