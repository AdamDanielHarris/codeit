#!/usr/bin/env python3
"""
Jupyter Interactive Module

Demonstrates patterns for making interactive Jupyter notebooks reproducible by:
- Capturing widget/GUI selections and persisting them
- Creating parameter files for headless execution
- Building notebooks that work both interactively and programmatically
- Using configuration-driven approaches for reproducible workflows
"""

import os
import sys
import json
from pathlib import Path

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

def check_interactive_mode():
    """Placeholder function - will be replaced by main script's version"""
    pass

def step_through_function(func, global_ns=None, local_ns=None):
    """Placeholder function - will be replaced by main script's version"""
    func()

def snippet_section(code_lines, description=None):
    """Placeholder function - will be replaced by main script's version"""
    pass

# Module metadata
DESCRIPTION = "Reproducible Interactive Notebooks - Capture GUI inputs for programmatic execution"
FUNCTION = None  # Will be set below after function definition


def jupyter_interactive_module():
    """
    Demonstrates how to make interactive notebooks reproducible.
    Shows patterns for capturing user inputs and running notebooks headlessly.
    """
    
    set_context('jupyter')
    print("🔄 Reproducible Interactive Notebooks")
    print("=" * 60)
    print("\nThis module demonstrates patterns for making interactive")
    print("notebooks (with widgets/GUI elements) run programmatically.\n")
    
    # =========================================================================
    # 1. The Parameter Store Class
    # =========================================================================
    print("1️⃣ The Parameter Store Pattern")
    print("-" * 60)
    print("Store all interactive selections in a JSON config file.")
    print("The notebook checks for saved parameters before showing widgets.\n")
    
    # Create a working ParameterStore class
    class ParameterStore:
        """Manages parameters for reproducible notebook execution."""
        
        def __init__(self, notebook_name, params_dir='./params'):
            self.params_dir = Path(params_dir)
            self.params_dir.mkdir(exist_ok=True)
            self.params_file = self.params_dir / f'{notebook_name}_params.json'
            self._params = self._load()
        
        def _load(self):
            if self.params_file.exists():
                return json.loads(self.params_file.read_text())
            return {}
        
        def save(self):
            self.params_file.write_text(json.dumps(self._params, indent=2))
            print(f"💾 Saved parameters to {self.params_file}")
        
        def get(self, key, default=None):
            """Get a parameter value."""
            if key in self._params:
                print(f"📁 Using saved value for '{key}': {self._params[key]}")
                return self._params[key]
            return default
        
        def set(self, key, value):
            """Set and persist a parameter value."""
            self._params[key] = value
            self.save()
            return value
        
        def clear(self):
            """Clear all saved parameters."""
            self._params = {}
            if self.params_file.exists():
                self.params_file.unlink()
                print(f"🗑️  Cleared parameters from {self.params_file}")
        
        def show(self):
            """Display all saved parameters."""
            if self._params:
                print("📋 Saved parameters:")
                for k, v in self._params.items():
                    print(f"   {k}: {v}")
            else:
                print("📋 No saved parameters")
        
        def __repr__(self):
            return f"ParameterStore({self.params_file}, params={self._params})"
    
    # Create a demo parameter store
    try:
        script_dir = Path(__file__).parent.parent
    except NameError:
        script_dir = Path.cwd()
    
    params_dir = script_dir / "practice" / "jupyter_interactive"
    params_dir.mkdir(parents=True, exist_ok=True)
    
    # Create instance for user to play with
    store = ParameterStore('demo_notebook', params_dir=str(params_dir))
    
    print("Created: store = ParameterStore('demo_notebook')")
    print(f"Params file: {store.params_file}")
    store.show()
    
    snippet_section([
        "# === ParameterStore - Core pattern for reproducible notebooks ===",
        "import json",
        "from pathlib import Path",
        "",
        "class ParameterStore:",
        "    def __init__(self, notebook_name, params_dir='./params'):",
        "        self.params_dir = Path(params_dir)",
        "        self.params_dir.mkdir(exist_ok=True)",
        "        self.params_file = self.params_dir / f'{notebook_name}_params.json'",
        "        self._params = self._load()",
        "    ",
        "    def _load(self):",
        "        if self.params_file.exists():",
        "            return json.loads(self.params_file.read_text())",
        "        return {}",
        "    ",
        "    def get(self, key, default=None):",
        "        return self._params.get(key, default)",
        "    ",
        "    def set(self, key, value):",
        "        self._params[key] = value",
        "        self.params_file.write_text(json.dumps(self._params, indent=2))",
        "",
        "# Usage:",
        "store = ParameterStore('my_notebook')",
        "store.set('dataset', 'sales_2024.csv')",
        "dataset = store.get('dataset', default='default.csv')",
    ], "ParameterStore class for saving interactive selections")
    
    print("\n💡 Try these commands:")
    print("   store.set('dataset', 'sales_2024.csv')  # Save a parameter")
    print("   store.get('dataset')                     # Retrieve it")
    print("   store.show()                             # See all saved params")
    print("   store.clear()                            # Reset all params")
    
    check_interactive_mode()
    
    # =========================================================================
    # 2. Interactive Mode Detection
    # =========================================================================
    print("\n2️⃣ Interactive Mode Detection")
    print("-" * 60)
    print("Detect if running interactively vs programmatically.\n")
    
    def is_jupyter():
        """Check if running in Jupyter notebook."""
        try:
            from IPython import get_ipython
            shell = get_ipython()
            if shell is None:
                return False
            return 'ZMQInteractiveShell' in str(type(shell))
        except:
            return False
    
    def is_ipython():
        """Check if running in IPython (terminal or notebook)."""
        try:
            from IPython import get_ipython
            return get_ipython() is not None
        except:
            return False
    
    def get_execution_context():
        """Determine how the code is being executed."""
        # Check for CI/CD
        if any(var in os.environ for var in ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI']):
            return 'ci_cd'
        # Check for papermill
        if 'PAPERMILL_OUTPUT_PATH' in os.environ:
            return 'papermill'
        # Check for Jupyter
        if is_jupyter():
            return 'jupyter'
        # Check for IPython
        if is_ipython():
            return 'ipython'
        return 'script'
    
    # Detect current context
    context = get_execution_context()
    is_interactive = context in ['jupyter', 'ipython']
    
    print(f"Current execution context: {context}")
    print(f"Is interactive: {is_interactive}")
    print(f"is_jupyter(): {is_jupyter()}")
    print(f"is_ipython(): {is_ipython()}")
    
    snippet_section([
        "# === Detect execution context ===",
        "import os",
        "",
        "def is_jupyter():",
        "    '''Check if running in Jupyter notebook.'''",
        "    try:",
        "        from IPython import get_ipython",
        "        shell = get_ipython()",
        "        return shell is not None and 'ZMQInteractiveShell' in str(type(shell))",
        "    except:",
        "        return False",
        "",
        "def get_execution_context():",
        "    if os.environ.get('CI'):",
        "        return 'ci_cd'",
        "    if os.environ.get('PAPERMILL_OUTPUT_PATH'):",
        "        return 'papermill'",
        "    if is_jupyter():",
        "        return 'jupyter'",
        "    return 'script'",
        "",
        "# Use it to decide behavior:",
        "if get_execution_context() == 'jupyter':",
        "    # Show widget",
        "    pass",
        "else:",
        "    # Use saved/default value",
        "    pass",
    ], "Execution context detection")
    
    print("\n💡 Try these:")
    print("   is_jupyter()            # Are we in Jupyter?")
    print("   is_ipython()            # Are we in IPython?")
    print("   get_execution_context() # Full context detection")
    
    check_interactive_mode()
    
    # =========================================================================
    # 3. The get_param Pattern with Fallbacks
    # =========================================================================
    print("\n3️⃣ The get_param Pattern with Fallbacks")
    print("-" * 60)
    print("Chain of fallbacks: env var → saved param → default\n")
    
    def get_param(store, name, default=None, env_prefix='NB_PARAM'):
        """
        Get parameter with fallback chain:
        1. Environment variable (for CI/CD)
        2. Saved parameter (from previous interactive session)
        3. Default value
        """
        # Check environment variable first
        env_var = f"{env_prefix}_{name.upper()}"
        env_val = os.environ.get(env_var)
        if env_val is not None:
            print(f"🌍 Using env var {env_var}: {env_val}")
            return env_val
        
        # Check saved parameters
        saved = store.get(name)
        if saved is not None:
            return saved
        
        # Use default
        if default is not None:
            print(f"📝 Using default for '{name}': {default}")
        return default
    
    # Demo the pattern
    print("Demo: get_param with fallback chain")
    print("-" * 40)
    
    # Set some example params
    store.set('threshold', 100)
    
    # Get params using fallback chain
    dataset = get_param(store, 'dataset', default='sample.csv')
    threshold = get_param(store, 'threshold', default=50)
    missing = get_param(store, 'missing_param', default='fallback_value')
    
    print(f"\nResults:")
    print(f"   dataset = '{dataset}'")
    print(f"   threshold = {threshold}")
    print(f"   missing = '{missing}'")
    
    snippet_section([
        "# === get_param pattern with fallback chain ===",
        "import os",
        "",
        "def get_param(store, name, default=None, env_prefix='NB_PARAM'):",
        "    '''",
        "    Fallback chain: env var → saved param → default",
        "    '''",
        "    # 1. Check environment variable (for CI/CD)",
        "    env_var = f'{env_prefix}_{name.upper()}'",
        "    env_val = os.environ.get(env_var)",
        "    if env_val is not None:",
        "        return env_val",
        "    ",
        "    # 2. Check saved parameters",
        "    saved = store.get(name)",
        "    if saved is not None:",
        "        return saved",
        "    ",
        "    # 3. Use default",
        "    return default",
        "",
        "# Usage:",
        "dataset = get_param(store, 'dataset', default='data.csv')",
        "threshold = get_param(store, 'threshold', default=100)",
        "",
        "# For CI/CD, set env vars:",
        "# NB_PARAM_DATASET=prod_data.csv python run_notebook.py",
    ], "get_param pattern with environment variable fallback")
    
    print("\n💡 Try these:")
    print("   get_param(store, 'dataset', default='test.csv')")
    print("   store.set('dataset', 'my_data.csv')")
    print("   get_param(store, 'dataset', default='test.csv')  # Now uses saved")
    print("   os.environ['NB_PARAM_DATASET'] = 'env_data.csv'")
    print("   get_param(store, 'dataset', default='test.csv')  # Now uses env var")
    
    check_interactive_mode()
    
    # =========================================================================
    # 4. Widget Simulation Pattern
    # =========================================================================
    print("\n4️⃣ Widget-or-Value Pattern")
    print("-" * 60)
    print("In notebooks: show widget. In scripts: use saved/default value.\n")
    
    class SmartParam:
        """
        A parameter that shows a widget in Jupyter or uses saved/default value otherwise.
        Automatically saves selections for later headless execution.
        """
        def __init__(self, store, name, options=None, default=None, description=''):
            self.store = store
            self.name = name
            self.options = options
            self.default = default
            self.description = description
            self._value = None
            self._resolve()
        
        def _resolve(self):
            # Check environment variable
            env_val = os.environ.get(f'NB_PARAM_{self.name.upper()}')
            if env_val is not None:
                self._value = env_val
                print(f"🌍 {self.name}: using env var = {env_val}")
                return
            
            # Check saved parameter
            saved = self.store._params.get(self.name)
            if saved is not None:
                self._value = saved
                print(f"📁 {self.name}: using saved = {saved}")
                return
            
            # In Jupyter, would show widget here
            if is_jupyter():
                print(f"🎛️  {self.name}: would show widget (options={self.options})")
                # In real notebook: create and display widget
                self._value = self.default
            else:
                self._value = self.default
                print(f"📝 {self.name}: using default = {self.default}")
        
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            self._value = new_value
            self.store.set(self.name, new_value)
        
        def __repr__(self):
            return f"SmartParam({self.name}={self._value})"
    
    # Demo SmartParam
    print("Demo: SmartParam class")
    print("-" * 40)
    
    dataset_param = SmartParam(
        store, 'analysis_dataset',
        options=['sales.csv', 'customers.csv', 'products.csv'],
        default='sales.csv',
        description='Select dataset'
    )
    
    filter_param = SmartParam(
        store, 'min_value',
        default=100,
        description='Minimum filter value'
    )
    
    print(f"\ndataset_param.value = '{dataset_param.value}'")
    print(f"filter_param.value = {filter_param.value}")
    
    snippet_section([
        "# === SmartParam - Widget or value based on context ===",
        "",
        "class SmartParam:",
        "    '''Shows widget in Jupyter, uses saved/default in scripts.'''",
        "    ",
        "    def __init__(self, store, name, options=None, default=None):",
        "        self.store = store",
        "        self.name = name",
        "        self.options = options",
        "        self._value = self._resolve(default)",
        "    ",
        "    def _resolve(self, default):",
        "        # Priority: env var > saved > widget/default",
        "        env_val = os.environ.get(f'NB_PARAM_{self.name.upper()}')",
        "        if env_val:",
        "            return env_val",
        "        saved = self.store.get(self.name)",
        "        if saved:",
        "            return saved",
        "        if is_jupyter() and self.options:",
        "            # Would show dropdown widget here",
        "            pass",
        "        return default",
        "    ",
        "    @property",
        "    def value(self):",
        "        return self._value",
        "    ",
        "    @value.setter", 
        "    def value(self, v):",
        "        self._value = v",
        "        self.store.set(self.name, v)",
        "",
        "# Usage:",
        "dataset = SmartParam(store, 'dataset', ",
        "                     options=['a.csv', 'b.csv'], ",
        "                     default='a.csv')",
        "print(dataset.value)",
        "dataset.value = 'b.csv'  # Auto-saves for next run",
    ], "SmartParam class for context-aware parameters")
    
    print("\n💡 Try these:")
    print("   dataset_param.value              # Get current value")
    print("   dataset_param.value = 'new.csv'  # Set and auto-save")
    print("   store.show()                     # See it was saved")
    
    check_interactive_mode()
    
    # =========================================================================
    # 5. Complete Workflow Example
    # =========================================================================
    print("\n5️⃣ Complete Workflow Example")
    print("-" * 60)
    print("Putting it all together for a reproducible analysis.\n")
    
    # Simulate a complete workflow
    class ReproducibleWorkflow:
        """A complete reproducible notebook workflow."""
        
        def __init__(self, name):
            self.name = name
            self.store = ParameterStore(name, params_dir=str(params_dir))
            self.results = {}
        
        def configure(self, **defaults):
            """Set up parameters with defaults."""
            self.params = {}
            for key, default in defaults.items():
                self.params[key] = get_param(self.store, key, default=default)
            return self.params
        
        def run_analysis(self, data):
            """Run analysis with configured parameters."""
            # Use the configured parameters
            threshold = self.params.get('threshold', 0)
            filtered = [x for x in data if x >= threshold]
            
            self.results = {
                'input_count': len(data),
                'filtered_count': len(filtered),
                'threshold_used': threshold,
                'filtered_data': filtered
            }
            return self.results
        
        def save_config(self):
            """Save current configuration for reproducibility."""
            for key, value in self.params.items():
                self.store.set(key, value)
            print(f"✅ Configuration saved for '{self.name}'")
        
        def show_status(self):
            """Display workflow status."""
            print(f"\n📊 Workflow: {self.name}")
            print(f"   Parameters: {self.params}")
            print(f"   Results: {self.results}")
            self.store.show()
    
    # Create and run workflow
    workflow = ReproducibleWorkflow('sales_analysis')
    
    # Configure with defaults (will use saved values if available)
    config = workflow.configure(
        threshold=50,
        output_format='csv',
        include_charts=True
    )
    print(f"Configuration: {config}")
    
    # Run analysis
    sample_data = [10, 25, 50, 75, 100, 150, 200]
    results = workflow.run_analysis(sample_data)
    print(f"Results: {results}")
    
    snippet_section([
        "# === Complete reproducible workflow pattern ===",
        "",
        "class ReproducibleWorkflow:",
        "    def __init__(self, name):",
        "        self.name = name",
        "        self.store = ParameterStore(name)",
        "    ",
        "    def configure(self, **defaults):",
        "        '''Load params: saved values override defaults.'''",
        "        self.params = {}",
        "        for key, default in defaults.items():",
        "            self.params[key] = get_param(self.store, key, default)",
        "        return self.params",
        "    ",
        "    def run_analysis(self, data):",
        "        # Analysis uses self.params",
        "        threshold = self.params['threshold']",
        "        return [x for x in data if x >= threshold]",
        "    ",
        "    def save_config(self):",
        "        '''Save current config for next run.'''",
        "        for k, v in self.params.items():",
        "            self.store.set(k, v)",
        "",
        "# Usage:",
        "wf = ReproducibleWorkflow('my_analysis')",
        "wf.configure(threshold=100, output='csv')",
        "results = wf.run_analysis(data)",
        "wf.save_config()  # Next run will use same params",
    ], "Complete reproducible workflow class")
    
    print("\n💡 Try these:")
    print("   workflow.params['threshold'] = 100")
    print("   workflow.run_analysis([10, 50, 100, 150, 200])")
    print("   workflow.save_config()  # Save for next run")
    print("   workflow.show_status()")
    
    check_interactive_mode()
    
    # =========================================================================
    # 6. Papermill Integration
    # =========================================================================
    print("\n6️⃣ Papermill Integration")
    print("-" * 60)
    print("Use papermill to run notebooks with injected parameters.\n")
    
    # Create a sample papermill command
    papermill_example = """
# Install: pip install papermill

# Run notebook with parameters:
papermill input.ipynb output.ipynb \\
    -p dataset 'sales_2024.csv' \\
    -p threshold 100 \\
    -p output_format 'excel'

# From Python:
import papermill as pm
pm.execute_notebook(
    'template.ipynb',
    'output/run_001.ipynb',
    parameters={
        'dataset': 'sales_2024.csv',
        'threshold': 100
    }
)
"""
    
    print("Papermill command-line example:")
    print(papermill_example)
    
    # Show how to tag parameters cell
    params_cell_example = """
# In your notebook, create a cell with these defaults
# and tag it as 'parameters' (in Jupyter: View > Cell Toolbar > Tags)

# --- Parameters Cell (tag: 'parameters') ---
dataset = 'default.csv'
threshold = 50
output_format = 'csv'
"""
    
    print("Parameters cell in notebook:")
    print(params_cell_example)
    
    snippet_section([
        "# === Papermill - Run notebooks with parameters ===",
        "# pip install papermill",
        "",
        "import papermill as pm",
        "",
        "# Execute notebook with injected parameters",
        "pm.execute_notebook(",
        "    'analysis_template.ipynb',   # Input notebook",
        "    'output/analysis_001.ipynb', # Output with results",
        "    parameters={",
        "        'dataset': 'sales_2024.csv',",
        "        'threshold': 100,",
        "        'output_format': 'excel'",
        "    }",
        ")",
        "",
        "# In the template notebook, tag a cell as 'parameters':",
        "# (Jupyter: View > Cell Toolbar > Tags > add 'parameters')",
        "",
        "# --- Parameters cell (tag it!) ---",
        "dataset = 'default.csv'  # Will be overwritten by papermill",
        "threshold = 50",
    ], "Papermill for parameterized notebook execution")
    
    check_interactive_mode()
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("\n📚 Summary: Key Patterns for Reproducible Notebooks")
    print("=" * 60)
    print("""
Objects available to explore:
  store      - ParameterStore instance for saving/loading params
  workflow   - ReproducibleWorkflow example
  
Key classes:
  ParameterStore  - Save/load parameters to JSON
  SmartParam      - Context-aware parameter (widget vs value)
  
Key functions:
  is_jupyter()           - Check if in Jupyter
  get_execution_context() - Full context detection
  get_param()            - Parameter with fallback chain

Patterns:
  1. Save all user selections to params file
  2. On next run, load saved values instead of showing widgets
  3. For CI/CD, use environment variables (NB_PARAM_*)
  4. For batch runs, use papermill with -p flags
""")
    
    print("💡 Experiment with the objects above!")
    check_interactive_mode()


# Set the FUNCTION after defining it
FUNCTION = jupyter_interactive_module
