#!/usr/bin/env python3
"""
Python Learning Modules Package

This package contains individual modules for learning different aspects of Python:
- basic_data_structures: Lists, tuples, sets, dictionaries
- advanced_data_structures: Collections module, dataclasses
- csv_module: CSV file handling
- pandas_module: Data analysis with pandas
- jupyter_module: Jupyter notebook creation and IPython features
- challenges: Programming challenges and algorithmic problem solving
- challenges_2: Advanced programming challenges for production scenarios
- database: Database operations and patterns
"""

# Import all modules
from . import basic_data_structures
from . import advanced_data_structures  
from . import csv_module
from . import pandas_module
from . import jupyter_module
from . import challenges
from . import challenges_2
from . import database

# Define available modules
AVAILABLE_MODULES = {
    'basic': (basic_data_structures.DESCRIPTION, basic_data_structures.FUNCTION),
    'advanced': (advanced_data_structures.DESCRIPTION, advanced_data_structures.FUNCTION),
    'csv_module': (csv_module.DESCRIPTION, csv_module.FUNCTION),
    'pandas': (pandas_module.DESCRIPTION, pandas_module.FUNCTION),
    'jupyter': (jupyter_module.DESCRIPTION, jupyter_module.FUNCTION),
    'challenges': (challenges.DESCRIPTION, challenges.FUNCTION),
    'challenges_2': (challenges_2.DESCRIPTION, challenges_2.FUNCTION),
    'database': (database.DESCRIPTION, database.FUNCTION),
}

def setup_module_functions(set_context_func, check_interactive_func, step_through_func=None, snippet_section_func=None):
    """
    Setup the functions that modules need from the main script.
    
    Args:
        set_context_func: Function to set current context for cs() help
        check_interactive_func: Function to check for interactive breakpoints
        step_through_func: Optional function for step-through execution
        snippet_section_func: Optional function for exporting code snippets
    """
    # Update all modules with the correct functions
    for module in [basic_data_structures, advanced_data_structures, csv_module, pandas_module, jupyter_module, challenges, challenges_2, database]:
        module.set_context = set_context_func
        module.check_interactive_mode = check_interactive_func
        if step_through_func and hasattr(module, 'step_through_function'):
            module.step_through_function = step_through_func
        if snippet_section_func:
            module.snippet_section = snippet_section_func

__all__ = ['AVAILABLE_MODULES', 'setup_module_functions']
