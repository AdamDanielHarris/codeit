# Docker-Based Python Learning Environment

## Overview

This project uses a **Docker-based environment management system** tha### Module Features

### Basic Data Structures
- Lists, tuples, sets, dictionaries
- Interactive breakpoints for exploration
- Examples with mutationsides Python learning with automatic conflict resolution and **copy mode support for restricted environments**. The system detects environment issues and automatically runs problematic modules in an isolated Docker container with file synchronization.

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
   - `challenges.py` - Programming challenges and algorithmic problem solving

### How It Works

1. **Smart Environment Switching**: The system:
   - Automatically builds a Docker environment if needed
   - Uses copy mode if volume mounting fails in restricted environments
   - Runs the problematic module inside the container
   - Returns results to the host

2. **Container Management**: The Docker manager handles:
   - Image building with Micromamba and scientific Python stack
   - Container lifecycle (create, start, stop, restart)
   - Volume mounting for file access OR copy mode for restricted environments
   - Command execution with proper environment activation
   - Background file synchronization in copy mode (every 2 seconds)

## Usage

### Basic Usage
```bash
# Run all modules
python python/learn_python.py

# Run specific modules
python python/learn_python.py --functions basic advanced pandas challenges

# Interactive mode with breakpoints
python python/learn_python.py --interactive --functions pandas

# Setup environment
python python/learn_python.py --setup-env

# Check environment status
python python/learn_python.py --env-status
```

### Copy Mode for Restricted Environments

Copy mode (`--cm` or `--copy-mode`) is designed for environments where Docker volume mounting is restricted:

```bash
# Basic copy mode
python python/learn_python.py --copy-mode

# Short form
python python/learn_python.py --cm

# Setup environment with copy mode
python python/learn_python.py --cm --setup-env

# Interactive learning with copy mode
python python/learn_python.py --cm --interactive --functions pandas

# Check status with copy mode enabled
python python/learn_python.py --cm --env-status
```

#### How Copy Mode Works

1. **Container Creation**: Creates Docker container without volume mounts
2. **File Sync To Container**: Copies project files into container before execution
3. **Background Sync**: Silent file synchronization every 2 seconds during interactive sessions
4. **File Sync From Container**: Copies results back to host after execution
5. **Clean Output**: No interference with interactive session formatting

#### Automatic Fallback

The system automatically detects when volume mounting fails and suggests copy mode:
```
❌ Failed to create container with volume mounting
💡 This might be due to filesystem restrictions in your environment
💡 Try using copy mode with: --copy-mode or --cm
💡 Copy mode copies files instead of mounting volumes
```

## Technical Details

### Docker Environment
- **Base Image**: `mambaorg/micromamba:1.5.6`
- **Python Version**: 3.11
- **Key Packages**: numpy, pandas, matplotlib, seaborn, jupyter, ipython
- **Environment**: Isolated with volume mounting for project access

### Environment Detection
The system automatically detects:
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

1. **Tested on Linux**: Compatible with various Linux distributions
2. **Copy Mode Support**: Operation in restricted environments where volume mounting isn't available
3. **Zero Configuration**: Automatic environment detection and setup
4. **Simple Experience**: Users don't need to know about containers
5. **Conflict Resolution**: Automatically handles library incompatibilities
6. **Clean Isolation**: No pollution of host environment
7. **Real-time File Sync**: Background synchronization in copy mode for immediate access to generated files
8. **Easy Cleanup**: Simple commands to remove everything

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

### Challenges Module
- Algorithmic problem solving
- Memoization and dynamic programming
- Common programming patterns
- Performance optimization techniques
- Step-by-step problem breakdowns

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
- For copy mode: Compatible with environments where volume mounting is restricted

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
    ├── pandas_module.py
    └── challenges.py
```

This architecture provides a robust Python learning environment that has been tested on Linux distributions and works regardless of many common system configuration issues.
