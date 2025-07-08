# CodeIt - Interactive Python Learning System

## Overview

CodeIt is a Docker-based Python learning environment designed for cross-platform compatibility and interactive education. The system provides Python learning and an interactive shell with breakpoints and code snippet management.

## Key Features

### 🐳 **Universal Docker Integration**
- Automatic environment conflict detection and resolution
- Docker container management with Micromamba and scientific Python stack
- Copy mode support for restricted environments and sandboxed systems
- Automatic fallback from volume mounting to file copying when necessary

### 📚 **Interactive Learning Modules**
- **Basic Data Structures**: Lists, tuples, sets, dictionaries with interactive exploration
- **Advanced Data Structures**: Collections, dataclasses, namedtuples with hands-on examples
- **CSV Module**: File handling with DictReader/DictWriter and step-through learning
- **Pandas Module**: Data analysis with DataFrames, filtering, and statistical operations
- **Challenges Module**: Programming challenges and algorithmic problem solving with memoization
- **Advanced Challenges Module**: Production-scenario challenges for system design and cloud security

### 💻 **Enhanced Interactive Shell**
- **Breakpoint System**: Stop at key points for hands-on exploration
- **Smart Help System**: `cs(topic)` for cheat sheets, `hf()` for function help
- **Tab Completion**: Enhanced with function signatures and context awareness
- **Variable Tracking**: `cm()` to show current session variables
- **Snippet Export**: Automatic saving to `practice/[module]/` folders with timestamps

### 🔄 **Copy Mode for Restricted Environments**
- **File Synchronization**: Copies files instead of volume mounting
- **Background Sync**: Silent 2-second interval sync during interactive sessions
- **Restricted Environment Support**: Works in environments with filesystem restrictions
- **Clean Output**: No interference with interactive session formatting

## Quick Start

### Standard Usage
```bash
# Run all modules
python python/learn_python.py

# Interactive mode with specific modules
python python/learn_python.py --interactive --functions challenges_2

# List available modules
python python/learn_python.py --list
```

### Copy Mode (Restricted Environments)
```bash
# Setup with copy mode
python python/learn_python.py --cm --setup-env

# Interactive learning with copy mode
python python/learn_python.py --cm --interactive --functions basic

# Quick copy mode (short form)
python python/learn_python.py --cm --functions pandas
```

### Environment Management
```bash
# Check environment status
python python/learn_python.py --env-status

# Clean up Docker resources
python python/learn_python.py --cleanup-env

# Generate bash completion
python python/learn_python.py --bash-completion > ~/.bash_completion_python
```

## Architecture

### Core Components
```
python/
├── learn_python.py          # Main learning orchestrator
├── docker_manager.py        # Docker environment management with copy mode
├── Dockerfile              # Container definition (Micromamba + Python stack)
├── environment.yml         # Conda environment specification
├── COPY_MODE.md            # Copy mode documentation
├── README.md               # Detailed technical documentation
└── modules/                # Learning modules
    ├── basic_data_structures.py
    ├── advanced_data_structures.py
    ├── csv_module.py
    ├── pandas_module.py
    └── challenges.py
```

### Generated Outputs
```
practice/                   # Auto-generated practice files
├── basic/                 # Basic data structure examples
├── advanced/              # Advanced structure examples  
├── csv/                   # CSV handling examples
├── pandas/                # Pandas analysis examples
└── challenges/            # Programming challenge examples

help/                      # Help system cache
└── [topic]/               # Cached cheat sheets and documentation
```

## Environment Compatibility

### Supported Platforms
- ✅ **Linux** (Tested on several distributions)

## Interactive Features

### Learning Commands
- **`cs(topic)`** - Get cheat sheets for any topic with intelligent fallback
- **`cm()`** - Show current variables and their values  
- **`hf(function)`** - Get detailed function help and documentation
- **`shortcuts()`** or **`sc()`** - Display all available interactive functions

### Breakpoint System
The system pauses at strategic points during learning modules, allowing you to:
- Explore variables in their current state
- Test modifications interactively
- Save interesting code snippets automatically
- Get contextual help for the current topic

### Snippet Management
- **Automatic Export**: Code sections saved to `practice/[module]/###.py`
- **Timestamped Files**: Examples saved with timestamps for reference
- **Background/Foreground**: Seamless snippet handling during interactive sessions

## Requirements

- **Docker**: Installed and running
- **Python 3.7+**: For the main orchestrator script
- **Storage**: ~2GB for Docker image
- **Network**: Internet connection for initial setup
- **Copy Mode**: Compatible with environments where volume mounting is restricted

## Benefits

1. **Simple Configuration**: Quick setup
2. **Broad Compatibility**: Tested on several Linux environments
3. **Educational Focus**: Interactive breakpoints and guided learning
4. **Real-world Skills**: Practical examples with modern Python practices
5. **Clean Isolation**: No pollution of host environment

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdamDanielHarris/codeit.git
   cd codeit
   ```

2. **Choose your mode**:
   - **Standard**: `python python/learn_python.py --interactive`
   - **Restricted environments**: `python python/learn_python.py --cm --interactive`

3. **Start learning**:
   - Follow interactive prompts
   - Explore at breakpoints
   - Check generated files in `practice/` folders

## Documentation

- **[Python README](python/README.md)**: Technical details and advanced usage
- **[Copy Mode Guide](python/COPY_MODE.md)**: Complete copy mode documentation
- **Interactive Help**: Use `cs()`, `hf()`, and `shortcuts()` within the system

---

**CodeIt** provides a modern, Docker-based approach to learning Python that adapts to any environment while maintaining educational quality and professional development practices.
