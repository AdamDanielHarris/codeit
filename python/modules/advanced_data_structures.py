#!/usr/bin/env python3
"""
Advanced Data Structures Module

Demonstrates advanced built-in data structures in Python including collections module
structures and their useful methods.
"""

from collections import defaultdict, Counter, OrderedDict, deque, namedtuple, ChainMap
from dataclasses import dataclass

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

def advanced_data_structures():
    """
    Demonstrates advanced built-in data structures in Python.
    Shows collections module structures and their useful methods.
    """
    # defaultdict - Dictionary with default values for missing keys
    dd1 = defaultdict(list)
    set_context('defaultdict')  # Set context for cs() function
    dd1['fruits'].append('apple')
    dd1['fruits'].append('banana')
    dd1['vegetables'].append('carrot')
    print("defaultdict (list):", dict(dd1))
    print("Accessing non-existent key 'grains':", dd1['grains'])  # Creates empty list
    
    # Export defaultdict snippet
    snippet_section([
        "from collections import defaultdict",
        "",
        "# defaultdict - Dictionary with default values for missing keys",
        "dd1 = defaultdict(list)",
        "dd1['fruits'].append('apple')",
        "dd1['fruits'].append('banana')",
        "dd1['vegetables'].append('carrot')",
        "print('defaultdict (list):', dict(dd1))",
        "print('Accessing non-existent key \"grains\":', dd1['grains'])",  # Creates empty list
    ], "defaultdict with list factory")
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # Counter - Dictionary for counting hashable objects
    counter1 = Counter(['a', 'b', 'c', 'a', 'b', 'a'])
    set_context('counter')  # Set context for cs() function
    print("Counter:", counter1)
    counter1.update(['a', 'd', 'd'])  # Add more counts
    print("After update:", counter1)
    print("Most common (2):", counter1.most_common(2))
    
    # Export Counter snippet
    snippet_section([
        "from collections import Counter",
        "",
        "# Counter - Dictionary for counting hashable objects",
        "counter1 = Counter(['a', 'b', 'c', 'a', 'b', 'a'])",
        "print('Counter:', counter1)",
        "counter1.update(['a', 'd', 'd'])  # Add more counts",
        "print('After update:', counter1)",
        "print('Most common (2):', counter1.most_common(2))",
        "",
        "# Other useful Counter methods:",
        "print('Total count:', sum(counter1.values()))",
        "print('Elements as list:', list(counter1.elements()))",
    ], "Counter for counting objects")
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # OrderedDict - Dictionary that maintains insertion order
    od1 = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
    print("OrderedDict:", od1)
    od1.move_to_end('first')  # Move key to end
    print("After move_to_end('first'):", od1)
    
    # Export OrderedDict snippet
    snippet_section([
        "from collections import OrderedDict",
        "",
        "# OrderedDict - Dictionary that maintains insertion order",
        "od1 = OrderedDict([('first', 1), ('second', 2), ('third', 3)])",
        "print('OrderedDict:', od1)",
        "od1.move_to_end('first')  # Move key to end",
        "print('After move_to_end(\"first\"):', od1)",
        "",
        "# Other OrderedDict methods:",
        "od1.move_to_end('second', last=False)  # Move to beginning",
        "print('After move_to_end(\"second\", last=False):', od1)",
    ], "OrderedDict operations")
    
    # Check for interactive mode breakpoint
    check_interactive_mode()
    
    # deque - Double-ended queue for efficient appends/pops
    deque1 = deque([1, 2, 3, 4, 5])
    set_context('deque')  # Set context for cs() function
    print("deque:", deque1)
    deque1.appendleft(0)  # Add to left
    deque1.append(6)  # Add to right
    print("After appends:", deque1)
    
    # Export deque snippet
    snippet_section([
        "from collections import deque",
        "",
        "# deque - Double-ended queue for efficient appends/pops",
        "deque1 = deque([1, 2, 3, 4, 5])",
        "print('deque:', deque1)",
        "deque1.appendleft(0)  # Add to left",
        "deque1.append(6)  # Add to right",
        "print('After appends:', deque1)",
        "",
        "# Efficient operations:",
        "left_item = deque1.popleft()  # Remove from left",
        "right_item = deque1.pop()  # Remove from right",
        "print('Popped left:', left_item, 'right:', right_item)",
    ], "deque operations")
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

# Module metadata
DESCRIPTION = 'Advanced Data Structures'
FUNCTION = advanced_data_structures
