# CodeIt

Interactive Python learning with Docker support.

## Quick Start

```bash
git clone https://github.com/AdamDanielHarris/codeit.git
cd codeit
python3 python/learn_python.py --interactive
```

## Usage

```bash
# Run specific modules
python3 python/learn_python.py --functions basic pandas

# List available modules
python3 python/learn_python.py --list

# Setup environments
python3 python/learn_python.py --setup-env               # Docker (default)
python3 python/learn_python.py --setup-env --mamba   # Local micromamba (Linux/macOS/Termux)
python3 python/learn_python.py --setup-env --rebuild     # Rebuild after changing environment.yml

# Execution modes
python3 python/learn_python.py --mamba      # Use local micromamba environment
python3 python/learn_python.py --docker   # Force Docker usage
python3 python/learn_python.py --no-docker      # Host Python only
python3 python/learn_python.py --cm             # Copy mode (restricted filesystems)
```

## Modules

- **basic** - Lists, tuples, sets, dictionaries
- **advanced** - Collections, dataclasses, namedtuples  
- **csv** - File handling with DictReader/DictWriter
- **pandas** - DataFrames, filtering, analysis
- **jupyter** - Notebook creation, IPython features, magic commands
- **challenges** - Programming problems and algorithms
- **challenges_2** - System design scenarios

## Interactive Commands

- `cs(topic)` - Cheat sheets
- `cm()` - Show variables
- `hf(function)` - Function help
- `shortcuts()` - Available commands

## Requirements

**Option 1: Docker (recommended for ease of use)**
- Docker Desktop or Docker Engine
- ~2GB storage for Docker image

**Option 2: Micromamba (recommended for Termux/Android)**
- curl (for installation)
- ~1GB storage for environment
- Works on Linux, macOS, WSL, Termux
- On Termux: proot is automatically installed for environment isolation
  - Uses `--always-copy` flag for compatibility
  - Bind mounts project directory so generated files are accessible

**Option 3: System Python**
- Python 3.7+ with pip
- Manual package installation

Generated practice files saved to `practice/[module]/`.
