# Copy Mode Documentation

## Overview

Copy mode (`--cm` or `--copy-mode`) is a feature designed for environments where Docker volume mounting is restricted or not supported, such as sandboxed environments.

## How It Works

### Traditional Mode (Default)
- Uses Docker volume mounts (`-v` flag)
- Project directory is mounted directly into container
- Changes are immediately visible on both host and container
- Requires filesystem permission to create bind mounts

### Copy Mode (`--cm`)
- Creates container without volume mounts
- Copies project files into container before execution
- Copies results back after execution
- Works in restricted environments

## Usage

### Basic Copy Mode
```bash
python learn_python.py --copy-mode
python learn_python.py --cm  # Short form
```

### With Specific Functions
```bash
python learn_python.py --cm --function variables
python learn_python.py --cm --list-functions
```

### Interactive Mode
```bash
python learn_python.py --cm --interactive
```

## Automatic Fallback

The system automatically detects when volume mounting fails and suggests copy mode:

```
❌ Failed to create container with volume mounting
💡 This might be due to filesystem restrictions in your environment
💡 Try using copy mode with: --copy-mode or --cm
💡 Copy mode copies files instead of mounting volumes
```

When auto-fallback is enabled (default), the system will automatically switch to copy mode if mounting fails.

## File Synchronization

### Files Copied To Container
- All project files in the workspace directory
- Python scripts, configuration files, data files

### Files Copied Back From Container
- Python files (`*.py`)
- Output files (`*.txt`, `*.csv`, `*.json`)
- Image files (`*.png`, `*.jpg`, `*.svg`, etc.)
- Documentation (`*.md`)
- Results and output directories

### Excluded Files
- Git repository data (`.git/`)
- Python cache (`__pycache__/`)
- Temporary files
- System files

## Performance Considerations

### Copy Mode
- **Pros**: Works in all environments, good isolation
- **Cons**: Slower file sync, uses more disk space
- **Best for**: Restricted environments, one-off executions

### Mount Mode
- **Pros**: Fast, real-time sync, efficient
- **Cons**: Requires filesystem permissions
- **Best for**: Development environments, interactive work

## Environment Detection

The system can detect environments that benefit from copy mode:

```python
def detect_environment_conflicts():
    # Detects:
    # - Systems with filesystem restrictions
    # - Multiple Python installations
    # - Package conflicts
    # - C++ library issues
```

## Status Display

Check current mode status:

```bash
python learn_python.py --status
```

Output includes:
```
Docker Environment Status:
==================================================
Docker available: ✅ Yes
Image exists: ✅ Yes  
Container exists: ✅ Yes
Container running: ✅ Yes
Copy mode: ✅ Enabled
```

## Implementation Details

### Container Creation
- **Mount mode**: Uses `-v` flag for bind mounts
- **Copy mode**: Creates clean container without mounts

### File Operations
1. `sync_to_container()` - Copy files before execution
2. Script execution in container
3. `sync_from_container()` - Copy results back

### Error Handling
- Graceful fallback from mount to copy mode
- Clear error messages with suggestions
- Automatic cleanup on failures

## Troubleshooting

### "Permission denied" on mount
```bash
# Solution: Use copy mode
python learn_python.py --cm
```

### "No such file or directory" 
```bash
# Ensure Docker is running
docker info

# Rebuild if needed
python learn_python.py --cleanup
python learn_python.py --cm
```

### Files not syncing back
- Check file patterns in `sync_from_container()`
- Verify container exists and is running
- Check Docker logs: `docker logs codeit-python`

## Restricted Environments

Copy mode is specifically designed for environments with filesystem restrictions:

1. **Install Docker** (if available)
2. **Use copy mode**: `python learn_python.py --cm`
3. **Automatic fallback** handles mounting restrictions
4. **File synchronization** preserves your work

Example workflow:
```bash
# Setup
cd /path/to/codeit
python python/learn_python.py --cm --setup

# Learn Python
python python/learn_python.py --cm --function variables
python python/learn_python.py --cm --interactive

# Check status
python python/learn_python.py --cm --status
```
