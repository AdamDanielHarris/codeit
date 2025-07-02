#!/usr/bin/env python3
"""
CSV Module - Demonstrates reading and writing CSV files using Python's csv module.
Shows both csv.reader and csv.writer, and drops into interactive mode at key points.
"""

import csv
import os

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

def csv_module(step=False):
    """
    Demonstrates reading and writing CSV files using Python's csv module.
    Shows both csv.reader and csv.writer, and drops into interactive mode at key points.
    If step=True, drops into interactive shell after every line in this block.
    """
    def csv_block():
        set_context('csv')  # Set context for cs() function
        temp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filename = os.path.join(temp_dir, "example.csv")
        rows = [
            ["name", "age", "city"],
            ["Alice", 30, "New York"],
            ["Bob", 25, "London"],
            ["Charlie", 35, "Paris"]
        ]
        
        # Export snippet for initial setup
        snippet_section([
            "import csv",
            "import os",
            "",
            "# Create sample data",
            "rows = [",
            '    ["name", "age", "city"],',
            '    ["Alice", 30, "New York"],',
            '    ["Bob", 25, "London"],',
            '    ["Charlie", 35, "Paris"]',
            "]"
        ], "Setting up CSV data")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        set_context('csv_writer')
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"Wrote CSV file: {filename}")
        
        # Export snippet for CSV writing
        snippet_section([
            "import csv",
            "",
            "# Write data to CSV file",
            'filename = "example.csv"',
            'with open(filename, "w", newline="") as f:',
            "    writer = csv.writer(f)",
            "    writer.writerows(rows)",
            'print(f"Wrote CSV file: {filename}")'
        ], "Writing data to CSV file")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        set_context('csv_reader')
        with open(filename, "r", newline='') as f:
            reader = csv.reader(f)
            print("CSV contents:")
            for row in reader:
                print("  ", row)
        
        # Export snippet for CSV reading
        snippet_section([
            "import csv",
            "",
            "# Read CSV file",
            'filename = "example.csv"',
            'with open(filename, "r", newline="") as f:',
            "    reader = csv.reader(f)",
            '    print("CSV contents:")',
            "    for row in reader:",
            '        print("  ", row)'
        ], "Reading data from CSV file")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        set_context('csv_dictreader')
        with open(filename, "r", newline='') as f:
            reader = csv.DictReader(f)
            print("CSV as dicts:")
            for row in reader:
                print("  ", row)
        
        # Export snippet for DictReader
        snippet_section([
            "import csv",
            "",
            "# Read CSV file as dictionaries",
            'filename = "example.csv"',
            'with open(filename, "r", newline="") as f:',
            "    reader = csv.DictReader(f)",
            '    print("CSV as dicts:")',
            "    for row in reader:",
            '        print("  ", row)'
        ], "Using DictReader for CSV files")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        os.remove(filename)
        print(f"Deleted CSV file: {filename}")

    if step:
        step_through_function(csv_block, globals(), locals())
    else:
        csv_block()

# Module metadata
DESCRIPTION = 'CSV Module Usage'
FUNCTION = csv_module
