# CodeIt

Interactive Python learning with Docker support.

## Quick Start

```bash
git clone https://github.com/AdamDanielHarris/codeit.git
cd codeit
python python/learn_python.py --interactive
```

## Usage

```bash
# Run specific modules
python python/learn_python.py --functions basic pandas

# List available modules
python python/learn_python.py --list

# Different execution modes
python python/learn_python.py --cm          # Copy mode (restricted environments)
python python/learn_python.py --no-docker  # Host Python only
python python/learn_python.py --force-docker # Force Docker usage
```

## Modules

- **basic** - Lists, tuples, sets, dictionaries
- **advanced** - Collections, dataclasses, namedtuples  
- **csv** - File handling with DictReader/DictWriter
- **pandas** - DataFrames, filtering, analysis
- **challenges** - Programming problems and algorithms
- **challenges_2** - System design scenarios

## Interactive Commands

- `cs(topic)` - Cheat sheets
- `cm()` - Show variables
- `hf(function)` - Function help
- `shortcuts()` - Available commands

## Requirements

- Docker (recommended) or Python 3.7+
- ~2GB storage for Docker image

Generated practice files saved to `practice/[module]/`.
