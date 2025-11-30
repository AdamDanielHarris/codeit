"""
Docker Environment Manager - Seamless Docker integration for Python learning
"""

import os
import subprocess
import sys
from pathlib import Path


class DockerEnvironmentManager:
    """
    Manages Docker-based Python environments using the existing Mamba setup.
    Provides seamless integration with the host system while isolating dependencies.
    """
    
    def __init__(self, image_name="python-learning", container_name="python-learning-env"):
        self.image_name = image_name
        self.container_name = container_name
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.copy_mode = False  # Default to volume mounting
        self.force_docker = False  # Default to auto-detection
        
    def _run_docker_command(self, cmd, capture_output=True, check=True):
        """Run a docker command and return the result.
        
        Args:
            cmd: Command to run (list)
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit (if False, returns result with exit code)
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            # Return the exception (it has .returncode) so callers can check for
            # special exit codes like 42 (exit all sessions)
            if capture_output:
                print(f"Docker command failed: {' '.join(cmd)}")
                if e.stdout:
                    print(f"stdout: {e.stdout}")
                if e.stderr:
                    print(f"stderr: {e.stderr}")
            return e  # CalledProcessError has .returncode, .stdout, .stderr
    
    def is_docker_available(self):
        """Check if Docker is available and running."""
        result = self._run_docker_command(["docker", "--version"])
        if not result:
            return False
        
        # Check if Docker daemon is running
        result = self._run_docker_command(["docker", "info"], capture_output=True, check=False)
        return result is not None and result.returncode == 0
    
    def image_exists(self):
        """Check if the Docker image exists."""
        result = self._run_docker_command(["docker", "images", "-q", self.image_name])
        return result and result.stdout.strip() != ""
    
    def container_exists(self):
        """Check if a container with our name exists."""
        result = self._run_docker_command(["docker", "ps", "-a", "-q", "-f", f"name={self.container_name}"])
        return result and result.stdout.strip() != ""
    
    def is_container_running(self):
        """Check if the container is currently running and healthy."""
        # First check if it shows up in running containers
        result = self._run_docker_command(["docker", "ps", "-q", "-f", f"name={self.container_name}"])
        if not result or result.stdout.strip() == "":
            return False
        
        # Double-check by trying a simple command to ensure it's responsive
        test_result = self._run_docker_command([
            "docker", "exec", self.container_name, "/opt/conda/activate_env.sh", "echo", "test"
        ], check=False)
        return test_result is not None and test_result.returncode == 0
    
    def build_image(self):
        """Build the Docker image using the existing Dockerfile and environment.yml."""
        print(f"🐳 Building Docker image '{self.image_name}'...")
        
        # Build the image from the python directory
        cmd = [
            "docker", "build", 
            "-t", self.image_name,
            "-f", str(self.script_dir / "Dockerfile"),
            str(self.script_dir)
        ]
        
        result = self._run_docker_command(cmd, capture_output=False)
        return result is not None
    
    def create_container(self):
        """Create a new container with proper volume mounts and user permissions."""
        # Get current user's UID and GID to avoid permission issues
        import pwd
        import grp
        
        try:
            current_user = pwd.getpwuid(os.getuid())
            current_group = grp.getgrgid(os.getgid())
            uid = current_user.pw_uid
            gid = current_group.gr_gid
        except (KeyError, OSError):
            # Fallback if we can't get user info
            uid = os.getuid() if hasattr(os, 'getuid') else 1000
            gid = os.getgid() if hasattr(os, 'getgid') else 1000
        
        # Check if container exists and has correct user mapping
        if self.container_exists():
            # Check if existing container has correct user
            inspect_result = self._run_docker_command([
                "docker", "inspect", self.container_name, 
                "--format", "{{.Config.User}}"
            ])
            
            if inspect_result and inspect_result.stdout.strip() == f"{uid}:{gid}":
                print(f"Container '{self.container_name}' already exists with correct user permissions")
                return True
            else:
                print(f"Container '{self.container_name}' exists but has wrong user permissions, recreating...")
                # Remove the old container
                self._run_docker_command(["docker", "rm", "-f", self.container_name])
        
        if getattr(self, 'copy_mode', False):
            return self._create_container_copy_mode(uid, gid)
        else:
            return self._create_container_mount_mode(uid, gid)
    
    def _create_container_mount_mode(self, uid, gid):
        """Create container with volume mounting (traditional mode)."""
        print(f"🐳 Creating container '{self.container_name}' with volume mounting...")
        
        # Create container with volume mounts for the project and correct user
        cmd = [
            "docker", "create",
            "--name", self.container_name,
            "--user", f"{uid}:{gid}",
            "-v", f"{self.project_root}:/workspace",
            "-w", "/workspace",
            # Environment variables to fix matplotlib and fontconfig permission issues
            "-e", "MPLCONFIGDIR=/tmp/matplotlib",
            "-e", "FONTCONFIG_PATH=/tmp/fontconfig", 
            "-e", "XDG_CACHE_HOME=/tmp/cache",
            "-e", "MPLBACKEND=Agg",  # Use non-interactive backend
            "-it",
            self.image_name
        ]
        
        result = self._run_docker_command(cmd)
        
        # Check if mounting failed and suggest copy mode
        if result is None:
            print("❌ Failed to create container with volume mounting")
            print("💡 This might be due to filesystem restrictions in your environment")
            print("💡 Try using copy mode with: --copy-mode or --cm")
            print("💡 Copy mode copies files instead of mounting volumes")
        
        return result is not None
    
    def _create_container_copy_mode(self, uid, gid):
        """Create container without volume mounting (copy mode)."""
        print(f"🐳 Creating container '{self.container_name}' for copy mode...")
        
        # Create container without volume mounts
        cmd = [
            "docker", "create",
            "--name", self.container_name,
            "--user", f"{uid}:{gid}",
            "-w", "/workspace",
            # Environment variables to fix matplotlib and fontconfig permission issues
            "-e", "MPLCONFIGDIR=/tmp/matplotlib",
            "-e", "FONTCONFIG_PATH=/tmp/fontconfig", 
            "-e", "XDG_CACHE_HOME=/tmp/cache",
            "-e", "MPLBACKEND=Agg",  # Use non-interactive backend
            "-it",
            self.image_name
        ]
        
        result = self._run_docker_command(cmd)
        return result is not None
    
    def start_container(self):
        """Start the container if it's not running."""
        if self.is_container_running():
            return True
        
        if not self.container_exists():
            if not self.create_container():
                return False
        
        print(f"🐳 Starting container '{self.container_name}'...")
        result = self._run_docker_command(["docker", "start", self.container_name])
        
        # Wait a moment for container to start
        import time
        time.sleep(2)
        
        # Verify it's actually running
        if not self.is_container_running():
            print("⚠️  Container started but appears unresponsive, trying to restart...")
            return self.restart_container()
        
        return result is not None
    
    def restart_container(self):
        """Restart the container (stop and start again)."""
        print(f"🔄 Restarting container '{self.container_name}'...")
        
        # Remove the problematic container
        if self.container_exists():
            self._run_docker_command(["docker", "rm", "-f", self.container_name])
        
        # Create and start fresh
        if self.create_container():
            result = self._run_docker_command(["docker", "start", self.container_name])
            import time
            time.sleep(2)
            return self.is_container_running()
        
        return False
    
    def stop_container(self):
        """Stop the running container."""
        if not self.is_container_running():
            return True
        
        print(f"🐳 Stopping container '{self.container_name}'...")
        result = self._run_docker_command(["docker", "stop", self.container_name])
        return result is not None
    
    def remove_container(self):
        """Remove the container."""
        if self.is_container_running():
            self.stop_container()
        
        if self.container_exists():
            print(f"🐳 Removing container '{self.container_name}'...")
            result = self._run_docker_command(["docker", "rm", self.container_name])
            return result is not None
        return True
    
    def run_command_in_container(self, command, interactive=False):
        """Run a command inside the container."""
        if not self.start_container():
            return None
        
        # Prepare docker exec command with proper micromamba activation
        cmd = ["docker", "exec"]
        if interactive:
            cmd.extend(["-it"])
        cmd.extend([
            self.container_name,
            "/opt/conda/activate_env.sh",
            "bash", "-c", command
        ])
        
        if interactive:
            # For interactive commands, don't capture output and don't check
            # so we can capture special exit codes like 42 (exit all sessions)
            result = self._run_docker_command(cmd, capture_output=False, check=False)
        else:
            result = self._run_docker_command(cmd)
        
        # If the command failed due to container issues, try restarting
        if result is None and not interactive:
            print("⚠️  Command failed, attempting to restart container...")
            if self.restart_container():
                print("🔄 Retrying command after container restart...")
                result = self._run_docker_command(cmd)
        
        return result
    
    def run_interactive_with_sync(self, command):
        """Run interactive command with periodic sync in copy mode."""
        import threading
        import time
        import signal
        import sys
        
        if not self.start_container():
            return None
        
        print("📋 Copy mode: Starting interactive session with auto-sync...")
        print("💡 Files will be synced back periodically during the session")
        
        # Prepare docker exec command with proper micromamba activation
        cmd = ["docker", "exec", "-it", self.container_name, "/opt/conda/activate_env.sh", "bash", "-c", command]
        
        # Flag to control sync thread
        sync_active = threading.Event()
        sync_active.set()
        
        def sync_periodically():
            """Background thread to sync files periodically."""
            while sync_active.is_set():
                time.sleep(2)  # Sync every 2 seconds
                if sync_active.is_set():  # Check again in case we're shutting down
                    try:
                        # Silent sync during background operation
                        self.sync_from_container(quiet=True)
                    except Exception as e:
                        # Don't print errors during background sync to avoid output interference
                        pass
        
        # Start background sync thread
        sync_thread = threading.Thread(target=sync_periodically, daemon=True)
        sync_thread.start()
        
        try:
            # Run the interactive command - don't check so we capture exit codes like 42
            result = self._run_docker_command(cmd, capture_output=False, check=False)
            return result
        finally:
            # Stop sync thread and do final sync
            sync_active.clear()
            print("\n📁 Performing final sync...")
            self.sync_from_container(quiet=False)
            print("✅ Interactive session ended, files synced")
    
    def run_python_script(self, script_path, *args):
        """Run a Python script inside the container."""
        # In copy mode, sync files to container first
        if getattr(self, 'copy_mode', False):
            if not self.sync_to_container():
                print("❌ Failed to sync files to container")
                return None
        
        # Convert absolute path to relative path from project root
        try:
            rel_path = Path(script_path).relative_to(self.project_root)
        except ValueError:
            # If path is not under project root, just use the filename
            rel_path = Path(script_path).name
        
        # Build command
        cmd_parts = ["python", str(rel_path)]
        cmd_parts.extend(args)
        command = " ".join(f'"{part}"' if " " in part else part for part in cmd_parts)
        
        # Check if this is an interactive session
        is_interactive = '--interactive' in args or '-i' in args
        
        # For interactive mode in copy mode, we need special handling
        if getattr(self, 'copy_mode', False) and is_interactive:
            result = self.run_interactive_with_sync(command)
        else:
            result = self.run_command_in_container(command, interactive=is_interactive)
        
        # In copy mode, sync files back from container after execution
        if getattr(self, 'copy_mode', False) and not is_interactive:
            if not self.sync_from_container(quiet=False):
                print("⚠️  Failed to sync files back from container")
        
        return result
    
    def get_python_path(self):
        """Get the Python executable path inside the container."""
        result = self.run_command_in_container("which python")
        if result and result.stdout:
            return result.stdout.strip()
        return "/opt/conda/envs/python-learning/bin/python"
    
    def setup_environment(self, copy_mode=False, rebuild=False):
        """Set up the complete Docker environment."""
        if not self.is_docker_available():
            print("❌ Docker is not available or not running")
            print("💡 Please install Docker and ensure it's running")
            return False
        
        # Store copy_mode for later use
        self.copy_mode = copy_mode
        
        # Handle rebuild - remove existing image and container
        if rebuild:
            print("🔨 Rebuild requested - removing existing container and image...")
            
            # Remove container if it exists
            if self.container_exists():
                print(f"🗑️  Removing existing container '{self.container_name}'...")
                if self.is_container_running():
                    self.stop_container()
                self.remove_container()
            
            # Remove image if it exists
            if self.image_exists():
                print(f"🗑️  Removing existing image '{self.image_name}'...")
                result = self._run_docker_command(["docker", "rmi", self.image_name])
                if result is None:
                    print("⚠️  Failed to remove image, but continuing with rebuild...")
            
            print("✅ Cleanup complete, proceeding with fresh build...")
        
        # Build image if it doesn't exist (or if we just removed it)
        if not self.image_exists():
            if not self.build_image():
                print("❌ Failed to build Docker image")
                return False
        
        # Try to start container 
        if not self.start_container():
            print("❌ Failed to start Docker container")
            return False
        
        print("✅ Docker environment is ready!")
        if self.copy_mode:
            print("📋 Copy mode enabled - files will be copied instead of mounted")
        return True
    
    def get_environment_info(self):
        """Get information about the Docker environment."""
        return {
            'manager_type': 'docker',
            'image_name': self.image_name,
            'container_name': self.container_name,
            'docker_available': self.is_docker_available(),
            'image_exists': self.image_exists(),
            'container_exists': self.container_exists(),
            'container_running': self.is_container_running(),
            'python_path': self.get_python_path() if self.is_container_running() else None
        }
    
    def show_environment_status(self):
        """Display detailed environment status."""
        info = self.get_environment_info()
        
        print("Docker Environment Status:")
        print("=" * 50)
        print(f"Docker available: {'✅ Yes' if info['docker_available'] else '❌ No'}")
        print(f"Image exists: {'✅ Yes' if info['image_exists'] else '❌ No'}")
        print(f"Container exists: {'✅ Yes' if info['container_exists'] else '❌ No'}")
        print(f"Container running: {'✅ Yes' if info['container_running'] else '❌ No'}")
        print(f"Copy mode: {'✅ Enabled' if getattr(self, 'copy_mode', False) else '❌ Disabled'}")
        
        if info['container_running']:
            print(f"Python path: {info['python_path']}")
            
            # Show package list
            result = self.run_command_in_container("pip list | head -10")
            if result and result.stdout:
                print("\nInstalled packages (sample):")
                for line in result.stdout.strip().split('\n')[:5]:
                    if line.strip():
                        print(f"  {line}")
    
    def cleanup(self):
        """Clean up Docker resources."""
        success = True
        
        if self.container_exists():
            if not self.remove_container():
                success = False
        
        if self.image_exists():
            print(f"🐳 Removing image '{self.image_name}'...")
            result = self._run_docker_command(["docker", "rmi", self.image_name])
            if not result:
                success = False
        
        return success
    
    def sync_to_container(self):
        """Copy project files to container (copy mode only)."""
        if not getattr(self, 'copy_mode', False):
            return True  # No sync needed in mount mode
        
        if not self.container_exists():
            print("❌ Container doesn't exist for file sync")
            return False
        
        print("📂 Syncing files to container...")
        
        # Copy the entire project directory to the container
        result = self._run_docker_command([
            "docker", "cp", 
            f"{self.project_root}/.", 
            f"{self.container_name}:/workspace/"
        ])
        
        if result is not None:
            print("✅ Files synced to container")
            return True
        else:
            print("❌ Failed to sync files to container")
            return False
    
    def sync_from_container(self, quiet=False):
        """Copy files back from container (copy mode only)."""
        if not getattr(self, 'copy_mode', False):
            return True  # No sync needed in mount mode
        
        if not self.container_exists():
            if not quiet:
                print("❌ Container doesn't exist for file sync")
            return False
        
        # Use a more comprehensive approach to find all files
        # Look for all Python files and common output files
        patterns = [
            "*.py", "*.txt", "*.md", "*.json", "*.csv", 
            "*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg",
            "*.html", "*.pdf"
        ]
        
        files_found = []
        for pattern in patterns:
            result = self._run_docker_command([
                "docker", "exec", self.container_name,
                "bash", "-c", f"find /workspace -name '{pattern}' -type f 2>/dev/null"
            ], check=False)
            
            if result and result.stdout.strip():
                files_found.extend(result.stdout.strip().split('\n'))
        
        if not files_found:
            return True
        
        success = True
        files_copied = 0
        new_files = 0
        
        for file_path in files_found:
            file_path = file_path.strip()
            if not file_path or not file_path.startswith('/workspace/'):
                continue
                
            # Skip files we don't want to sync back
            if any(skip in file_path for skip in ['.git/', '__pycache__/', '.pyc', '/tmp/', '/opt/conda/']):
                continue
            
            # Calculate relative path from workspace
            rel_path = file_path[11:]  # Remove '/workspace/' prefix
            host_path = os.path.join(self.project_root, rel_path)
            
            # Check if this is a new file
            is_new_file = not os.path.exists(host_path)
            
            # Create directory if needed
            host_dir = os.path.dirname(host_path)
            if host_dir:
                os.makedirs(host_dir, exist_ok=True)
            
            # Copy the file
            copy_result = self._run_docker_command([
                "docker", "cp",
                f"{self.container_name}:{file_path}",
                host_path
            ], check=False)
            
            if copy_result and copy_result.returncode == 0:
                files_copied += 1
                if is_new_file:
                    new_files += 1
                    if not quiet:
                        print(f"📄 New file: {rel_path}")
            else:
                success = False
        
        if new_files > 0 and not quiet:
            print(f"✅ Synced {new_files} new files from container")
        elif files_copied > 0 and not quiet:
            # Only show this for manual syncs, not background syncs
            pass  
        
        return success


def detect_environment_conflicts():
    """
    Detect environment conflicts that would benefit from Docker isolation.
    """
    conflicts = []
    
    # Check for problematic numpy installations
    try:
        import numpy
        try:
            numpy.array([1, 2, 3])
        except Exception as e:
            if "libstdc++" in str(e) or "GLIBCXX" in str(e):
                conflicts.append("numpy: C++ library compatibility issues")
    except ImportError:
        pass
    
    # Check for pandas conflicts
    try:
        import pandas
        try:
            pandas.DataFrame({'test': [1, 2, 3]})
        except Exception as e:
            if "source directory" in str(e) or "build" in str(e):
                conflicts.append("pandas: Build/installation conflicts")
    except ImportError:
        pass
    
    # Check for multiple Python installations
    python_paths = []
    for path_dir in os.environ.get('PATH', '').split(':'):
        python_exe = os.path.join(path_dir, 'python3')
        if os.path.exists(python_exe):
            python_paths.append(python_exe)
    
    if len(python_paths) > 3:
        conflicts.append(f"Multiple Python installations: {len(python_paths)} found")
    
    return len(conflicts) > 0, conflicts


if __name__ == "__main__":
    # Test the Docker environment manager
    manager = DockerEnvironmentManager()
    
    print("Docker Environment Manager Test")
    print("=" * 40)
    
    # Show current info
    manager.show_environment_status()
    
    # Check for conflicts
    has_conflicts, conflict_list = detect_environment_conflicts()
    print(f"\nConflicts detected: {has_conflicts}")
    if conflict_list:
        for conflict in conflict_list:
            print(f"  - {conflict}")
    
    # Setup environment
    print("\nSetting up Docker environment...")
    if manager.setup_environment():
        print("✅ Docker environment ready!")
        manager.show_environment_status()
    else:
        print("❌ Failed to set up Docker environment")
