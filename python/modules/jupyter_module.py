#!/usr/bin/env python3
"""
Jupyter Notebook Module

Demonstrates how to work with Jupyter notebooks programmatically and showcases
common Jupyter/IPython features including magic commands, rich display, and
interactive widgets.
"""

import os
import sys

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

def jupyter_module():
    """
    Demonstrates Jupyter notebook concepts and IPython features.
    Shows programmatic notebook creation, magic commands, and rich display.
    """
    def jupyter_block():
        # Check if required packages are available
        try:
            import nbformat
            from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
            import jupyter_client
        except ImportError as e:
            print(f"❌ Error importing Jupyter packages: {e}")
            print("📦 Jupyter packages are required. Install with:")
            print("   pip install jupyter nbformat jupyter_client")
            print("   or run: python python/learn_python.py --setup-env")
            return
        
        try:
            import IPython
            from IPython.display import display, HTML, Markdown, Image
            from IPython import get_ipython
        except ImportError:
            # IPython not available, continue with limited functionality
            IPython = None
            display = None
            get_ipython = None
        
        set_context('jupyter')
        print("📓 Jupyter Notebook Demonstration")
        print("=" * 50)
        
        # 1. Creating notebooks programmatically
        print("\n1️⃣ Creating Notebooks Programmatically")
        print("-" * 50)
        
        nb = new_notebook()
        
        # Add markdown cell
        nb.cells.append(new_markdown_cell("# Data Analysis Example\n\nThis notebook demonstrates basic data analysis."))
        
        # Add code cell
        nb.cells.append(new_code_cell("import pandas as pd\nimport numpy as np\n\ndata = {'x': [1, 2, 3], 'y': [4, 5, 6]}\ndf = pd.DataFrame(data)\nprint(df)"))
        
        print("✅ Created notebook with 2 cells")
        print(f"   - Cells: {len(nb.cells)}")
        print(f"   - Notebook format: {nb.nbformat}.{nb.nbformat_minor}")
        
        snippet_section([
            "# Create a new Jupyter notebook programmatically",
            "from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell",
            "",
            "nb = new_notebook()",
            "",
            "# Add markdown cell",
            "nb.cells.append(new_markdown_cell('# Data Analysis Example'))",
            "",
            "# Add code cell",
            "code = '''import pandas as pd",
            "df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})",
            "print(df)'''",
            "nb.cells.append(new_code_cell(code))",
        ], "Creating notebooks programmatically")
        
        check_interactive_mode()
        
        # 2. Saving and loading notebooks
        print("\n2️⃣ Saving and Loading Notebooks")
        print("-" * 50)
        
        # Determine the correct path for saving
        if os.path.exists('/workspace'):
            # We're in Docker
            practice_dir = '/workspace/practice/jupyter'
        else:
            # We're on host
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            practice_dir = os.path.join(project_root, 'practice', 'jupyter')
        
        os.makedirs(practice_dir, exist_ok=True)
        notebook_path = os.path.join(practice_dir, 'example.ipynb')
        
        # Save the notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        # Convert path for display
        display_path = notebook_path.replace('/workspace/', '') if '/workspace/' in notebook_path else notebook_path
        print(f"✅ Saved notebook to: {display_path}")
        
        # Load it back
        with open(notebook_path, 'r', encoding='utf-8') as f:
            loaded_nb = nbformat.read(f, as_version=4)
        
        print(f"✅ Loaded notebook with {len(loaded_nb.cells)} cells")
        
        snippet_section([
            "# Save a notebook to file",
            "import nbformat",
            "",
            "with open('example.ipynb', 'w', encoding='utf-8') as f:",
            "    nbformat.write(nb, f)",
            "",
            "# Load a notebook from file",
            "with open('example.ipynb', 'r', encoding='utf-8') as f:",
            "    loaded_nb = nbformat.read(f, as_version=4)",
            "",
            "print(f'Loaded {len(loaded_nb.cells)} cells')",
        ], "Saving and loading notebooks")
        
        check_interactive_mode()
        
        # 3. IPython features (if available)
        print("\n3️⃣ IPython Features")
        print("-" * 50)
        
        if get_ipython is not None:
            ipython = get_ipython()
            print("✅ Running in IPython environment")
            print(f"   - IPython version: {IPython.__version__}")
            
            # Show magic commands
            print("\n📚 Available Magic Commands:")
            print("   %timeit - Time execution of single statement")
            print("   %%timeit - Time execution of cell")
            print("   %run - Run Python script")
            print("   %load - Load code from file or URL")
            print("   %pwd - Print working directory")
            print("   %ls - List directory contents")
            print("   %who - List variables")
            print("   %whos - List variables with details")
        else:
            print("ℹ️  Not running in IPython environment")
            print("   Magic commands are only available in IPython/Jupyter")
            print("   Run this in a Jupyter notebook to try them!")
        
        snippet_section([
            "# IPython magic commands (use in Jupyter notebooks)",
            "",
            "# Time a single statement",
            "# %timeit sum(range(100))",
            "",
            "# Time a cell",
            "# %%timeit",
            "# total = 0",
            "# for i in range(100):",
            "#     total += i",
            "",
            "# List variables",
            "# %who",
            "# %whos  # With details",
            "",
            "# Run a Python script",
            "# %run my_script.py",
        ], "IPython magic commands")
        
        check_interactive_mode()
        
        # 4. Working with notebook cells
        print("\n4️⃣ Working with Notebook Cells")
        print("-" * 50)
        
        # Iterate through cells
        for i, cell in enumerate(loaded_nb.cells, 1):
            print(f"\nCell {i}: {cell.cell_type}")
            if cell.cell_type == 'code':
                print(f"   Source: {cell.source[:50]}...")
            elif cell.cell_type == 'markdown':
                print(f"   Content: {cell.source[:50]}...")
        
        snippet_section([
            "# Iterate through notebook cells",
            "for i, cell in enumerate(nb.cells, 1):",
            "    print(f'Cell {i}: {cell.cell_type}')",
            "    if cell.cell_type == 'code':",
            "        print(f'   Code: {cell.source[:50]}...')",
            "    elif cell.cell_type == 'markdown':",
            "        print(f'   Content: {cell.source[:50]}...')",
        ], "Iterating through cells")
        
        check_interactive_mode()
        
        # 5. Rich display features
        print("\n5️⃣ Rich Display in Jupyter")
        print("-" * 50)
        
        if display is not None:
            print("✅ IPython.display available")
            print("\n📊 You can display rich content:")
            print("   - HTML: display(HTML('<h1>Title</h1>'))")
            print("   - Markdown: display(Markdown('# Heading'))")
            print("   - Images: display(Image('path/to/image.png'))")
            print("   - DataFrames (rendered as HTML tables)")
            print("   - Plots (matplotlib, seaborn, plotly)")
        else:
            print("ℹ️  IPython.display not available")
            print("   Install IPython to use rich display features")
        
        snippet_section([
            "# Rich display in Jupyter notebooks",
            "from IPython.display import display, HTML, Markdown",
            "",
            "# Display HTML",
            "display(HTML('<h2 style=\"color:blue\">Styled Heading</h2>'))",
            "",
            "# Display Markdown",
            "display(Markdown('# This is **bold** and *italic*'))",
            "",
            "# Display pandas DataFrame (auto-formatted as table)",
            "import pandas as pd",
            "df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})",
            "display(df)  # Better than print(df) in notebooks",
        ], "Rich display in Jupyter")
        
        check_interactive_mode()
        
        # 6. Practical notebook creation example
        print("\n6️⃣ Creating a Complete Analysis Notebook")
        print("-" * 50)
        
        # Create a more complete example notebook
        analysis_nb = new_notebook()
        
        # Title
        analysis_nb.cells.append(new_markdown_cell(
            "# Data Analysis Report\n\n"
            "This notebook demonstrates a complete data analysis workflow.\n\n"
            "## Setup"
        ))
        
        # Imports
        analysis_nb.cells.append(new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n\n"
            "# Set style\n"
            "sns.set_style('whitegrid')\n"
            "plt.rcParams['figure.figsize'] = (10, 6)"
        ))
        
        # Load data
        analysis_nb.cells.append(new_markdown_cell("## Load Data"))
        analysis_nb.cells.append(new_code_cell(
            "# Create sample dataset\n"
            "np.random.seed(42)\n"
            "data = {\n"
            "    'date': pd.date_range('2024-01-01', periods=100),\n"
            "    'value': np.random.randn(100).cumsum(),\n"
            "    'category': np.random.choice(['A', 'B', 'C'], 100)\n"
            "}\n"
            "df = pd.DataFrame(data)\n"
            "df.head()"
        ))
        
        # Analysis
        analysis_nb.cells.append(new_markdown_cell("## Analysis"))
        analysis_nb.cells.append(new_code_cell(
            "# Summary statistics\n"
            "print('Summary Statistics:')\n"
            "print(df.describe())\n\n"
            "print('\\nCategory counts:')\n"
            "print(df['category'].value_counts())"
        ))
        
        # Visualization
        analysis_nb.cells.append(new_markdown_cell("## Visualization"))
        analysis_nb.cells.append(new_code_cell(
            "# Plot time series\n"
            "plt.figure(figsize=(12, 6))\n"
            "plt.plot(df['date'], df['value'])\n"
            "plt.title('Value Over Time')\n"
            "plt.xlabel('Date')\n"
            "plt.ylabel('Value')\n"
            "plt.xticks(rotation=45)\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ))
        
        # Save the complete notebook
        complete_path = os.path.join(practice_dir, 'complete_analysis.ipynb')
        with open(complete_path, 'w', encoding='utf-8') as f:
            nbformat.write(analysis_nb, f)
        
        display_complete = complete_path.replace('/workspace/', '') if '/workspace/' in complete_path else complete_path
        print(f"✅ Created complete analysis notebook")
        print(f"   Saved to: {display_complete}")
        print(f"   Cells: {len(analysis_nb.cells)}")
        print(f"\n💡 Open this notebook in Jupyter to run it:")
        print(f"   jupyter notebook {display_complete}")
        
        snippet_section([
            "# Create a complete analysis notebook",
            "from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell",
            "import nbformat",
            "",
            "nb = new_notebook()",
            "",
            "# Add title",
            "nb.cells.append(new_markdown_cell('# Data Analysis Report'))",
            "",
            "# Add imports",
            "nb.cells.append(new_code_cell(",
            "    'import pandas as pd\\n'",
            "    'import numpy as np\\n'",
            "    'import matplotlib.pyplot as plt'",
            "))",
            "",
            "# Add analysis section",
            "nb.cells.append(new_markdown_cell('## Analysis'))",
            "nb.cells.append(new_code_cell('df.describe()'))",
            "",
            "# Save notebook",
            "with open('analysis.ipynb', 'w') as f:",
            "    nbformat.write(nb, f)",
        ], "Creating complete analysis notebooks")
        
        check_interactive_mode()
        
        # Summary
        print("\n" + "=" * 50)
        print("✅ Jupyter Module Complete!")
        print("\n📚 Key Takeaways:")
        print("   1. Create notebooks programmatically with nbformat")
        print("   2. Add code and markdown cells")
        print("   3. Save/load notebooks as JSON files")
        print("   4. Use IPython magic commands in notebooks")
        print("   5. Display rich content (HTML, Markdown, plots)")
        print("\n💡 Next Steps:")
        print(f"   - Open practice notebooks in Jupyter Lab or Notebook")
        print(f"   - Try: jupyter lab {practice_dir}")
        print(f"   - Experiment with magic commands")
        print(f"   - Create your own analysis notebooks")
    
    # Run the jupyter block
    if hasattr(check_interactive_mode, 'step_mode') and check_interactive_mode.step_mode:
        # If step mode is enabled, step through the function
        step_through_function(jupyter_block)
    else:
        # Normal execution
        jupyter_block()

# Module metadata
DESCRIPTION = 'Jupyter Notebooks'
FUNCTION = jupyter_module
