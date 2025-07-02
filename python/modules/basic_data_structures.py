#!/usr/bin/env python3
"""
Basic Data Structures Module

Demonstrates basic data structures in Python including lists, tuples, sets, and dictionaries.
Shows how to add and remove items, or explains why not possible if immutable.
"""

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

def check_interactive_mode():
    """Placeholder function - will be replaced by main script's version"""
    pass

def snippet_section(code_lines, description=None):
    """Placeholder function - will be replaced by main script's version"""
    pass

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
    
    # Export list operations snippet
    snippet_section([
        "# Working with Lists",
        "list1 = [1, 2, 3, 4, 5]",
        "print('List:', list1)",
        "list1.append(6)  # Add item to end",
        "print('After append:', list1)",
    ], "List creation and append operations")
    
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

    # Export tuple snippet
    snippet_section([
        "# Working with Tuples",
        "tuple1 = (1, 2, 3)",
        "print('Tuple:', tuple1)",
        "# Tuples are immutable - cannot add or remove items",
        "print('Cannot add or remove items from a tuple (immutable)')",
        "",
        "# But you can access elements:",
        "print('First element:', tuple1[0])",
        "print('Length:', len(tuple1))",
    ], "Tuple creation and immutability")

    # Check for interactive mode breakpoint
    check_interactive_mode()

    # Sets
    set1 = {1, 2, 3, 4}
    set_context('set')  # Set context for cs() function
    print("Set:", set1)
    set1.add(5)  # Add item
    print("After add:", set1)
    
    # Export set operations snippet
    snippet_section([
        "# Working with Sets",
        "set1 = {1, 2, 3, 4}",
        "print('Set:', set1)",
        "set1.add(5)  # Add item (duplicates ignored)",
        "print('After add:', set1)",
        "",
        "# Set operations:",
        "set2 = {4, 5, 6, 7}",
        "print('Union:', set1 | set2)",
        "print('Intersection:', set1 & set2)",
    ], "Set creation and operations")
    
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
    
    # Export dictionary operations snippet
    snippet_section([
        "# Working with Dictionaries",
        "dict1 = {'a': 1, 'b': 2, 'c': 3}",
        "print('Dictionary:', dict1)",
        "dict1['d'] = 4  # Add new key-value pair",
        "print('After adding key \"d\":', dict1)",
        "",
        "# Dictionary methods:",
        "print('Keys:', list(dict1.keys()))",
        "print('Values:', list(dict1.values()))",
        "print('Items:', list(dict1.items()))",
    ], "Dictionary creation and manipulation")
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    del dict1['b']  # Remove item
    print("After deleting key 'b':", dict1)

# Module metadata
DESCRIPTION = 'Basic Data Structures'
FUNCTION = basic_data_structures
