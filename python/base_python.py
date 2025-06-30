#!/usr/bin/env python3

import argparse
import code
import sys
try:
    import readline
    import rlcompleter
except ImportError:
    readline = None

# Let's start off with the basic data strucrtures in Python.

# Global variable to track current context for cs() function
_current_context = 'basics'

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

AVAILABLE_FUNCTIONS = {}

def register_function(key, description):
    """Decorator to register functions for selective execution."""
    def decorator(func):
        AVAILABLE_FUNCTIONS[key] = (description, func)
        return func
    return decorator

@register_function('basic', 'Basic Data Structures')
def basic_data_structures():
    """
    Demonstrates basic data structures in Python.
    Shows how to add and remove items, or explains why not possible if immutable.
    """
    # Lists
    list1 = [1, 2, 3, 4, 5]
    set_context('list')  # Set context for cs() function
    print("List:", list1)
    list1.append(6)  # Add item
    print("After append:", list1)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    list1.remove(3)  # Remove item
    print("After remove:", list1)

    # Tuples
    tuple1 = (1, 2, 3)
    set_context('tuple')  # Set context for cs() function
    print("Tuple:", tuple1)
    # Tuples are immutable, so you cannot add or remove items
    print("Cannot add or remove items from a tuple (immutable)")

    # Check for interactive mode breakpoint
    check_interactive_mode()

    # Sets
    set1 = {1, 2, 3, 4}
    set_context('set')  # Set context for cs() function
    print("Set:", set1)
    set1.add(5)  # Add item
    print("After add:", set1)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    set1.discard(2)  # Remove item
    print("After discard:", set1)

    # Dictionaries
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    set_context('dict')  # Set context for cs() function
    print("Dictionary:", dict1)
    dict1['d'] = 4  # Add item
    print("After adding key 'd':", dict1)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    del dict1['b']  # Remove item
    print("After deleting key 'b':", dict1)

@register_function('advanced', 'Advanced Data Structures')
def advanced_data_structures():
    """
    Demonstrates advanced built-in data structures in Python.
    Shows collections module structures and their useful methods.
    """
    from collections import defaultdict, Counter, OrderedDict, deque, namedtuple, ChainMap
    from dataclasses import dataclass
    
    # defaultdict - Dictionary with default values for missing keys
    dd1 = defaultdict(list)
    set_context('defaultdict')  # Set context for cs() function
    dd1['fruits'].append('apple')
    dd1['fruits'].append('banana')
    dd1['vegetables'].append('carrot')
    print("defaultdict (list):", dict(dd1))
    print("Accessing non-existent key 'grains':", dd1['grains'])  # Creates empty list
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # Counter - Dictionary for counting hashable objects
    counter1 = Counter(['a', 'b', 'c', 'a', 'b', 'a'])
    set_context('counter')  # Set context for cs() function
    print("Counter:", counter1)
    counter1.update(['a', 'd', 'd'])  # Add more counts
    print("After update:", counter1)
    print("Most common (2):", counter1.most_common(2))
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # OrderedDict - Dictionary that maintains insertion order
    od1 = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
    print("OrderedDict:", od1)
    od1.move_to_end('first')  # Move key to end
    print("After move_to_end('first'):", od1)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # deque - Double-ended queue for efficient appends/pops
    deque1 = deque([1, 2, 3, 4, 5])
    set_context('deque')  # Set context for cs() function
    print("deque:", deque1)
    deque1.appendleft(0)  # Add to left
    deque1.append(6)      # Add to right
    print("After appendleft(0) and append(6):", deque1)
    deque1.rotate(2)      # Rotate right by 2
    print("After rotate(2):", deque1)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # namedtuple - Tuple subclass with named fields
    Person = namedtuple('Person', ['name', 'age', 'city'])
    person1 = Person('Alice', 30, 'New York')
    print("namedtuple Person:", person1)
    print("Access by name:", person1.name, person1.age)
    person2 = person1._replace(age=31)  # Create new instance with changed field
    print("After _replace(age=31):", person2)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # ChainMap - Dictionary-like class for creating a single view of multiple mappings
    dict_a = {'a': 1, 'b': 2}
    dict_b = {'b': 3, 'c': 4}
    chain1 = ChainMap(dict_a, dict_b)
    print("ChainMap:", chain1)
    print("Value of 'b' (from first dict):", chain1['b'])
    chain1['d'] = 5  # Adds to first dict
    print("After adding 'd': dict_a =", dict_a)
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # frozenset - Immutable version of set
    frozenset1 = frozenset([1, 2, 3, 4, 5])
    print("frozenset:", frozenset1)
    frozenset2 = frozenset([4, 5, 6, 7])
    print("Union with another frozenset:", frozenset1.union(frozenset2))
    print("Intersection:", frozenset1.intersection(frozenset2))
    # frozensets are immutable, so no add/remove methods
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # dataclass - Classes for storing data with automatic method generation
    @dataclass
    class Student:
        name: str
        grade: int
        subjects: list = None
        
        def __post_init__(self):
            if self.subjects is None:
                self.subjects = []
    
    student1 = Student('Bob', 85, ['Math', 'Science'])
    print("dataclass Student:", student1)
    student1.subjects.append('History')
    print("After adding subject:", student1)

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
    print("-" * 60)
    
    if relevant_vars:
        print("Current variables:")
        for name, value in relevant_vars.items():
            print(f"  {name} = {repr(value)}")
    else:
        print("No local variables defined yet")
    
    print("="*60 + "\n")
    
    # Add convenient exit shortcuts to the local namespace
    local_vars_with_shortcuts = local_vars.copy()
    local_vars_with_shortcuts.update({
        'q': exit,
        'quit': exit,
        'exit': exit,
        'cs': cs,  # Add cheat.sh function
        'cm': cm,  # Add current memory function
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
    """
    # Get current frame's local variables
    frame = sys._getframe(1)
    local_vars = {**frame.f_locals, **frame.f_globals}
    
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

# Main function
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Python basics demonstration with interactive mode')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Enable interactive mode - drops into Python shell at breakpoints')
    parser.add_argument('--doc', action='store_true',
                       help='Always show docstrings on first tab press (default: show on second tab)')
    parser.add_argument('--functions', nargs='*', 
                       help='Specify which functions to run (e.g., basic advanced). If not specified, runs all.')
    parser.add_argument('--list', action='store_true',
                       help='List available functions and exit')
    parser.add_argument('--bash-completion', action='store_true',
                       help='Generate bash completion script and exit')
    args = parser.parse_args()
    
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
    
    # Set interactive mode flag
    check_interactive_mode.interactive_mode = args.interactive
    # Set always show docs flag
    check_interactive_mode.always_show_docs = args.doc
    
    if args.interactive:
        print("Interactive mode enabled - you'll be dropped into a Python shell at breakpoints")
        if args.doc:
            print("Documentation mode enabled - docstrings will show on first tab press")
    
    # Determine which functions to run
    if args.functions is not None:
        # Specific functions requested
        if not args.functions:
            # --functions was specified but no functions listed, show available and exit
            print("Available functions:")
            for key, (description, _) in AVAILABLE_FUNCTIONS.items():
                print(f"  {key}: {description}")
            print("\nUsage: --functions basic advanced")
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
            func()
        else:
            print(f"Error: Unknown function '{func_key}'. Use --list to see available functions.")
            return

def cs(topic=None):
    """
    Cheat.sh integration for the interactive shell.
    Look up help on programming topics using cheat.sh.
    
    Args:
        topic (str, optional): Topic to look up. If None, tries to determine from current context.
    
    Examples:
        cs()                    # Context-aware help
        cs("python/list")       # Python list help
        cs("python/dict/pop")   # Dictionary pop method
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
        url = f"https://cheat.sh/{topic}"
        
        # Make request with user agent to avoid rate limiting
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'curl/7.68.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            
            # Clean up content - remove excessive blank lines
            lines = content.split('\n')
            cleaned_lines = []
            prev_blank = False
            
            for line in lines:
                is_blank = line.strip() == ''
                if not (is_blank and prev_blank):  # Skip consecutive blank lines
                    cleaned_lines.append(line)
                prev_blank = is_blank
            
            content = '\n'.join(cleaned_lines[:50])  # Limit to first 50 lines
            
            print("=" * 60)
            print(content)
            print("=" * 60)
            print(f"💡 More help: curl cheat.sh/{topic}")
            
    except Exception as e:
        print(f"❌ Error fetching help: {e}")
        print(f"💡 Try: curl cheat.sh/{topic}")
        print("💡 Common topics: python/list, python/dict, python/collections, python/dataclass")

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

if __name__ == "__main__":
    main()









