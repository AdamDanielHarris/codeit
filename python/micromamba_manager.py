"""
Micromamba Manager - Local micromamba installation and environment management
Alternative to Docker for cross-platform Python environment isolation
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path


def is_termux():
    """Detect if running in Termux environment."""
    return os.path.exists('/data/data/com.termux') or 'com.termux' in os.environ.get('PREFIX', '')


def is_proot_distro_available():
    """Check if proot-distro is installed in Termux."""
    try:
        result = subprocess.run(['which', 'proot-distro'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def is_debian_installed():
    """Check if Debian is installed via proot-distro."""
    try:
        # Try to login to debian - if it works, it's installed
        result = subprocess.run(
            ['proot-distro', 'login', 'debian', '--', 'echo', 'ok'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and 'ok' in result.stdout
    except Exception:
        return False


def install_proot_distro():
    """Install proot-distro in Termux. Returns True if successful."""
    print("📦 Installing proot-distro in Termux...")
    try:
        result = subprocess.run(['pkg', 'install', '-y', 'proot-distro'], capture_output=False)
        if result.returncode == 0:
            print("✅ proot-distro installed successfully")
            return True
        else:
            print("❌ Failed to install proot-distro")
            return False
    except Exception as e:
        print(f"❌ Error installing proot-distro: {e}")
        return False


def install_debian_distro():
    """Install Debian distribution via proot-distro. Returns True if successful."""
    print("📦 Installing Debian via proot-distro (this may take a few minutes)...")
    try:
        result = subprocess.run(['proot-distro', 'install', 'debian'], capture_output=False)
        if result.returncode == 0:
            print("✅ Debian installed successfully")
            return True
        else:
            print("❌ Failed to install Debian")
            return False
    except Exception as e:
        print(f"❌ Error installing Debian: {e}")
        return False


def prompt_install_proot_distro():
    """Prompt user to install proot-distro and Debian if not available."""
    if not is_proot_distro_available():
        print("\n⚠️  proot-distro is not installed.")
        print("   proot-distro with Debian is required for running micromamba in Termux.")
        print("   This provides a full Linux environment for the Python packages.\n")
        
        while True:
            response = input("Would you like to install proot-distro now? [y/n]: ").strip().lower()
            if response in ['y', 'yes']:
                if not install_proot_distro():
                    return False
                break
            elif response in ['n', 'no']:
                print("❌ proot-distro is required for micromamba on Termux. Aborting.")
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    if not is_debian_installed():
        print("\n⚠️  Debian is not installed in proot-distro.")
        print("   Debian will be downloaded and installed (~150MB).\n")
        
        while True:
            response = input("Would you like to install Debian now? [y/n]: ").strip().lower()
            if response in ['y', 'yes']:
                if not install_debian_distro():
                    return False
                break
            elif response in ['n', 'no']:
                print("❌ Debian is required for micromamba on Termux. Aborting.")
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    return True


class MicromambaManager:
    """
    Manages local micromamba installation and Python environments.
    Provides cross-platform environment isolation without Docker.
    Works on Linux, macOS, WSL, and Termux (Android) with proot-distro Debian.
    """
    
    def __init__(self, env_name="python-learning"):
        self.env_name = env_name
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.mamba_root = self.project_root / ".mamba"
        self.micromamba_bin = self.mamba_root / "bin" / "micromamba"
        
        # Termux/proot detection
        self.is_termux = is_termux()
        self.use_proot = self.is_termux
        self.proot_ready = False
        
        # Set environment variables for micromamba
        self.env_vars = os.environ.copy()
        self.env_vars['MAMBA_ROOT_PREFIX'] = str(self.mamba_root)
    
    def _ensure_proot(self):
        """Ensure proot-distro with Debian is available for Termux. Returns True if ready."""
        if not self.use_proot:
            return True
        
        if self.proot_ready:
            return True
        
        if not prompt_install_proot_distro():
            return False
        
        self.proot_ready = True
        return True
    
    def _get_proot_distro_command(self, command, include_mamba_env=True):
        """
        Build a proot-distro login command with bind mounts.
        
        Args:
            command: Command string to run inside Debian
            include_mamba_env: Whether to export MAMBA_ROOT_PREFIX inside proot
        
        Returns:
            Full command string to run via shell
        """
        # Bind mount the project directory so files are accessible inside and outside
        bind_args = f"--bind {self.project_root}:{self.project_root}"
        
        # Export MAMBA_ROOT_PREFIX inside proot so micromamba knows where to look
        if include_mamba_env:
            env_export = f'export MAMBA_ROOT_PREFIX="{self.mamba_root}" && '
            inner_cmd = env_export + command
        else:
            inner_cmd = command
        
        # Escape double quotes in the command
        inner_cmd_escaped = inner_cmd.replace('"', '\\"')
        
        # The command to run inside Debian
        return f'proot-distro login debian {bind_args} -- bash -c "{inner_cmd_escaped}"'
    
    def _run_in_proot(self, command, capture_output=True, check=True, include_mamba_env=True):
        """Run a command inside proot-distro Debian."""
        full_cmd = self._get_proot_distro_command(command, include_mamba_env=include_mamba_env)
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check,
                cwd=str(self.project_root)
            )
            return result
        except subprocess.CalledProcessError as e:
            if capture_output:
                print(f"Command failed: {command}")
                if e.stdout:
                    print(f"stdout: {e.stdout}")
                if e.stderr:
                    print(f"stderr: {e.stderr}")
            return None
        
    def _run_command(self, cmd, capture_output=True, check=True):
        """Run a command and return the result.
        
        On Termux, commands are run inside proot-distro Debian.
        On other platforms, commands are run directly.
        
        Args:
            cmd: Command to run (list or string)
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit
        """
        try:
            if self.use_proot:
                # Convert list command to string if needed
                if isinstance(cmd, list):
                    cmd_str = ' '.join(str(arg) for arg in cmd)
                else:
                    cmd_str = cmd
                return self._run_in_proot(cmd_str, capture_output=capture_output, check=check)
            else:
                # Run directly
                result = subprocess.run(
                    cmd,
                    capture_output=capture_output,
                    text=True,
                    check=check,
                    shell=isinstance(cmd, str),
                    env=self.env_vars
                )
                return result
        except subprocess.CalledProcessError as e:
            if capture_output:
                print(f"Command failed: {cmd}")
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
        # Ensure proot is available on Termux
        if self.use_proot and not self._ensure_proot():
            return False
        
        print("🐍 Installing micromamba...")
        print(f"   Installation directory: {self.mamba_root}")
        if self.is_termux:
            print("   📱 Termux detected - installing inside proot")
        
        # Create .mamba directory if it doesn't exist
        self.mamba_root.mkdir(parents=True, exist_ok=True)
        bin_dir = self.mamba_root / 'bin'
        bin_dir.mkdir(exist_ok=True)
        
        # Set up environment variables for the installer script
        # These variables control where micromamba gets installed
        install_env = os.environ.copy()
        install_env['MAMBA_ROOT_PREFIX'] = str(self.mamba_root)
        install_env['BIN_FOLDER'] = str(bin_dir)
        install_env['INIT_YES'] = 'no'  # Don't modify shell rc files
        install_env['CONDA_FORGE_YES'] = 'no'  # Don't add conda-forge by default
        
        # Build the install command with environment variables passed explicitly
        # Export the env vars inside the command so they're available to the script
        env_exports = f'export MAMBA_ROOT_PREFIX="{self.mamba_root}" BIN_FOLDER="{bin_dir}" INIT_YES=no CONDA_FORGE_YES=no'
        curl_cmd = 'curl -L micro.mamba.pm/install.sh | bash'
        base_install_cmd = f'{env_exports} && {curl_cmd}'
        
        if self.use_proot:
            # Run the install script inside proot-distro Debian with proper bind mounts
            # Don't add extra mamba env since we already export everything needed
            install_cmd = self._get_proot_distro_command(base_install_cmd, include_mamba_env=False)
        else:
            install_cmd = f'bash -c "{base_install_cmd}"'
        
        print("📥 Downloading and installing micromamba...")
        
        # Run the installation
        result = subprocess.run(
            install_cmd,
            shell=True,
            capture_output=False,
            env=install_env,
            cwd=str(self.project_root)
        )
        
        if result.returncode != 0:
            print("❌ Failed to install micromamba")
            return False
        
        # Verify installation
        if self.is_micromamba_installed():
            print(f"✅ Micromamba installed successfully at {self.micromamba_bin}")
            return True
        else:
            print("❌ Binary not found in expected location after installation")
            return False
    
    def environment_exists(self):
        """Check if the Python learning environment exists."""
        if not self.is_micromamba_installed():
            return False
        
        # Check if the environment directory actually exists
        env_dir = self.mamba_root / "envs" / self.env_name
        if not env_dir.exists():
            return False
        
        # Also verify with micromamba
        result = self._run_command(
            [str(self.micromamba_bin), "env", "list", "-r", str(self.mamba_root)],
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
                [str(self.micromamba_bin), "env", "remove", "-r", str(self.mamba_root), "-n", self.env_name, "-y"],
                capture_output=False
            )
            if result is None:
                print("⚠️  Failed to remove environment, but continuing...")
        
        # Create environment
        # Use --always-copy on Termux to avoid symlink issues
        create_cmd = [str(self.micromamba_bin), "create", "-r", str(self.mamba_root), "-f", str(env_file), "-y"]
        if self.is_termux:
            print(f"   📱 Using --always-copy for Termux compatibility")
            create_cmd.append("--always-copy")
        
        print(f"🔨 Creating environment '{self.env_name}' from {env_file}...")
        result = self._run_command(
            create_cmd,
            capture_output=False
        )
        
        if result is None:
            print("❌ Failed to create environment")
            return False
        
        # Clean up
        print("🧹 Cleaning up package cache...")
        self._run_command(
            [str(self.micromamba_bin), "clean", "-r", str(self.mamba_root), "--all", "-y"],
            capture_output=True
        )
        
        return True
    
    def setup_environment(self, rebuild=False):
        """Set up the complete micromamba environment."""
        # Ensure proot is available on Termux
        if self.use_proot:
            print("📱 Termux detected - using proot for environment isolation")
            if not self._ensure_proot():
                return False
        
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
        if self.is_termux:
            print("   📱 Running in proot on Termux")
        return True
    
    def get_activation_command(self):
        """Get the command to activate the environment."""
        base_cmd = f'eval "$({self.micromamba_bin} shell hook -s bash -r {self.mamba_root})" && {self.micromamba_bin} activate -r {self.mamba_root} {self.env_name}'
        if self.use_proot:
            # Wrap activation in proot-distro Debian for Termux
            return self._get_proot_distro_command(base_cmd)
        return base_cmd
    
    def run_python_script(self, script_path, *args):
        """Run a Python script in the micromamba environment."""
        if not self.environment_exists():
            print("❌ Environment not set up")
            return None
        
        # Use absolute path - the bind mount preserves the full path inside proot
        abs_path = Path(script_path).absolute()
        
        # Build command - run python through micromamba
        # Use -r to explicitly specify the root prefix
        cmd_parts = [
            str(self.micromamba_bin), "run",
            "-r", str(self.mamba_root),
            "-n", self.env_name,
            "python", str(abs_path)
        ]
        cmd_parts.extend(args)
        
        result = self._run_command(cmd_parts, capture_output=False)
        return result
    
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
                [str(self.micromamba_bin), "run", "-r", str(self.mamba_root), "-n", self.env_name, "bash", "-c", command],
                capture_output=False
            )
        
        return result
    
    def get_python_path(self):
        """Get the path to the Python executable in the environment."""
        if not self.environment_exists():
            return None
        
        result = self._run_command(
            [str(self.micromamba_bin), "run", "-r", str(self.mamba_root), "-n", self.env_name, "which", "python"],
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
            'micromamba_bin': str(self.micromamba_bin),
            'is_termux': self.is_termux,
            'use_proot': self.use_proot,
            'proot_distro_available': is_proot_distro_available() if self.is_termux else None,
            'debian_installed': is_debian_installed() if self.is_termux else None
        }
    
    def show_environment_status(self):
        """Display detailed environment status."""
        info = self.get_environment_info()
        
        print("Micromamba Environment Status:")
        print("=" * 50)
        
        # Show Termux/proot status
        if info['is_termux']:
            print(f"📱 Termux detected: ✅ Yes")
            print(f"   proot-distro available: {'✅ Yes' if info['proot_distro_available'] else '❌ No'}")
            print(f"   Debian installed: {'✅ Yes' if info['debian_installed'] else '❌ No'}")
        
        print(f"Micromamba installed: {'✅ Yes' if info['micromamba_installed'] else '❌ No'}")
        print(f"Installation path: {info['mamba_root']}")
        print(f"Environment exists: {'✅ Yes' if info['environment_exists'] else '❌ No'}")
        
        if info['environment_exists']:
            print(f"Environment name: {info['env_name']}")
            print(f"Python path: {info['python_path']}")
            
            # Show package list
            result = self._run_command(
                [str(self.micromamba_bin), "list", "-r", str(self.mamba_root), "-n", self.env_name],
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
        if self.is_termux:
            print("   # On Termux, commands run automatically inside proot")
            print("   python python/learn_python.py --functions basic --use-mamba")
        else:
            print(f"   eval \"$({self.micromamba_bin} shell hook -s bash)\"")
            print(f"   {self.micromamba_bin} activate {self.env_name}")
    
    def cleanup(self):
        """Remove the micromamba environment."""
        if self.environment_exists():
            print(f"🗑️  Removing environment '{self.env_name}'...")
            result = self._run_command(
                [str(self.micromamba_bin), "env", "remove", "-r", str(self.mamba_root), "-n", self.env_name, "-y"],
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
