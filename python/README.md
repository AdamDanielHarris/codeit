# Docker-Based Python Learning Environment

## Overview

This project now uses a **Docker-based environment management system** that provides seamless Python learning with automatic conflict resolution. The system smartly detects environment issues (like NixOS compatibility problems) and automatically runs problematic modules in an isolated Docker container.

## Architecture

### Core Components

1. **`learn_python.py`** - Main learning script with integrated environment management
2. **`docker_manager.py`** - Docker environment manager
3. **`Dockerfile`** - Container definition with Micromamba and Python scientific stack
4. **`environment.yml`** - Conda environment specification
5. **`modules/`** - Modular learning components
   - `basic_data_structures.py` - Lists, tuples, sets, dictionaries
   - `advanced_data_structures.py` - Collections, dataclasses, namedtuples
   - `csv_module.py` - CSV file handling
   - `pandas_module.py` - Data analysis with pandas

### How It Works

1. **Automatic Conflict Detection**: The system detects environment conflicts such as:
   - NixOS incompatibilities with dynamically linked executables
   - C++ library version conflicts (libstdc++, GLIBCXX)
   - Multiple Python installation conflicts
   - Package build/installation issues

2. **Smart Environment Switching**: When conflicts are detected (especially for pandas), the system:
   - Automatically builds a Docker environment if needed
   - Runs the problematic module inside the container
   - Seamlessly returns results to the host

3. **Container Management**: The Docker manager handles:
   - Image building with Micromamba and scientific Python stack
   - Container lifecycle (create, start, stop, restart)
   - Volume mounting for seamless file access
   - Command execution with proper environment activation

## Usage

### Basic Usage
```bash
# Run all modules
python python/learn_python.py

# Run specific modules
python python/learn_python.py --functions basic advanced pandas

# Interactive mode with breakpoints
python python/learn_python.py --interactive --functions pandas

# List available modules
python python/learn_python.py --list
```

### Environment Management
```bash
# Check environment status
python python/learn_python.py --env-status

# Set up Docker environment
python python/learn_python.py --setup-env

# Show activation instructions
python python/learn_python.py --activate-env

# Clean up environments
python python/learn_python.py --cleanup-env
```

### Interactive Features
```bash
# Interactive mode with step-through capability
python python/learn_python.py --interactive --step --functions csv_module

# Generate bash completion
python python/learn_python.py --bash-completion > ~/.bash_completion_python
```

## Technical Details

### Docker Environment
- **Base Image**: `mambaorg/micromamba:1.5.6`
- **Python Version**: 3.11
- **Key Packages**: numpy, pandas, matplotlib, seaborn, jupyter, ipython
- **Environment**: Fully isolated with volume mounting for project access

### Environment Detection
The system automatically detects:
- Host OS compatibility issues (NixOS, etc.)
- Python library conflicts
- Missing or broken package installations
- File permission issues

### Conflict Resolution
When conflicts are detected:
1. Build Docker image (if not exists)
2. Create and start container
3. Execute problematic code in container
4. Return results to host
5. Automatic container restart on failures

## Benefits

1. **Universal Compatibility**: Works on any system with Docker (NixOS, Ubuntu, macOS, etc.)
2. **Zero Configuration**: Automatic environment detection and setup
3. **Seamless Experience**: Users don't need to know about containers
4. **Conflict Resolution**: Automatically handles library incompatibilities
5. **Clean Isolation**: No pollution of host environment
6. **Easy Cleanup**: Simple commands to remove everything

## Module Features

### Basic Data Structures
- Lists, tuples, sets, dictionaries
- Interactive breakpoints for exploration
- Comprehensive examples with mutations

### Advanced Data Structures
- Collections module (defaultdict, Counter, OrderedDict, deque, ChainMap)
- Named tuples and frozen sets
- Dataclasses with field types and methods

### CSV Module
- Reading and writing CSV files
- DictReader and DictWriter examples
- Step-through mode for learning
- Automatic file cleanup

### Pandas Module
- DataFrame creation and manipulation
- Data selection and filtering
- Statistical operations and summaries
- Column operations and calculations
- Series operations
- File I/O with automatic container-friendly paths

## Interactive Shell Features

When using `--interactive` mode:
- **`cs(topic)`** - Cheat sheet lookup with fallback strategies
- **`cm()`** - Show current variables
- **Tab completion** - Enhanced with function signatures
- **Breakpoints** - Interactive exploration at key points
- **Context-aware help** - Automatic topic detection

## Error Handling

The system includes robust error handling:
- Container health checks and automatic restart
- File permission issue resolution
- Package import error detection
- Graceful fallback for Docker unavailability

## Requirements

- Docker installed and running
- Python 3.7+ on host (for the main script)
- ~2GB disk space for Docker image
- Internet connection for initial setup

## File Structure

```
python/
├── learn_python.py          # Main script
├── docker_manager.py        # Docker environment manager
├── Dockerfile              # Container definition
├── environment.yml         # Conda environment spec
└── modules/
    ├── __init__.py
    ├── basic_data_structures.py
    ├── advanced_data_structures.py
    ├── csv_module.py
    └── pandas_module.py
```

This architecture provides a robust, cross-platform Python learning environment that "just works" regardless of the host system's configuration or conflicts.
