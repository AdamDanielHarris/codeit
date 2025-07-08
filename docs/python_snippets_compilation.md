# Python Concepts - All Snippets Compilation

This document contains all the practice snippets from your interactive learning sessions, organized by module. Each snippet represents hands-on code you can run and modify.

## 📋 Table of Contents
- [Basic Data Structures](#basic-data-structures)
- [Advanced Data Structures](#advanced-data-structures) 
- [CSV Module](#csv-module)
- [Pandas Data Analysis](#pandas-data-analysis)
- [Programming Challenges](#programming-challenges)
- [Advanced Programming Challenges](#advanced-programming-challenges)
- [Database Operations](#database-operations)

---

## 🔤 Basic Data Structures

### Snippet 1: Lists
```python
# Basic Practice Snippet 1
# List creation and append operations
# Extracted from interactive learning session

# Working with Lists
list1 = [1, 2, 3, 4, 5]
print('List:', list1)
list1.append(6)  # Add item to end
print('After append:', list1)
```

### Snippet 2: Tuples
```python
# Basic Practice Snippet 2
# Tuple creation and immutability
# Extracted from interactive learning session

# Working with Tuples
tuple1 = (1, 2, 3)
print('Tuple:', tuple1)
# Tuples are immutable - cannot add or remove items
print('Cannot add or remove items from a tuple (immutable)')

# But you can access elements:
print('First element:', tuple1[0])
print('Length:', len(tuple1))

# Named tuple
tuple2 = ({'name': 'Alice', 'age': 30})
```

### Snippet 3: Sets
```python
# Basic Practice Snippet 3
# Set creation and operations
# Extracted from interactive learning session

# Working with Sets
set1 = {1, 2, 3, 4}
print('Set:', set1)
set1.add(5)  # Add item (duplicates ignored)
print('After add:', set1)

# Set operations:
set2 = {4, 5, 6, 7}
print('Union:', set1 | set2)
print('Intersection:', set1 & set2)

# Benefits of using sets:
# - Unordered collection of unique items
# - Fast membership testing
# - Useful for mathematical set operations like union, intersection, and difference
# - Can be used to remove duplicates from a list
# - Supports operations like subset, superset, and disjoint
```

### Snippet 4: Dictionaries
```python
# Basic Practice Snippet 4
# Dictionary creation and manipulation
# Extracted from interactive learning session

# Working with Dictionaries
dict1 = {'a': 1, 'b': 2, 'c': 3}
print('Dictionary:', dict1)
dict1['d'] = 4  # Add new key-value pair
print('After adding key "d":', dict1)

# Dictionary methods:
print('Keys:', list(dict1.keys()))
print('Values:', list(dict1.values()))
print('Items:', list(dict1.items()))

dict1['e'] = 5
```

---

## 🎯 Advanced Data Structures

### Snippet 1: defaultdict
```python
# Advanced Practice Snippet 1
# defaultdict with list factory
# Extracted from interactive learning session

from collections import defaultdict

# defaultdict - Dictionary with default values for missing keys
dd1 = defaultdict(list)
dd1['fruits'].append('apple')
dd1['fruits'].append('banana')
dd1['vegetables'].append('carrot')
print('defaultdict (list):', dict(dd1))
print('Accessing non-existent key "grains":', dd1['grains'])
```

### Snippet 2: Counter
```python
# Advanced Practice Snippet 2
# Counter for counting objects
# Extracted from interactive learning session

from collections import Counter

# Counter - Dictionary for counting hashable objects
counter1 = Counter(['a', 'b', 'c', 'a', 'b', 'a'])
print('Counter:', counter1)
counter1.update(['a', 'd', 'd'])  # Add more counts
print('After update:', counter1)
print('Most common (2):', counter1.most_common(2))

# Other useful Counter methods:
print('Total count:', sum(counter1.values()))
print('Elements as list:', list(counter1.elements()))
```

### Snippet 3: OrderedDict
```python
# Advanced Practice Snippet 3
# OrderedDict operations
# Extracted from interactive learning session

from collections import OrderedDict

# OrderedDict - Dictionary that maintains insertion order
od1 = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
print('OrderedDict:', od1)
od1.move_to_end('first')  # Move key to end
print('After move_to_end("first"):', od1)

# Other OrderedDict methods:
od1.move_to_end('second', last=False)  # Move to beginning
print('After move_to_end("second", last=False):', od1)
```

---

## 📄 CSV Module

### Snippet 1: Setting up CSV Data
```python
# Csv_Module Practice Snippet 1
# Setting up CSV data
# Extracted from interactive learning session

import csv
import os

# Create sample data
rows = [
    ["name", "age", "city"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "London"],
    ["Charlie", 35, "Paris"]
]
```

### Snippet 2: Writing CSV Files
```python
# Csv_Module Practice Snippet 2
# Writing data to CSV file
# Extracted from interactive learning session

import csv

# Write data to CSV file
filename = "example.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print(f"Wrote CSV file: {filename}")
```

### Snippet 3: Reading CSV Files
```python
# Csv_Module Practice Snippet 3
# Reading data from CSV file
# Extracted from interactive learning session

import csv

# Read CSV file
filename = "example.csv"
with open(filename, "r", newline="") as f:
    reader = csv.reader(f)
    print("CSV contents:")
    for row in reader:
        print("  ", row)
```

---

## 🐼 Pandas Data Analysis

### Snippet 1: DataFrame Creation
```python
# Pandas Practice Snippet 1
# Creating a DataFrame from dictionary
# Extracted from interactive learning session

import pandas as pd

# Create a simple DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
    'salary': [50000, 60000, 70000, 55000, 65000]
}
df = pd.DataFrame(data)
print('Created DataFrame:')
print(df)
```

### Snippet 2: DataFrame Information
```python
# Pandas Practice Snippet 2
# Basic DataFrame information
# Extracted from interactive learning session

# Basic DataFrame operations
print('DataFrame Info:')
print(f'Shape: {df.shape}')
print(f'Columns: {list(df.columns)}')
print(f'Data types:\n{df.dtypes}')
```

---

## 🧩 Programming Challenges

### Basic Algorithms
*See challenges/ practice directory for more examples*

---

## 🚀 Advanced Programming Challenges

### Snippet 1: Rate Limiter
```python
# Challenges_2 Practice Snippet 1
# Sliding window rate limiter for API endpoints
# Extracted from interactive learning session

# Sliding Window Rate Limiter Implementation

from collections import deque
import time

class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()

    def allow_request(self):
        now = time.time()
        # Remove old requests outside the window
        while self.requests and self.requests[0] <= now - self.window_seconds:
            self.requests.popleft()

        # Check if we can allow this request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

# Usage example
limiter = SlidingWindowRateLimiter(5, 10)  # 5 requests per 10 seconds
allowed = limiter.allow_request()
print(f'Request allowed: {allowed}')
```

---

## 🗄️ Database Operations

*See database/ practice directory for more examples*

---

## 📚 How to Use These Snippets

Each snippet is a complete, runnable Python program that demonstrates specific concepts:

1. **Copy and Run**: Copy any snippet into a Python file and run it
2. **Modify and Experiment**: Change values, add print statements, try variations  
3. **Combine Concepts**: Mix snippets from different modules to build larger programs
4. **Practice**: Use these as starting points for your own projects

## 📝 Snippet Sources

All snippets were extracted from interactive learning sessions using the CodeIt Python Learning System. Each snippet represents hands-on code that was demonstrated and tested in interactive breakpoints.

### Directory Structure
```
practice/
├── basic/              # Basic data structures
├── advanced/           # Advanced data structures  
├── csv_module/         # CSV file operations
├── pandas/             # Data analysis with pandas
├── challenges/         # Programming challenges
├── challenges_2/       # Advanced system design challenges
└── database/           # Database operations
```

---

*Generated from CodeIt Python Learning System - All practice snippets compilation*
