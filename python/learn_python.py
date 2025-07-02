#!/usr/bin/env python3

import argparse
import code
import sys
import csv
import inspect
import subprocess
import os
import tempfile
import datetime
import re
import ast
import textwrap
import glob
from pathlib import Path
from docker_manager import DockerEnvironmentManager, detect_environment_conflicts
import urllib.request
import urllib.parse
try:
    import readline
    import rlcompleter
except ImportError:
    readline = None

# Import the modular learning modules
from modules import AVAILABLE_MODULES, setup_module_functions

# Global variable to track current context for cs() function
_current_context = 'basics'

# Global variables for snippet export
_snippet_mode = False
_current_module = None
_snippet_counter = 0
_current_snippet_lines = []
_snippet_messages = []  # Store all snippet messages to display at the end

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

# Available functions registry (now populated from modules)
AVAILABLE_FUNCTIONS = AVAILABLE_MODULES

def step_through_function(func, global_ns=None, local_ns=None):
    """
    Execute a function line by line, dropping into interactive mode after each line if step mode is enabled.
    Uses AST parsing to execute statements with proper context tracking.
    """
    import inspect, textwrap, ast
    global _current_context
    
    # Get the source code and dedent it for AST parsing
    source = inspect.getsource(func)
    source = textwrap.dedent(source)
    tree = ast.parse(source)
    
    # Extract the function body (skip the def line)
    func_node = tree.body[0]
    body_statements = func_node.body
    
    # Prepare the execution environment
    env = {}
    if global_ns:
        env.update(global_ns)
    if local_ns:
        env.update(local_ns)
    
    # Add necessary imports and functions to the environment
    env.update({
        'csv': csv,
        'os': os,
        'set_context': set_context_wrapper,
        'print': print,
        '_current_context': _current_context
    })
    
    print("🔍 Step-through mode: Executing function line by line...")
    print("   Use 'cm()' to see current variables, 'cs()' for help, 'exit()' to continue")
    print("-" * 60)
    
    # Execute each statement in the function body
    for i, stmt in enumerate(body_statements, 1):
        # Get the source line for display
        stmt_source = ast.get_source_segment(source, stmt)
        if stmt_source:
            # Clean up the source for display
            stmt_display = stmt_source.strip()
            print(f"Step {i}: {stmt_display}")
        
        # Compile and execute the statement
        stmt_code = compile(ast.Module(body=[stmt], type_ignores=[]), '<step>', 'exec')
        try:
            exec(stmt_code, env, env)
            
            # Update global context if it was modified
            if '_current_context' in env:
                _current_context = env['_current_context']
            
            # Drop into interactive shell if interactive mode is enabled
            if hasattr(check_interactive_mode, 'interactive_mode') and check_interactive_mode.interactive_mode:
                # Update the calling frame with new variables
                frame = sys._getframe(1)
                frame.f_locals.update(env)
                start_interactive_shell(env)
                
        except Exception as e:
            print(f"❌ Error executing statement: {e}")
            if hasattr(check_interactive_mode, 'interactive_mode') and check_interactive_mode.interactive_mode:
                print("Dropping into shell to debug...")
                frame = sys._getframe(1)
                frame.f_locals.update(env)
                start_interactive_shell(env)
            break
    
    print("-" * 60)
    print("✅ Step-through execution completed")

def set_context_wrapper(data_type):
    """
    Wrapper for set_context that works properly in step-through mode.
    Updates both local and global context variables.
    """
    global _current_context
    _current_context = data_type
    
    # Also update in the current execution frame
    frame = sys._getframe(1)
    if hasattr(frame, 'f_locals') and frame.f_locals:
        frame.f_locals['_current_context'] = data_type
    if hasattr(frame, 'f_globals') and frame.f_globals:
        frame.f_globals['_current_context'] = data_type


def start_interactive_shell(local_vars=None):
    """
    Starts an interactive Python shell with access to local variables.
    """
    if local_vars is None:
        local_vars = globals()
    
    # Filter to show only relevant local variables (exclude built-ins, modules, functions)
    relevant_vars = {}
    
    for name, value in local_vars.items():
        # Skip built-in variables and private variables
        if name.startswith('__') and name.endswith('__'):
            continue
        # Skip imported modules
        if hasattr(value, '__file__') and hasattr(value, '__name__'):
            continue
        # Skip functions defined in this module
        if callable(value) and hasattr(value, '__module__'):
            continue
        # Skip specific module names we know about
        if name in {'argparse', 'code', 'sys'}:
            continue
        # Include everything else (these should be the data variables we're working with)
        relevant_vars[name] = value
    
    print("\n" + "="*60)
    print("INTERACTIVE PYTHON SHELL")
    print("Type 'exit()', 'quit()', 'q', or press Ctrl+D to continue execution")
    print("Type 'cs()' for context help or 'cs(\"topic\")' for specific help")
    print("Type 'hf(\"function\")' for function docs, 'cm()' to show current variables")
    print("Type 'shortcuts()' or 'sc()' to see all available shortcuts")
    if _snippet_mode:
        print("Type 'save()' to save current snippet, 'saved()' to list recent snippets")
    
    # Display current context
    current_context = local_vars.get('_current_context', _current_context)
    if current_context:
        print(f"Current context: {current_context} (cs() will show help for python/{current_context})")
    
    print("-" * 60)
    
    if relevant_vars:
        print("Current variables:")
        for name, value in relevant_vars.items():
            print(f"  {name} = {repr(value)}")
    else:
        print("No local variables defined yet")
    
    # Show snippet contents if available
    global _snippet_messages
    if _snippet_mode and _snippet_messages:
        print()
        print("Snippet Contents:")
        print("-" * 40)
        
        # Read and display the most recent snippet file content
        try:
            # Get the most recent snippet message and extract the path
            recent_message = _snippet_messages[-1]
            if "practice/" in recent_message:
                # Extract path from message like "📝 Snippet exported: practice/pandas/001.py"
                file_path = recent_message.split(": ")[1]
                
                # Convert to absolute path
                if not file_path.startswith('/'):
                    # Relative path - convert to absolute
                    if os.path.exists('/workspace'):
                        # We're in Docker
                        abs_path = os.path.join('/workspace', file_path)
                    else:
                        # We're on host
                        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        abs_path = os.path.join(project_root, file_path)
                else:
                    abs_path = file_path
                
                # Read and display the snippet content
                if os.path.exists(abs_path):
                    with open(abs_path, 'r') as f:
                        content = f.read()
                    print(content)
                    print("-" * 40)
                    print(f"📁 Saved to: {file_path}")
                else:
                    print(f"⚠️  Snippet file not found: {abs_path}")
        except Exception as e:
            print(f"⚠️  Error reading snippet: {e}")
        
        # Don't remove the message so save() function can use it
        # _snippet_messages.pop()  # Remove the message we just showed
        print()
    
    print("="*60 + "\n")
    
    # Add convenient exit shortcuts to the local namespace
    local_vars_with_shortcuts = local_vars.copy()
    local_vars_with_shortcuts.update({
        'q': exit,
        'quit': exit,
        'exit': exit,
        'cs': cs,  # Add cheat.sh function
        'cm': cm,  # Add current memory function
        'save': save,  # Add snippet save function
        'saved': saved,  # Add saved function to list recent snippets
        'hf': hf,  # Add help file function
        'shortcuts': shortcuts,  # Add shortcuts display function
        'sc': sc,  # Add shortcuts alias
    })
    
    # Enable tab completion if readline is available
    if readline:
        # Create a custom completer that shows function signatures
        class SignatureCompleter(rlcompleter.Completer):
            def __init__(self, namespace=None):
                super().__init__(namespace)
                self.last_completion_context = None
                self.tab_count = 0
            
            def complete(self, text, state):
                # If we're completing inside parentheses, show function signature
                line = readline.get_line_buffer()
                if '(' in line and not line.rstrip().endswith(')'):
                    # Extract function name before parentheses
                    before_paren = line.split('(')[0].strip()
                    if '.' in before_paren:
                        parts = before_paren.split('.')
                        obj_name = parts[0]
                        method_name = parts[-1]
                        if obj_name in self.namespace:
                            obj = self.namespace[obj_name]
                            if hasattr(obj, method_name):
                                method = getattr(obj, method_name)
                                if callable(method):
                                    try:
                                        import inspect
                                        try:
                                            sig = inspect.signature(method)
                                        except (ValueError, TypeError):
                                            # Built-in methods don't have signatures, use fallback
                                            sig_str = f"({method_name}(...)"
                                            sig = sig_str
                                        
                                        # Check if this is the same completion context
                                        current_context = f"{obj_name}.{method_name}"
                                        if current_context == self.last_completion_context:
                                            self.tab_count += 1
                                        else:
                                            self.tab_count = 1
                                            self.last_completion_context = current_context
                                        
                                        if state == 0:
                                            current_line = readline.get_line_buffer()
                                            
                                            # Check if always showing docs is enabled
                                            always_show_docs = hasattr(check_interactive_mode, 'always_show_docs') and check_interactive_mode.always_show_docs
                                            
                                            if self.tab_count == 1 and not always_show_docs:
                                                # First tab: show signature only (unless --doc flag is set)
                                                if isinstance(sig, str):
                                                    print(f"\n{sig}")
                                                else:
                                                    print(f"\n{method_name}{sig}")
                                                print(f">>> {current_line}", end='', flush=True)
                                            else:
                                                # Second tab or --doc flag: show docstring and signature
                                                docstring = method.__doc__
                                                
                                                # For built-in methods, try to get better help text
                                                if not docstring or docstring.strip() == "":
                                                    try:
                                                        # Try to get help for built-in methods
                                                        import io
                                                        import contextlib
                                                        
                                                        f = io.StringIO()
                                                        with contextlib.redirect_stdout(f):
                                                            help(method)
                                                        help_text = f.getvalue()
                                                        
                                                        # Extract just the method description, not the full help
                                                        lines = help_text.split('\n')
                                                        for i, line in enumerate(lines):
                                                            if 'method' in line.lower() or 'function' in line.lower():
                                                                # Take the next few lines as description
                                                                desc_lines = []
                                                                for j in range(i+1, min(i+5, len(lines))):
                                                                    if lines[j].strip() and not lines[j].startswith('Help on'):
                                                                        desc_lines.append(lines[j].strip())
                                                                if desc_lines:
                                                                    docstring = ' '.join(desc_lines)
                                                                break
                                                    except:
                                                        pass
                                                
                                                if not docstring:
                                                    docstring = "No documentation available"
                                                
                                                # Clean up docstring - remove extra whitespace and format nicely
                                                docstring = ' '.join(docstring.split())
                                                
                                                # Wrap long lines at 80 characters
                                                if len(docstring) > 80:
                                                    import textwrap
                                                    wrapped_lines = textwrap.wrap(docstring, width=80)
                                                    docstring = '\n'.join(wrapped_lines)
                                                
                                                print(f"\n{docstring}")
                                                if isinstance(sig, str):
                                                    print(f"{sig}")
                                                else:
                                                    print(f"{method_name}{sig}")
                                                print(f">>> {current_line}", end='', flush=True)
                                            
                                            return None
                                    except Exception as e:
                                        # Debug: print the exception to see what's going wrong
                                        print(f"\nDebug: Error with {obj_name}.{method_name}: {e}")
                                        pass
                else:
                    # Reset tab count when not in function parentheses
                    self.last_completion_context = None
                    self.tab_count = 0
                
                # Default completion
                return super().complete(text, state)
        
        completer = SignatureCompleter(local_vars_with_shortcuts)
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")
    
    # Start interactive shell with all variables available (suppress default banner)
    code.interact(banner="", local=local_vars_with_shortcuts)

def check_interactive_mode():
    """
    Check if --interactive flag was passed and start interactive shell if so.
    Also export code snippets if --snip mode is enabled.
    """
    # Get current frame's local variables
    frame = sys._getframe(1)
    local_vars = {**frame.f_locals, **frame.f_globals}
    
    # Export snippet if snippet mode is enabled
    if _snippet_mode:
        export_snippet()
    
    # Check if we're in interactive mode (this will be set in main)
    if hasattr(check_interactive_mode, 'interactive_mode') and check_interactive_mode.interactive_mode:
        start_interactive_shell(local_vars)

# Bash completion support
def generate_bash_completion():
    """Generate bash completion script for this program."""
    script_name = sys.argv[0] if sys.argv else 'base_python.py'
    # Get function names dynamically from registry
    function_names = ' '.join(AVAILABLE_FUNCTIONS.keys())
    
    completion_script = f'''
# Bash completion for {script_name}
_{script_name.replace('.py', '').replace('-', '_')}_completion() {{
    local cur prev opts
    COMPREPLY=()
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    
    # Basic options
    opts="-i --interactive --doc --functions --list --bash-completion -h --help"
    
    # If previous word was --functions, complete with available function names
    if [[ "${{prev}}" == "--functions" ]] || [[ "${{COMP_WORDS[@]}}" =~ "--functions" && "${{prev}}" != "--"* ]]; then
        local functions="{function_names}"
        COMPREPLY=( $(compgen -W "${{functions}}" -- "${{cur}}") )
        return 0
    fi
    
    # Default completion with options
    COMPREPLY=( $(compgen -W "${{opts}}" -- "${{cur}}") )
    return 0
}}

complete -F _{script_name.replace('.py', '').replace('-', '_')}_completion {script_name}

# To enable completion, run: source <(python {script_name} --bash-completion)
# Or save to a file and source it: python {script_name} --bash-completion > ~/.bash_completion_python_basics
'''
    return completion_script.strip()

def detect_legacy_conflicts():
    """
    Detect legacy environment conflicts and suggest Docker environment.
    """
    # Check if we're in a directory that might cause import conflicts
    current_dir = os.getcwd()
    potential_conflicts = []
    
    # Check for common problematic directories/files
    for item in os.listdir(current_dir):
        if item.lower() in ['numpy', 'pandas', 'scipy', 'matplotlib']:
            if os.path.isdir(item):
                potential_conflicts.append(item)
    
    if potential_conflicts:
        print("⚠️  Potential import conflicts detected!")
        print(f"Found directories that might conflict with imports: {', '.join(potential_conflicts)}")
        print("💡 Recommended solutions:")
        print("   1. Run from a different directory")
        print("   2. Use Docker environment: python python/learn_python.py --setup-env")
        print("   3. Run with managed environment automatically")
        
        return True
    
    return False

def run_function_directly(func_key):
    """Run a function directly on the host."""
    try:
        func_info = AVAILABLE_FUNCTIONS.get(func_key)
        if not func_info:
            print(f"❌ Unknown function: {func_key}")
            return False
        
        # Extract the function object from the tuple (description, func)
        description, func = func_info
        if not func:
            print(f"❌ Function {func_key} is not callable")
            return False
        
        print(f"🚀 Running {func_key} directly on host...")
        func()
        return True
    except Exception as e:
        print(f"❌ Error running function directly: {e}")
        return False

def run_in_managed_environment(func_key, copy_mode=False, force_docker=False, no_docker=False):
    """
    Run a function in a Docker-managed environment.
    """
    try:
        # If Docker is explicitly disabled, run directly on host
        if no_docker:
            print("🏠 Running directly on host (Docker disabled with --no-docker)")
            return run_function_directly(func_key)
        
        # If Docker is forced, or if Docker is available and not disabled
        if force_docker:
            print("🔄 Running in Docker environment (forced with --force-docker)")
            manager = DockerEnvironmentManager()
            
            # Ensure environment is set up
            if not manager.setup_environment(copy_mode=copy_mode):
                print("❌ Failed to set up Docker environment")
                return False
            
            # Run the function in Docker
            print(f"🐳 Running {func_key} in Docker container...")
            script_path = os.path.abspath(__file__)
            args = ['--functions', func_key]
            
            # Add interactive mode flags if they're set
            if hasattr(check_interactive_mode, 'interactive_mode') and check_interactive_mode.interactive_mode:
                args.append('--interactive')
            if hasattr(check_interactive_mode, 'step_mode') and check_interactive_mode.step_mode:
                args.append('--step')
            if hasattr(check_interactive_mode, 'always_show_docs') and check_interactive_mode.always_show_docs:
                args.append('--doc')
            if _snippet_mode:
                args.append('--snip')
            if copy_mode:
                args.append('--cm')
            
            result = manager.run_python_script(script_path, *args)
            return result is not None and result.returncode == 0
        
        # Neither forced nor disabled, try running directly first
        return run_function_directly(func_key)
        
    except Exception as e:
        print(f"❌ Error running in managed environment: {e}")
        return False

# Main function
def main():
    # Setup module functions before parsing arguments
    setup_module_functions(set_context, check_interactive_mode, step_through_function, snippet_section)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Python basics demonstration with interactive mode')
    parser.add_argument('-i', '--interactive', action='store_true', default=True,
                       help='Enable interactive mode - drops into Python shell at breakpoints (default: True)')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Disable interactive mode')
    parser.add_argument('-s', '--step', action='store_true',
                       help='Step mode: drop into interactive shell after every line in csv_module')
    parser.add_argument('--doc', action='store_true',
                       help='Always show docstrings on first tab press (default: show on second tab)')
    parser.add_argument('--functions', nargs='*', 
                       help='Specify which functions to run (e.g., basic advanced pandas). If not specified, runs all.')
    parser.add_argument('--list', action='store_true',
                       help='List available functions and exit')
    parser.add_argument('--bash-completion', action='store_true',
                       help='Generate bash completion script and exit')
    parser.add_argument('--snip', action='store_true', default=True,
                       help='Export code snippets to practice/[module]/ folder for hands-on practice (default: True)')
    parser.add_argument('--no-snip', action='store_true',
                       help='Disable snippet export')
    parser.add_argument('--cm', '--copy-mode', action='store_true',
                      help='Use file copying instead of volume mounting (for restricted environments)')
    
    parser.add_argument('--force-docker', action='store_true',
                      help='Force using Docker for all operations, regardless of environment detection')
    
    parser.add_argument('--no-docker', action='store_true',
                      help='Disable Docker usage completely and run directly on host')
    
    # Python Environment Management Options
    parser.add_argument('--setup-env', action='store_true',
                       help='Set up a new Python environment with default packages')
    parser.add_argument('--activate-env', action='store_true',
                       help='Show how to activate the Python environment')
    parser.add_argument('--install-packages', nargs='+', metavar='PACKAGE',
                       help='Install packages in the Python environment')
    parser.add_argument('--env-status', action='store_true',
                       help='Show status of Python environments')
    parser.add_argument('--cleanup-env', action='store_true',
                       help='Clean up temporary Python environments')
    
    args = parser.parse_args()
    
    # Handle Python environment management options first
    if args.setup_env:
        copy_mode = getattr(args, 'cm', False)
        force_docker = getattr(args, 'force_docker', False)
        no_docker = getattr(args, 'no_docker', False)
        setup_mamba_environment(copy_mode=copy_mode, force_docker=force_docker, no_docker=no_docker)
        return
    
    if args.activate_env:
        show_mamba_activation()
        return
    
    if args.install_packages:
        print("❌ Direct package installation not yet implemented for Docker environments.")
        print("💡 Instead, edit python/environment.yml and run --setup-env to recreate environment.")
        return
    
    if args.env_status:
        mamba_environment_status()
        return
    
    if args.cleanup_env:
        cleanup_mamba_environments()
        return
    
    # Handle --bash-completion option
    if args.bash_completion:
        print(generate_bash_completion())
        return
    
    # Handle --list option
    if args.list:
        print("Available functions:")
        for key, (description, _) in AVAILABLE_FUNCTIONS.items():
            print(f"  {key}: {description}")
        return
    
    # Set interactive mode flag (default True, but can be disabled with --no-interactive)
    check_interactive_mode.interactive_mode = args.interactive and not args.no_interactive
    # Set always show docs flag
    check_interactive_mode.always_show_docs = args.doc
    # Set step mode flag (for csv_module)
    check_interactive_mode.step_mode = args.step
    
    # Set snippet export mode (default True, but can be disabled with --no-snip)
    global _snippet_mode
    _snippet_mode = args.snip and not args.no_snip
    
    # Set copy mode and Docker flags from args
    copy_mode = getattr(args, 'cm', False)
    force_docker = getattr(args, 'force_docker', False)
    no_docker = getattr(args, 'no_docker', False)

    # Prevent using both flags at the same time
    if force_docker and no_docker:
        print("❌ Error: --force-docker and --no-docker cannot be used at the same time.")
        return

    if force_docker:
        print("⚙️ Force Docker mode enabled - all functions will run in Docker container")
    
    if no_docker:
        print("🏠 No Docker mode enabled - all functions will run directly on host")
        
    if copy_mode:
        print("📋 Copy mode enabled - files will be copied instead of mounted")
    
    if check_interactive_mode.interactive_mode:
        print("Interactive mode enabled - you'll be dropped into a Python shell at breakpoints")
        if args.doc:
            print("Documentation mode enabled - docstrings will show on first tab press")
    else:
        print("Interactive mode disabled - running in demonstration-only mode")
    
    if _snippet_mode:
        print("Snippet export mode enabled - code sections will be saved to practice/[module]/ folders")
    else:
        print("Snippet export disabled")
    
    # Determine which functions to run
    if args.functions is not None:
        # Specific functions requested
        if not args.functions:
            # --functions was specified but no functions listed, show available and exit
            print("Available functions:")
            for key, (description, _) in AVAILABLE_FUNCTIONS.items():
                print(f"  {key}: {description}")
            print("\nUsage: --functions basic advanced pandas")
            return
        
        functions_to_run = args.functions
    else:
        # No --functions specified, run all functions
        functions_to_run = list(AVAILABLE_FUNCTIONS.keys())
    
    # Run selected functions
    for func_key in functions_to_run:
        if func_key in AVAILABLE_FUNCTIONS:
            description, func = AVAILABLE_FUNCTIONS[func_key]
            print(f"\nDemonstrating {description}:")
            
            # Set current module for snippet export
            if _snippet_mode:
                set_snippet_module(func_key)

            # Run the function in the appropriate environment
            if not run_in_managed_environment(func_key, copy_mode=copy_mode, force_docker=force_docker, no_docker=no_docker):
                print(f"❌ Failed to run {func_key}.")
            
            # Show any snippet messages that were collected during this function
            show_all_snippet_messages()
        else:
            print(f"Error: Unknown function '{func_key}'. Use --list to see available functions.")
            return

def cs(topic=None, save=False, full=False):
    """
    Cheat.sh integration for the interactive shell with file generation capabilities.
    Look up help on programming topics using cheat.sh.
    
    Args:
        topic (str, optional): Topic to look up. If None, tries to determine from current context.
        save (bool): If True, save code examples to practice files.
        full (bool): If True, save comprehensive help to organized files.
    
    Examples:
        cs()                    # Context-aware help
        cs("python/list")       # Python list help
        cs("python/dict/pop")   # Dictionary pop method
        cs("python/list", save=True)  # Save list examples to file
        cs("python/pandas", full=True)  # Save comprehensive help to file
    """
    import urllib.request
    import urllib.parse
    
    # If no topic specified, try to determine from current context
    if topic is None:
        if _current_context:
            topic = f"python/{_current_context}"
            print(f"📚 Looking up help for: {topic} (current context)")
        else:
            topic = "python"
            print(f"📚 Looking up help for: {topic} (default)")
    else:
        print(f"📚 Looking up help for: {topic}")
    
    try:
        # Clean up topic and construct URL
        topic = topic.strip('/')
        topic_for_curl = topic  # Always keep the original slash form for help message
        url = f"https://cheat.sh/{topic}"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'curl/7.68.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        # Check for 404 or unknown cheat sheet or unknown topic
        if (
            content.lstrip().startswith('#  404') or
            'Unknown cheat sheet' in content or
            'Unknown topic.' in content
        ):
            # Cascading fallback strategy
            fallback_topics = []
            
            # If topic has underscores, try replacing last underscore with dot
            if '_' in topic_for_curl:
                topic_underscore_to_dot = topic_for_curl.rsplit('_', 1)
                topic_underscore_to_dot = topic_underscore_to_dot[0] + '.' + topic_underscore_to_dot[1]
                fallback_topics.append(topic_underscore_to_dot)
            
            # If topic has slash, try removing the last part after slash
            if '/' in topic_for_curl:
                topic_base = topic_for_curl.rsplit('/', 1)[0]
                fallback_topics.append(topic_base)
            
            # Try each fallback in order
            for fallback_topic in fallback_topics:
                url_fallback = f"https://cheat.sh/{fallback_topic}"
                req_fallback = urllib.request.Request(url_fallback)
                req_fallback.add_header('User-Agent', 'curl/7.68.0')
                try:
                    with urllib.request.urlopen(req_fallback, timeout=10) as response_fallback:
                        content_fallback = response_fallback.read().decode('utf-8')
                    # Check if this fallback worked
                    if not (
                        content_fallback.lstrip().startswith('#  404') or
                        'Unknown cheat sheet' in content_fallback or
                        'Unknown topic.' in content_fallback
                    ):
                        content = content_fallback
                        print(f"🔄 Using fallback topic: {fallback_topic}")
                        break  # Success, stop trying fallbacks
                except Exception:
                    continue  # Try next fallback
        
        # Clean up content - remove excessive blank lines
        lines = content.split('\n')
        cleaned_lines = []
        prev_blank = False
        for line in lines:
            is_blank = line.strip() == ''
            if not (is_blank and prev_blank):
                cleaned_lines.append(line)
            prev_blank = is_blank
        content = '\n'.join(cleaned_lines[:50])
        
        # Display content
        print("=" * 60)
        print(content)
        print("=" * 60)
        print(f"💡 More help: curl cheat.sh/{topic_for_curl}")
        
        # Save to file if requested
        if save:
            save_code_to_file(content, topic_for_curl)
        
        # Save comprehensive help to file if requested
        if full:
            save_comprehensive_help(content, topic_for_curl)
            
    except Exception as e:
        print(f"❌ Error fetching help: {e}")
        print(f"💡 Try: curl cheat.sh/{topic}")
        print("💡 Common topics: python/list, python/dict, python/collections, python/dataclass")

def save_code_to_file(content, topic):
    """
    Save code examples to practice files with clean formatting.
    """
    # Strip ANSI color codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_content = ansi_escape.sub('', content)
    
    # Extract Python code blocks
    lines = clean_content.split('\n')
    code_blocks = []
    current_block = []
    in_code_block = False
    
    for line in lines:
        # Simple heuristic: lines that start with spaces or common Python patterns
        if (line.strip().startswith(('def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ', 'try:', 'with ')) or
            line.startswith('    ') or line.startswith('\t') or
            (line.strip() and not line.strip().startswith('#') and '=' in line and not line.strip().startswith('>'))):
            in_code_block = True
            current_block.append(line)
        elif in_code_block and line.strip() == '':
            current_block.append(line)
        elif in_code_block:
            if current_block:
                code_blocks.append('\n'.join(current_block))
                current_block = []
            in_code_block = False
    
    # Add any remaining block
    if current_block:
        code_blocks.append('\n'.join(current_block))
    
    if not code_blocks:
        print("⚠️  No Python code blocks found to save")
        return
    
    # Determine function name and create directory
    # Map topic names to function names
    topic_to_function = {
        'csv_writer': 'csv_module',
        'csv_reader': 'csv_module',
        'csv_dictreader': 'csv_module',
        'csv_dictwriter': 'csv_module',
        'dataframe': 'pandas',
        'dataframe_selection': 'pandas',
        'dataframe_stats': 'pandas',
        'dataframe_modify': 'pandas',
        'dataframe_manipulation': 'pandas',
        'series': 'pandas',
        'pandas_io': 'pandas',
    }
    
    # Extract base topic for directory naming
    if '/' in topic:
        base_topic = topic.split('/')[-1]
    else:
        base_topic = topic
    
    function_name = topic_to_function.get(base_topic, base_topic)
    
    # Create practice directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    practice_dir = os.path.join(base_dir, '..', 'practice', function_name)
    practice_dir = os.path.normpath(practice_dir)  # Normalize the path to remove ..
    os.makedirs(practice_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{base_topic}_example_{timestamp}.py"
    filepath = os.path.join(practice_dir, filename)
    filepath = os.path.normpath(filepath)  # Normalize the file path
    
    # Generate file content
    file_content = f"""#!/usr/bin/env python3
\"\"\"
Code examples for {topic}
Generated from cheat.sh on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
\"\"\"

"""
    
    # Add imports if needed
    if any('import ' in block or 'from ' in block for block in code_blocks):
        imports_added = set()
        for block in code_blocks:
            for line in block.split('\n'):
                if line.strip().startswith(('import ', 'from ')):
                    if line.strip() not in imports_added:
                        file_content += line.rstrip() + '\n'
                        imports_added.add(line.strip())
        file_content += '\n'
    
    # Add code blocks with proper indentation
    for i, block in enumerate(code_blocks):
        if i > 0:
            file_content += '\n' + '# ' + '-' * 50 + '\n\n'
        
        # Clean up and add the code block
        clean_block = '\n'.join(line.rstrip() for line in block.split('\n'))
        file_content += f"# Example {i + 1}\n"
        file_content += clean_block + '\n'
    
    # Write to file
    try:
        with open(filepath, 'w') as f:
            f.write(file_content)
        
        # Show relative paths for display (remove workspace prefix if present)
        if os.path.exists('/workspace'):
            # We're in Docker - convert Docker path to host path for display
            display_filepath = filepath.replace('/workspace/', '')
            display_practice_dir = practice_dir.replace('/workspace/', '')
        else:
            # We're on host - show relative path from project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            try:
                display_filepath = os.path.relpath(filepath, project_root)
                display_practice_dir = os.path.relpath(practice_dir, project_root)
            except ValueError:
                # If relative path fails, use the full path
                display_filepath = filepath
                display_practice_dir = practice_dir
        
        print(f"📁 Code saved to: {display_filepath}")
        print(f"📂 Practice directory: {display_practice_dir}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def save_comprehensive_help(content, topic):
    """
    Save comprehensive help content to organized files with clean formatting.
    This function handles the full help file saving logic.
    """
    import re
    
    # Clean up content - remove ANSI codes and format nicely
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_content = ansi_escape.sub('', content)
    
    # Create help directory structure
    if os.path.exists('/workspace'):
        # We're in Docker
        help_base = '/workspace/help'
    else:
        # We're on host
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        help_base = os.path.join(project_root, 'help')
    
    # Determine category for organization
    clean_topic = topic.strip('/')
    if '/' in clean_topic:
        parts = clean_topic.split('/')
        if parts[0] == 'python':
            if len(parts) > 1:
                if parts[1] in ['pandas', 'numpy', 'matplotlib']:
                    category = 'dataframes'
                elif parts[1] in ['list', 'dict', 'tuple', 'set']:
                    category = 'basics'
                elif parts[1] in ['collections', 'itertools', 'functools']:
                    category = 'advanced'
                else:
                    category = 'general'
            else:
                category = 'general'
        else:
            category = parts[0]
    else:
        category = 'general'
    
    # Create category directory
    help_dir = os.path.join(help_base, category)
    os.makedirs(help_dir, exist_ok=True)
    
    # Generate filename
    safe_filename = clean_topic.replace('/', '_').replace(' ', '_')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_filename}_{timestamp}.txt"
    filepath = os.path.join(help_dir, filename)
    
    # Create well-formatted content
    formatted_content = f"""Help for: {topic}
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: cheat.sh/{clean_topic}
{'=' * 60}

{clean_content}

{'=' * 60}
End of help content
"""
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        # Show relative path for display
        if os.path.exists('/workspace'):
            display_path = filepath.replace('/workspace/', '')
        else:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            display_path = os.path.relpath(filepath, project_root)
        
        print(f"✅ Full help saved to: {display_path}")
        print(f"📂 Category: {category}")
        print(f"💡 Open this file in your editor for easier reading!")
        
    except Exception as e:
        print(f"❌ Error saving comprehensive help: {e}")

def save_function_help_to_file(function_name, signature_str, docstring):
    """
    Save function documentation to organized files with clean formatting.
    """
    # Create help directory structure
    if os.path.exists('/workspace'):
        # We're in Docker
        help_base = '/workspace/help'
    else:
        # We're on host
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        help_base = os.path.join(project_root, 'help')
    
    # Determine category for organization based on function type
    if '.' in function_name:
        # This is a method or attribute (e.g., 'df.combine', 'list.append')
        parts = function_name.split('.')
        if parts[0] in ['df', 'pd', 'pandas']:
            category = 'dataframes'
        elif parts[0] in ['np', 'numpy']:
            category = 'dataframes'
        elif parts[0] in ['list', 'dict', 'tuple', 'set', 'str']:
            category = 'basics'
        else:
            category = 'functions'
    else:
        # Built-in function or simple name
        if function_name in ['len', 'max', 'min', 'sum', 'abs', 'round', 'sorted', 'reversed']:
            category = 'basics'
        elif function_name in ['print', 'input', 'open', 'range', 'enumerate', 'zip']:
            category = 'basics'
        else:
            category = 'functions'
    
    # Create category directory
    help_dir = os.path.join(help_base, category)
    os.makedirs(help_dir, exist_ok=True)
    
    # Generate filename
    safe_filename = function_name.replace('.', '_').replace(' ', '_')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"function_{safe_filename}_{timestamp}.txt"
    filepath = os.path.join(help_dir, filename)
    
    # Create well-formatted content
    formatted_content = f"""Function Documentation: {function_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: Python inspection
{'=' * 60}

🔧 SIGNATURE:
{signature_str if signature_str else f"{function_name}(...)"}

📝 DOCUMENTATION:
{docstring if docstring else "No documentation available"}

{'=' * 60}
End of function documentation
"""
    
    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        # Show relative path for display
        if os.path.exists('/workspace'):
            display_path = filepath.replace('/workspace/', '')
        else:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            display_path = os.path.relpath(filepath, project_root)
        
        print(f"✅ Function help saved to: {display_path}")
        print(f"📂 Category: {category}")
        print(f"💡 Open this file in your editor for easier reading!")
        
    except Exception as e:
        print(f"❌ Error saving function help: {e}")

def cm():
    """
    Show current variables in the interactive shell.
    Recreates the "Current variables:" message from shell entry.
    """
    # Get current frame's local variables
    frame = sys._getframe(1)
    local_vars = {**frame.f_locals, **frame.f_globals}
    
    # Filter to show only relevant local variables (same logic as start_interactive_shell)
    relevant_vars = {}
    
    for name, value in local_vars.items():
        # Skip built-in variables and private variables
        if name.startswith('__') and name.endswith('__'):
            continue
        # Skip imported modules
        if hasattr(value, '__file__') and hasattr(value, '__name__'):
            continue
        # Skip functions defined in this module
        if callable(value) and hasattr(value, '__module__'):
            continue
        # Skip specific module names we know about
        if name in {'argparse', 'code', 'sys'}:
            continue
        # Include everything else (these should be the data variables we're working with)
        relevant_vars[name] = value
    
    # Display in same format as start_interactive_shell
    if relevant_vars:
        print("Current variables:")
        for name, value in relevant_vars.items():
            print(f"  {name} = {repr(value)}")
    else:
        print("No local variables defined yet")

# Python Environment Management Functions (based on temp/functions patterns)

def get_temp_python_dirs():
    """Find all temppython directories in the temp directory."""
    temp_dir = os.environ.get('TMPDIR', '/tmp')
    pattern = os.path.join(temp_dir, 'temppython*')
    import glob
    return glob.glob(pattern)

def validate_python_env(temp_dir):
    """Validate that a Python environment is working properly."""
    try:
        venv_python = os.path.join(temp_dir, '.venv', 'bin', 'python3')
        venv_pip = os.path.join(temp_dir, '.venv', 'bin', 'pip3')
        
        # Test that pip works
        result = subprocess.run([venv_pip, '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False

def install_python_packages(packages, temp_dir=None):
    """Install Python packages using the pattern from temp/functions."""
    if temp_dir is None:
        # Create new temporary environment
        temp_dir = tempfile.mkdtemp(prefix='temppython-', dir=os.environ.get('TMPDIR', '/tmp'))
        print(f"Warning: Python3 modules not found, trying to install them")
        print(f"Creating temporary environment: {temp_dir}")
        
        # Create virtual environment
        subprocess.run([sys.executable, '-m', 'venv', os.path.join(temp_dir, '.venv')], 
                      check=True)
        
        # Activate and upgrade pip
        venv_pip = os.path.join(temp_dir, '.venv', 'bin', 'pip3')
        subprocess.run([venv_pip, 'install', '--upgrade', 'pip'], check=True)
    else:
        venv_pip = os.path.join(temp_dir, '.venv', 'bin', 'pip3')
    
    # Install packages
    for package in packages:
        print(f"Installing {package}...")
        subprocess.run([venv_pip, 'install', package], check=True)
        print(f"✓ {package} installed successfully")
    
    return temp_dir

def get_python_with_pip_packages(packages):
    """
    Get Python environment with specified packages, following temp/functions pattern.
    Returns the path to the environment directory.
    """
    # Define mapping between pip package names and their import names
    pip_packages = {
        "pyyaml": "yaml"
    }
    
    # Find existing temppython directories
    temppython_dirs = get_temp_python_dirs()
    
    # Validate existing temp directories - if any have broken pip, remove ALL
    if temppython_dirs:
        for temp_dir in temppython_dirs:
            if not validate_python_env(temp_dir):
                print("Found broken python temp directory, removing ALL temp directories")
                for dir_to_remove in temppython_dirs:
                    print(f"Removing: {dir_to_remove}")
                    import shutil
                    shutil.rmtree(dir_to_remove, ignore_errors=True)
                temppython_dirs = []
                break
    
    # If there are any temppython directories, use the most recent one
    if temppython_dirs:
        temp_dir = max(temppython_dirs, key=os.path.getmtime)
        print(f"Using existing Python environment: {temp_dir}")
        
        venv_python = os.path.join(temp_dir, '.venv', 'bin', 'python3')
        venv_pip = os.path.join(temp_dir, '.venv', 'bin', 'pip3')
        
        # Silently upgrade pip
        try:
            subprocess.run([venv_pip, 'install', '--upgrade', 'pip'], 
                          capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("Failed to upgrade pip")
            return None
        
        # Check if the python3 modules are installed
        for package in packages:
            import_name = pip_packages.get(package, package)
            
            result = subprocess.run([venv_python, '-c', f'import {import_name}'], 
                                  capture_output=True)
            if result.returncode == 0:
                print(f"✓ {package} (imports as '{import_name}') is installed here: {temp_dir}")
            else:
                print(f"✗ {package} (imports as '{import_name}') is not installed")
                print(f"Trying to install {package}")
                try:
                    subprocess.run([venv_pip, 'install', package], check=True)
                    print(f"✓ {package} installed successfully")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {package}, falling back to new environment")
                    return install_python_packages(packages)
        
        return temp_dir
    else:
        # No existing directories, create new one
        return install_python_packages(packages)

def ensure_python_with_yaml():
    """Ensure Python3 and PyYAML are available, following temp/functions pattern."""
    try:
        import yaml
        print("✓ PyYAML is available in current Python environment")
        return None
    except ImportError:
        print("PyYAML not found in active Python environment")
        return get_python_with_pip_packages(['pyyaml'])

def show_mamba_activation():
    """Show how to activate the Docker environment."""
    try:
        manager = DockerEnvironmentManager()
        info = manager.get_environment_info()
        
        print("Docker Environment Status:")
        print("=" * 40)
        
        if info['docker_available']:
            if info['container_running']:
                print("✅ Docker environment is active!")
                print(f"Container: {info['container_name']}")
                print(f"Python path: {info['python_path']}")
                print("\n💡 To run commands manually:")
                print(f"  docker exec -it {info['container_name']} bash")
            elif info['container_exists']:
                print("⏸️  Docker environment exists but not running")
                print("💡 Start it with: python python/learn_python.py --setup-env")
            else:
                print("❌ Docker environment not set up")
                print("💡 Create it with: python python/learn_python.py --setup-env")
        else:
            print("❌ Docker is not available")
            print("💡 Please install Docker and ensure it's running")
            
    except Exception as e:
        print(f"❌ Error checking Docker environment: {e}")

def setup_mamba_environment(copy_mode=False, force_docker=False, no_docker=False):
    """Set up a Docker environment with all required packages."""
    try:
        if no_docker:
            print("🚫 Docker usage explicitly disabled with --no-docker flag")
            print("📝 Running all Python operations directly on host")
            return True
            
        manager = DockerEnvironmentManager()
        
        print("🚀 Setting up Docker environment for Python learning...")
        if force_docker:
            print("⚙️ Docker usage forced with --force-docker flag")
            print("📝 All Python operations will use Docker container")
            
        if copy_mode:
            print("📋 Copy mode enabled - using file copying instead of volume mounting")
            
        print("This will create a Docker container with Python 3.11, numpy, pandas, matplotlib, and more.")
        
        if manager.setup_environment(copy_mode=copy_mode, force_docker=force_docker):
            print("\n✅ Docker environment set up successfully!")
            if copy_mode:
                print("📁 Container ready for file copying operations")
            show_mamba_activation()
            return True
        else:
            print("❌ Failed to set up Docker environment")
            return False
    except Exception as e:
        print(f"❌ Error setting up environment: {e}")
        return False

def mamba_environment_status():
    """Show status of Docker environment."""
    try:
        manager = DockerEnvironmentManager()
        manager.show_environment_status()
        
    except Exception as e:
        print(f"❌ Error checking environment status: {e}")

def cleanup_mamba_environments():
    """Clean up Docker environments."""
    try:
        manager = DockerEnvironmentManager()
        
        print("Docker Environment Cleanup")
        print("=" * 50)
        
        info = manager.get_environment_info()
        
        if info['container_exists'] or info['image_exists']:
            print("Found Docker resources:")
            if info['container_exists']:
                print(f"  - Container: {info['container_name']}")
            if info['image_exists']:
                print(f"  - Image: {info['image_name']}")
            
            response = input("Remove Docker environment? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                if manager.cleanup():
                    print("✅ Docker environment cleaned up.")
                else:
                    print("❌ Some cleanup operations failed.")
            else:
                print("Cleanup cancelled.")
        else:
            print("No Docker environment found.")
            
        # Also clean up legacy temp environments
        temp_dirs = get_temp_python_dirs()
        if temp_dirs:
            print(f"\nFound {len(temp_dirs)} legacy temporary environment(s):")
            for temp_dir in temp_dirs:
                print(f"  {temp_dir}")
            
            response = input("Remove legacy temporary environments? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                import shutil
                for temp_dir in temp_dirs:
                    print(f"Removing: {temp_dir}")
                    shutil.rmtree(temp_dir, ignore_errors=True)
                print("✅ All legacy environments removed.")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def export_snippet(frame=None):
    """Export the current code snippet to practice/[module]/XXX.py file."""
    # This will be called by check_interactive_mode(), but we'll use a different
    # approach - track code through context changes instead
    pass

def snippet_section(code_lines, description=None):
    """
    Export a code section as a snippet if snippet mode is enabled.
    
    Args:
        code_lines: List of code lines or a single multiline string
        description: Optional description for the snippet
    """
    global _snippet_counter, _snippet_messages
    
    if not _snippet_mode or not _current_module:
        return
    
    try:
        # Determine the appropriate practice directory
        # Check if we're running in Docker container
        if os.path.exists('/workspace'):
            # We're in Docker - try multiple approaches to handle permissions
            practice_base = '/workspace/practice'
            practice_dir = os.path.join(practice_base, _current_module)
            
            # First try to create the directory normally
            try:
                os.makedirs(practice_dir, exist_ok=True)
            except PermissionError:
                # If permission denied, try using /tmp and then copying
                print(f"⚠️  Permission denied creating {practice_dir}, using /tmp fallback")
                practice_dir = os.path.join('/tmp', 'practice', _current_module)
                os.makedirs(practice_dir, exist_ok=True)
        else:
            # We're on host system
            practice_dir = os.path.join(os.path.dirname(__file__), '..', 'practice', _current_module)
            os.makedirs(practice_dir, exist_ok=True)
        
        # Increment counter and create filename
        _snippet_counter += 1
        filename = os.path.join(practice_dir, f'{_snippet_counter:03d}.py')
        
        # Convert single string to lines if needed
        if isinstance(code_lines, str):
            code_lines = code_lines.strip().split('\n')
        
        # Write the code snippet
        with open(filename, 'w') as f:
            # Add a header comment
            f.write(f"# {_current_module.title()} Practice Snippet {_snippet_counter}\n")
            if description:
                f.write(f"# {description}\n")
            f.write(f"# Extracted from interactive learning session\n\n")
            
            # Add necessary imports based on content
            content = '\n'.join(code_lines)
            imports_added = set()
            
            if 'pd.' in content and 'import pandas' not in content:
                f.write("import pandas as pd\n")
                imports_added.add('pandas')
            
            if 'np.' in content and 'import numpy' not in content:
                f.write("import numpy as np\n")
                imports_added.add('numpy')
                
            if 'csv.' in content and 'import csv' not in content:
                f.write("import csv\n")
                imports_added.add('csv')
                
            if 'os.' in content and 'import os' not in content:
                f.write("import os\n")
                imports_added.add('os')
            
            if imports_added:
                f.write("\n")
            
            # Write the actual code
            for line in code_lines:
                f.write(line.rstrip() + '\n')
        
        # If we used /tmp fallback, try to copy to the correct location
        if os.path.exists('/workspace') and '/tmp/practice' in practice_dir:
            try:
                import shutil
                target_dir = os.path.join('/workspace/practice', _current_module)
                target_file = os.path.join(target_dir, f'{_snippet_counter:03d}.py')
                
                # Try to create target directory with different permissions
                os.makedirs(target_dir, mode=0o777, exist_ok=True)
                shutil.copy2(filename, target_file)
                
                # Convert Docker path to host path for display
                host_path = target_file.replace('/workspace/', '')  # Remove /workspace prefix
                snippet_message = f"📝 Snippet exported: {host_path}"
                
                # Store for later display
                _snippet_messages.append(snippet_message)
                
                # Clean up temp file
                os.remove(filename)
            except Exception as copy_error:
                snippet_message = f"📝 Snippet exported to temp location: {filename}"
                _snippet_messages.append(snippet_message)  # Store instead of printing
                # Don't print immediately - let interactive shell handle it
        else:
            # Determine display path based on context
            if os.path.exists('/workspace'):
                # We're in Docker - convert Docker path to host path for display
                display_path = filename.replace('/workspace/', '')  # Remove /workspace prefix
                snippet_message = f"📝 Snippet exported: {display_path}"
            else:
                # We're on host - show relative path from project root
                # Convert absolute path to relative path for display
                try:
                    # Get the absolute path of the project root (parent of python directory)
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    relative_path = os.path.relpath(filename, project_root)
                    snippet_message = f"📝 Snippet exported: {relative_path}"
                except:
                    # Fallback to just the filename if path calculation fails
                    snippet_message = f"📝 Snippet exported: {filename}"
            
            # Store for later display
            _snippet_messages.append(snippet_message)
        
    except Exception as e:
        print(f"⚠️  Failed to export snippet: {e}")
        print(f"Debug info: Docker container={os.path.exists('/workspace')}, Module={_current_module}, Mode={_snippet_mode}")
        # Try to provide helpful debugging information
        if os.path.exists('/workspace'):
            try:
                workspace_contents = os.listdir('/workspace')
                print(f"Workspace contents: {workspace_contents}")
                if 'practice' in workspace_contents:
                    practice_contents = os.listdir('/workspace/practice')
                    print(f"Practice directory contents: {practice_contents}")
                    # Check permissions
                    import stat
                    practice_stat = os.stat('/workspace/practice')
                    permissions = oct(practice_stat.st_mode)[-3:]
                    print(f"Practice directory permissions: {permissions}")
            except Exception as debug_e:
                print(f"Debug error: {debug_e}")

def set_snippet_module(module_name):
    """Set the current module for snippet export."""
    global _current_module, _snippet_counter
    _current_module = module_name
    _snippet_counter = 0  # Reset counter for new module

def show_all_snippet_messages():
    """Display all collected snippet export messages at the end."""
    global _snippet_messages
    if _snippet_mode and _snippet_messages:
        print()  # Add some spacing
        for message in _snippet_messages:
            print(message)
        print("💡 You can now work with these snippets in your editor!")
        _snippet_messages = []  # Clear the messages

def save():
    """
    Save the current snippet with a unique timestamp so it won't be overwritten.
    This function is available in the interactive shell.
    """
    global _snippet_messages, _current_module, _snippet_counter
    
    if not _snippet_mode:
        print("❌ Snippet mode is not enabled. Run with --snip flag to enable.")
        return
    
    if not _current_module:
        print("❌ No current module set for snippet export.")
        return
    
    if not _snippet_messages:
        print("❌ No snippet available to save.")
        return
    
    try:
        # Get the most recent snippet message and extract the path
        recent_message = _snippet_messages[-1]
        if "practice/" in recent_message:
            # Extract path from message like "📝 Snippet exported: practice/pandas/001.py"
            file_path = recent_message.split(": ")[1]
            
            # Convert to absolute path
            if not file_path.startswith('/'):
                # Relative path - convert to absolute
                if os.path.exists('/workspace'):
                    # We're in Docker
                    abs_path = os.path.join('/workspace', file_path)
                    save_dir = os.path.join('/workspace/practice', _current_module)
                else:
                    # We're on host
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    abs_path = os.path.join(project_root, file_path)
                    save_dir = os.path.join(project_root, 'practice', _current_module)
            else:
                abs_path = file_path
                save_dir = os.path.dirname(abs_path)
            
            # Read the current snippet content
            if os.path.exists(abs_path):
                with open(abs_path, 'r') as f:
                    content = f.read()
                
                # Generate unique filename with timestamp
                import datetime
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                base_name = f"{_current_module}_snippet_{timestamp}.py"
                save_path = os.path.join(save_dir, base_name)
                
                # Write the saved copy
                with open(save_path, 'w') as f:
                    f.write(content)
                
                # Show the saved path (relative format)
                if os.path.exists('/workspace'):
                    # We're in Docker - show relative path
                    relative_save_path = save_path.replace('/workspace/', '')
                else:
                    # We're on host - show relative path from project root
                    try:
                        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        relative_save_path = os.path.relpath(save_path, project_root)
                    except:
                        relative_save_path = save_path
                
                print(f"💾 Snippet saved to: {relative_save_path}")
                print("💡 This copy won't be overwritten by future snippets!")
                
            else:
                print(f"❌ Current snippet file not found: {abs_path}")
        else:
            print("❌ Could not determine snippet file path.")
            
    except Exception as e:
        print(f"❌ Error saving snippet: {e}")

def saved():
    """
    List the most recent saved snippet files (excluding default numbered files).
    Shows only files saved explicitly with save() function.
    """
    if not _current_module:
        print("❌ No module context available.")
        return
    
    try:
        # Determine the practice directory
        if os.path.exists('/workspace'):
            # We're in Docker
            practice_dir = os.path.join('/workspace/practice', _current_module)
        else:
            # We're on host
            practice_dir = os.path.join(os.path.dirname(__file__), '..', 'practice', _current_module)
        
        if not os.path.exists(practice_dir):
            print(f"📂 No saved snippets found for {_current_module} module.")
            print(f"💡 Practice directory: {practice_dir}")
            return
        
        # Get all Python files, excluding default numbered files (001.py, 002.py, etc.)
        files = []
        for filename in os.listdir(practice_dir):
            if filename.endswith('.py'):
                # Exclude files that are just 3 digits + .py (default numbered files)
                if not (len(filename) == 6 and filename[:3].isdigit() and filename == f"{filename[:3]}.py"):
                    filepath = os.path.join(practice_dir, filename)
                    # Get modification time
                    mtime = os.path.getmtime(filepath)
                    files.append((mtime, filename, filepath))
        
        if not files:
            print(f"📂 No saved snippets found for {_current_module} module.")
            print("💡 Use save() in the interactive shell to save a snippet with timestamp.")
            return
        
        # Sort by modification time (newest first)
        files.sort(reverse=True)
        
        print(f"📁 Saved snippets for {_current_module} module:")
        print("=" * 50)
        
        # Show up to 5 most recent files
        for i, (mtime, filename, filepath) in enumerate(files[:5]):
            # Convert timestamp to readable format
            import datetime
            time_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Show relative path for display
            if os.path.exists('/workspace'):
                display_path = filepath.replace('/workspace/', '')
            else:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                display_path = os.path.relpath(filepath, project_root)
            
            if i == 0:
                print(f"🔥 MOST RECENT: {display_path}")
                print(f"   Modified: {time_str}")
            else:
                print(f"{i+1}. {display_path}")
                print(f"   Modified: {time_str}")
        
        if len(files) > 5:
            print(f"... and {len(files) - 5} more files")
        
        print("💡 Open the most recent file in your editor to resume your work!")
        
    except Exception as e:
        print(f"❌ Error listing saved snippets: {e}")

def hf(function_name=None, save=False):
    """
    Get function documentation and usage like tab completion.
    Shows function signature and docstring for Python functions, methods, and objects.
    
    Args:
        function_name (str): Function or method name to get help for.
                           Can be a function name, method name, or object.attribute
        save (bool): If True, save the documentation to a file in addition to displaying it.
    
    Examples:
        hf('len')              # Get help for len() function
        hf('df.combine')       # Get help for DataFrame.combine method
        hf('list.append')      # Get help for list.append method
        hf('pandas.DataFrame') # Get help for pandas DataFrame class
        hf('len', save=True)   # Get help and save to file
    """
    if function_name is None:
        print("❌ Please provide a function name")
        print("💡 Examples: hf('len'), hf('df.combine'), hf('list.append')")
        return
    
    try:
        # Get current frame's local and global variables
        frame = sys._getframe(1)
        local_vars = frame.f_locals
        global_vars = frame.f_globals
        
        # Combine local and global namespaces
        namespace = {**global_vars, **local_vars}
        
        # Try to resolve the function/method
        obj = None
        signature_str = ""
        docstring = ""
        
        # Handle dot notation (e.g., 'df.combine', 'list.append')
        if '.' in function_name:
            parts = function_name.split('.')
            try:
                # Try to resolve the object chain
                obj = namespace.get(parts[0])
                if obj is None:
                    # Try to get from builtins or imported modules
                    import builtins
                    obj = getattr(builtins, parts[0], None)
                    if obj is None:
                        # Try common imports
                        import pandas as pd
                        import numpy as np
                        common_modules = {'pd': pd, 'np': np, 'pandas': pd, 'numpy': np}
                        obj = common_modules.get(parts[0])
                
                # Navigate through the attribute chain
                for part in parts[1:]:
                    if obj is None:
                        break
                    obj = getattr(obj, part, None)
                    
            except (AttributeError, KeyError):
                obj = None
        else:
            # Simple function name
            obj = namespace.get(function_name)
            if obj is None:
                # Try builtins
                import builtins
                obj = getattr(builtins, function_name, None)
        
        if obj is None:
            print(f"❌ Could not find function '{function_name}'")
            print("💡 Make sure the function/object is imported and accessible")
            return
        
        # Get function signature
        try:
            import inspect
            if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isbuiltin(obj):
                try:
                    sig = inspect.signature(obj)
                    signature_str = f"{function_name}{sig}"
                except (ValueError, TypeError):
                    # Some built-in functions don't have signatures available
                    signature_str = f"{function_name}(...)"
            elif inspect.isclass(obj):
                try:
                    sig = inspect.signature(obj.__init__)
                    # Remove 'self' parameter for cleaner display
                    params = list(sig.parameters.values())[1:]  # Skip 'self'
                    new_sig = inspect.Signature(params)
                    signature_str = f"{function_name}{new_sig}"
                except (ValueError, TypeError):
                    signature_str = f"{function_name}(...)"
            else:
                signature_str = f"{function_name}"
        except Exception:
            signature_str = f"{function_name}(...)"
        
        # Get docstring
        try:
            docstring = inspect.getdoc(obj) or ""
        except Exception:
            docstring = ""
        
        # Display the help information
        print("=" * 60)
        print(f"📖 Help for: {function_name}")
        print("=" * 60)
        print()
        
        # Show signature
        if signature_str:
            print("🔧 Signature:")
            print(f"   {signature_str}")
            print()
        
        # Show docstring
        if docstring:
            print("📝 Documentation:")
            # Format the docstring nicely
            lines = docstring.split('\n')
            for line in lines:
                print(f"   {line}")
        else:
            print("� No documentation available")
        
        print()
        print("=" * 60)
        
        # Save to file if requested
        if save:
            save_function_help_to_file(function_name, signature_str, docstring)
        
    except Exception as e:
        print(f"❌ Error getting help for '{function_name}': {e}")
        print("💡 Try: hf('len'), hf('df.combine'), hf('list.append')")

def shortcuts():
    """
    Display all available shortcut functions in the interactive shell.
    """
    print("\n" + "=" * 60)
    print("📋 Available Shortcuts in Interactive Shell")
    print("=" * 60)
    print()
    print("🔍 Help & Information:")
    print("  cs()              - Context-aware help from cheat.sh")
    print("  cs('topic')       - Get help for specific topic (e.g., cs('python/list'))")
    print("  cs('topic', save=True) - Save code examples to practice files")
    print("  cs('topic', full=True) - Save comprehensive help to organized files")
    print("  hf('function')    - Get function documentation & signature (e.g., hf('df.combine'))")
    print("  hf('function', save=True) - Get function docs & save to file")
    print("  cm()              - Show current variables/memory")
    print("  shortcuts()       - Show this help (alias: sc())")
    print()
    print("💾 Snippet Management:")
    print("  save()            - Save current snippet with timestamp")
    print("  saved()           - List recently saved snippets")
    print()
    print("🚪 Exit Options:")
    print("  q                 - Quit interactive shell")
    print("  quit()            - Quit interactive shell")
    print("  exit()            - Quit interactive shell")
    print()
    print("💡 Examples:")
    print("  >>> cs('python/pandas')         # Get pandas help")
    print("  >>> cs('python/list', save=True) # Save list code examples to practice files")
    print("  >>> cs('python/list', full=True) # Save comprehensive list help to file")
    print("  >>> hf('df.combine')             # Get DataFrame.combine documentation")
    print("  >>> hf('len', save=True)         # Get len() function help and save to file")
    print("  >>> cm()                         # Show current variables")
    print("  >>> save()                       # Save current snippet")
    print("=" * 60)
    print()

def sc():
    """
    Alias for shortcuts() - Display all available shortcut functions.
    """
    shortcuts()

if __name__ == "__main__":
    main()


