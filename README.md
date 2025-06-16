# Code Collector

A Python tool for collecting code files into a single text file or multiple chunks, optimized for use with Large Language Models (LLMs).

## Features

- Collects files with specified extensions
- Adds relative paths as comments
- Excludes certain directories by default (node_modules, .git, etc.)
- Adds timestamps for start and end of collection
- Supports splitting into chunks with defined maximum size
- Automatic filename generation with project name and timestamp
- **Stdout output for direct copy & paste or piping**
- Error handling for unreadable files

## Installation

```bash
git clone [repository-url]
cd code-collector
```

## Virtual Environment Setup (optional)

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

### Basic Usage
```bash
# Collect all .py files into a single file
python code_collector.py /path/to/project -e .py

# Multiple file extensions
python code_collector.py /path/to/project -e .astro .vue .jsx

# Direct output to stdout (for copy & paste)
python code_collector.py /path/to/project -e .py --stdout
```

### Chunk-based Usage
```bash
# Split output into 4MB chunks (4096 KB)
python code_collector.py /path/to/project -e .py -c 4096

# 2MB chunks with custom name
python code_collector.py /path/to/project -e .py -c 2048 -o project_base.txt
```

### Custom Exclusions
```bash
# Exclude additional directories
python code_collector.py /path/to/project -e .py --exclude-dirs node_modules .git temp cache
```

### Stdout Output for LLMs
```bash
# Direct output for copy & paste into LLM tools
python code_collector.py /path/to/project -e .js .jsx .ts --stdout

# With redirection to file (if desired)
python code_collector.py /path/to/project -e .py --stdout > output.txt

# For macOS clipboard (pbcopy)
python code_collector.py /path/to/project -e .py --stdout | pbcopy
```

## Output Format

### Single File
The output file contains:
- Metadata (date, searched extensions)
- Start timestamp
- For each file:
  - Separator line
  - Relative path as comment
  - File content
- End timestamp

### Stdout Output
Identical format as single file, but directly to stdout for:
- Copy & paste into LLM interfaces
- Piping to other tools
- Integration into workflows and automation

### Chunks
Each chunk contains:
- Chunk number and timestamp
- Files up to maximum chunk size
- Separator lines between files
- Relative paths as comments

## Filename Format

### Single File
```
code_collection_[projectname]_[YYYYMMDD_HHMMSS].txt
```

### Chunks
```
code_collection_[projectname]_[YYYYMMDD_HHMMSS]_chunk001.txt
code_collection_[projectname]_[YYYYMMDD_HHMMSS]_chunk002.txt
...
```

## Default Excluded Directories

- Version control: `.git`
- Build directories: `dist`, `build`, `old`
- Dependencies: `node_modules`, `lib`, `libs`
- Python-specific:
  - Virtual environments: `venv`, `.venv`, `env`, `.env`
  - Cache: `__pycache__`, `.pytest_cache`, `.mypy_cache`
  - Test & Coverage: `.coverage`, `htmlcov`, `.tox`
  - Package info: `egg-info`, `.eggs`

## Command Line Arguments

- `source_dir`: Source directory to search through
- `-e, --extensions`: List of file extensions (e.g. .astro .vue)
- `-o, --output`: Optional custom output filename
- `-c, --chunk-size`: Maximum size per chunk in KB (e.g. 4096 for 4MB)
- `--exclude-dirs`: Directories to skip
- `--stdout`: **Output to stdout instead of file (for direct copy & paste)**

## macOS Integration

### Automator Quick Action
The tool can be set up as a macOS Quick Action for quick access:

1. Open Automator → Create Quick Action
2. "Workflow receives: folders in Finder"
3. Add Run Shell Script Action with:
```bash
extensions=$(osascript -e 'text returned of (display dialog "File extensions:" default answer ".js .json")')
for folder in "$@"; do
    python /path/to/code_collector.py "$folder" -e $extensions --stdout
done
```
4. Add "View Results" Action for text display
5. Save as Quick Action

**Usage:** Right-click on folder → Services → "Generate Code Collection"

## Requirements

- Python 3.6 or higher
- Standard libraries (os, argparse, pathlib, datetime, sys)

## License

MIT