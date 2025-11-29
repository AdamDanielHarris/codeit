"""
Micromamba Manager - Local micromamba installation and environment management
Alternative to Docker for cross-platform Python environment isolation
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path


class MicromambaManager:
    """
    Manages local micromamba installation and Python environments.
    Provides cross-platform environment isolation without Docker.
    Works on Linux, macOS, WSL, and Termux (Android).
    """
    
    def __init__(self, env_name="python-learning"):
        self.env_name = env_name
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.mamba_root = self.project_root / ".mamba"
        self.micromamba_bin = self.mamba_root / "bin" / "micromamba"
        
        # Set environment variables for micromamba
        self.env_vars = os.environ.copy()
        self.env_vars['MAMBA_ROOT_PREFIX'] = str(self.mamba_root)
        
    def _run_command(self, cmd, capture_output=True, check=True, shell=False):
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=check,
                shell=shell,
                env=self.env_vars
            )
            return result
        except subprocess.CalledProcessError as e:
            if capture_output:
                print(f"Command failed: {' '.join(cmd) if not shell else cmd}")
                if e.stdout:
                    print(f"stdout: {e.stdout}")
                if e.stderr:
                    print(f"stderr: {e.stderr}")
            return None
    
    def is_micromamba_installed(self):
        """Check if micromamba is installed in .mamba directory."""
        return self.micromamba_bin.exists()
    
    def install_micromamba(self):
        """Install micromamba using the official installation script."""
        print("🐍 Installing micromamba...")
        print(f"   Installation directory: {self.mamba_root}")
        
        # Create .mamba directory if it doesn't exist
        self.mamba_root.mkdir(parents=True, exist_ok=True)
        bin_dir = self.mamba_root / 'bin'
        bin_dir.mkdir(exist_ok=True)
        
        # Set up environment variables for non-interactive installation
        install_env = os.environ.copy()
        install_env['MAMBA_ROOT_PREFIX'] = str(self.mamba_root)
        # Override BIN_FOLDER to force installation in our directory
        install_env['BIN_FOLDER'] = str(bin_dir)
        
        # Download and run installation script with environment variables
        # The -b flag makes it non-interactive, BIN_FOLDER controls where it goes
        install_cmd = 'curl -L micro.mamba.pm/install.sh | bash -s -- -b'
        
        print("📥 Downloading and installing micromamba (non-interactive)...")
        
        # Use bash to run the installation
        result = subprocess.run(
            install_cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=install_env,
            cwd=str(self.project_root)
        )
        
        if result.returncode != 0:
            print("❌ Failed to install micromamba")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            print("💡 Trying alternative installation method...")
            return self._install_micromamba_direct()
        
        # Verify installation
        if self.is_micromamba_installed():
            print(f"✅ Micromamba installed successfully at {self.micromamba_bin}")
            return True
        else:
            print("⚠️  Binary not found in expected location, trying alternative method...")
            return self._install_micromamba_direct()
    
    def _install_micromamba_direct(self):
        """Download micromamba binary directly without using the installer script."""
        import platform
        import urllib.request
        
        print("📥 Downloading micromamba binary directly...")
        
        # Determine the correct binary URL based on platform
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Map architecture names
        if machine in ['x86_64', 'amd64']:
            arch = '64'
        elif machine in ['aarch64', 'arm64']:
            arch = 'aarch64'
        else:
            print(f"❌ Unsupported architecture: {machine}")
            return False
        
        # Construct download URL
        if system == 'linux':
            url = f'https://micro.mamba.pm/api/micromamba/linux-{arch}/latest'
        elif system == 'darwin':
            url = f'https://micro.mamba.pm/api/micromamba/osx-{arch}/latest'
        else:
            print(f"❌ Unsupported operating system: {system}")
            return False
        
        try:
            # Create bin directory
            bin_dir = self.mamba_root / 'bin'
            bin_dir.mkdir(parents=True, exist_ok=True)
            
            # Download binary
            print(f"   Downloading from: {url}")
            urllib.request.urlretrieve(url, str(self.micromamba_bin))
            
            # Make executable
            os.chmod(str(self.micromamba_bin), 0o755)
            
            if self.is_micromamba_installed():
                print(f"✅ Micromamba installed successfully at {self.micromamba_bin}")
                return True
            else:
                print("❌ Download completed but binary not working")
                return False
                
        except Exception as e:
            print(f"❌ Failed to download micromamba: {e}")
            return False
    
    def environment_exists(self):
        """Check if the Python learning environment exists."""
        if not self.is_micromamba_installed():
            return False
        
        result = self._run_command(
            [str(self.micromamba_bin), "env", "list"],
            capture_output=True
        )
        
        if result and result.stdout:
            return self.env_name in result.stdout
        return False
    
    def create_environment(self, rebuild=False):
        """Create the Python learning environment from environment.yml."""
        if not self.is_micromamba_installed():
            print("❌ Micromamba not installed")
            return False
        
        env_file = self.script_dir / "environment.yml"
        if not env_file.exists():
            print(f"❌ Environment file not found: {env_file}")
            return False
        
        # Remove existing environment if rebuild requested
        if rebuild and self.environment_exists():
            print(f"🗑️  Removing existing environment '{self.env_name}'...")
            result = self._run_command(
                [str(self.micromamba_bin), "env", "remove", "-n", self.env_name, "-y"],
                capture_output=False
            )
            if result is None:
                print("⚠️  Failed to remove environment, but continuing...")
        
        # Create environment
        print(f"🔨 Creating environment '{self.env_name}' from {env_file}...")
        result = self._run_command(
            [str(self.micromamba_bin), "create", "-f", str(env_file), "-y"],
            capture_output=False
        )
        
        if result is None:
            print("❌ Failed to create environment")
            return False
        
        # Clean up
        print("🧹 Cleaning up package cache...")
        self._run_command(
            [str(self.micromamba_bin), "clean", "--all", "-y"],
            capture_output=True
        )
        
        return True
    
    def setup_environment(self, rebuild=False):
        """Set up the complete micromamba environment."""
        # Check if micromamba is installed
        if not self.is_micromamba_installed():
            print("Micromamba not found in .mamba directory")
            if not self.install_micromamba():
                return False
        
        # Create or rebuild environment
        if not self.environment_exists() or rebuild:
            if not self.create_environment(rebuild=rebuild):
                return False
        else:
            print(f"✅ Environment '{self.env_name}' already exists")
        
        print("\n✅ Micromamba environment is ready!")
        return True
    
    def get_activation_command(self):
        """Get the command to activate the environment."""
        return f'eval "$({self.micromamba_bin} shell hook -s bash)" && {self.micromamba_bin} activate {self.env_name}'
    
    def run_python_script(self, script_path, *args):
        """Run a Python script in the micromamba environment."""
        if not self.environment_exists():
            print("❌ Environment not set up")
            return None
        
        # Convert absolute path to relative path from project root
        try:
            rel_path = Path(script_path).relative_to(self.project_root)
        except ValueError:
            rel_path = Path(script_path).name
        
        # Build command - run python through micromamba
        cmd_parts = [str(self.micromamba_bin), "run", "-n", self.env_name, "python", str(rel_path)]
        cmd_parts.extend(args)
        
        # Change to project root directory for execution
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_root)
            result = self._run_command(cmd_parts, capture_output=False)
            return result
        finally:
            os.chdir(original_dir)
    
    def run_command_in_environment(self, command, interactive=False):
        """Run a command in the micromamba environment."""
        if not self.environment_exists():
            print("❌ Environment not set up")
            return None
        
        # Build command
        if interactive:
            # For interactive sessions, use shell with activation
            activation = self.get_activation_command()
            full_cmd = f'{activation} && {command}'
            result = self._run_command(full_cmd, capture_output=False, shell=True)
        else:
            # For non-interactive, use micromamba run
            result = self._run_command(
                [str(self.micromamba_bin), "run", "-n", self.env_name, "bash", "-c", command],
                capture_output=False
            )
        
        return result
    
    def get_python_path(self):
        """Get the path to the Python executable in the environment."""
        if not self.environment_exists():
            return None
        
        result = self._run_command(
            [str(self.micromamba_bin), "run", "-n", self.env_name, "which", "python"],
            capture_output=True
        )
        
        if result and result.stdout:
            return result.stdout.strip()
        return None
    
    def get_environment_info(self):
        """Get information about the micromamba environment."""
        return {
            'manager_type': 'micromamba',
            'env_name': self.env_name,
            'mamba_root': str(self.mamba_root),
            'micromamba_installed': self.is_micromamba_installed(),
            'environment_exists': self.environment_exists(),
            'python_path': self.get_python_path() if self.environment_exists() else None,
            'micromamba_bin': str(self.micromamba_bin)
        }
    
    def show_environment_status(self):
        """Display detailed environment status."""
        info = self.get_environment_info()
        
        print("Micromamba Environment Status:")
        print("=" * 50)
        print(f"Micromamba installed: {'✅ Yes' if info['micromamba_installed'] else '❌ No'}")
        print(f"Installation path: {info['mamba_root']}")
        print(f"Environment exists: {'✅ Yes' if info['environment_exists'] else '❌ No'}")
        
        if info['environment_exists']:
            print(f"Environment name: {info['env_name']}")
            print(f"Python path: {info['python_path']}")
            
            # Show package list
            result = self._run_command(
                [str(self.micromamba_bin), "list", "-n", self.env_name],
                capture_output=True
            )
            if result and result.stdout:
                lines = result.stdout.strip().split('\n')
                print(f"\nInstalled packages (showing first 10):")
                for line in lines[:10]:
                    print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... and {len(lines) - 10} more")
        
        print("\n💡 Activate with:")
        print(f"   eval \"$({self.micromamba_bin} shell hook -s bash)\"")
        print(f"   {self.micromamba_bin} activate {self.env_name}")
    
    def cleanup(self):
        """Remove the micromamba environment."""
        if self.environment_exists():
            print(f"🗑️  Removing environment '{self.env_name}'...")
            result = self._run_command(
                [str(self.micromamba_bin), "env", "remove", "-n", self.env_name, "-y"],
                capture_output=False
            )
            return result is not None
        return True
    
    def cleanup_all(self):
        """Remove the entire .mamba directory."""
        if self.mamba_root.exists():
            print(f"🗑️  Removing entire micromamba installation at {self.mamba_root}...")
            try:
                shutil.rmtree(self.mamba_root)
                print("✅ Micromamba installation removed")
                return True
            except Exception as e:
                print(f"❌ Failed to remove: {e}")
                return False
        else:
            print("ℹ️  No micromamba installation found")
            return True
