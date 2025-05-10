# LLM Code Collector
A Python tool for collecting code files into a single text file or multiple chunks, optimized for use with Large Language Models (LLMs).

## Features
- Collects files with specified extensions
- Adds relative paths as comments
- Excludes certain directories by default (node_modules, .git, etc.)
- Adds timestamps for start and end of collection
- Supports splitting into chunks with defined maximum size
- Automatic generation of filenames with project name and timestamp
- Error handling for unreadable files

## Installation
```bash
git clone [repository-url]
cd code-collector
```

## Setting up virtual environment (optional)
```bash
# Create virtual environment
python -m venv .venv
# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/MacOS:
source .venv/bin/activate
# Install dependencies (if any are added in the future), also optional
pip install -r requirements.txt
```

## Usage
### Basic usage
```bash
# Collects all .py files into a single file
python code_collector.py /path/to/project -e .py
# Multiple file extensions
python code_collector.py /path/to/project -e .astro .vue .jsx
```

### Chunk-based usage
```bash
# Splits the output into 4MB chunks (4096 KB)
python code_collector.py /path/to/project -e .py -c 4096
# 2MB chunks with custom name
python code_collector.py /path/to/project -e .py -c 2048 -o project_base.txt
```

### Custom exclusions
```bash
# Exclude additional directories
python code_collector.py /path/to/project -e .py --exclude-dirs node_modules .git temp cache
```

## Output format
### Single file
The output file contains:
- Metadata (date, searched extensions)
- Start timestamp
- For each file:
  - Separator line
  - Relative path as comment
  - File content
- End timestamp

### Chunks
Each chunk contains:
- Chunk number and timestamp
- Files up to the maximum chunk size
- Separator lines between files
- Relative paths as comments

## Filename format
### Single file
```
code_collection_[projectname]_[YYYYMMDD_HHMMSS].txt
```

### Chunks
```
code_collection_[projectname]_[YYYYMMDD_HHMMSS]_chunk001.txt
code_collection_[projectname]_[YYYYMMDD_HHMMSS]_chunk002.txt
...
```

## Directories excluded by default
- Version control: `.git`
- Build directories: `dist`, `build`
- Dependencies: `node_modules`, `lib`, `libs`
- Python-specific:
  - Virtual environments: `venv`, `.venv`, `env`, `.env`
  - Cache: `__pycache__`, `.pytest_cache`, `.mypy_cache`
  - Test & Coverage: `.coverage`, `htmlcov`, `.tox`
  - Package info: `egg-info`, `.eggs`

## Command line arguments
- `source_dir`: Source directory to search
- `-e, --extensions`: List of file extensions (e.g. .astro .vue)
- `-o, --output`: Optional custom output filename
- `-c, --chunk-size`: Maximum size per chunk in KB (e.g. 4096 for 4MB)
- `--exclude-dirs`: Directories to skip

## Requirements
- Python 3.6 or higher
- Standard libraries (os, argparse, pathlib, datetime)

## License
MIT
