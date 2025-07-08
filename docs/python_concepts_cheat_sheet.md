# Python Concepts Cheat Sheet

## 📋 Table of Contents
- [Basic Data Structures](#basic-data-structures)
- [Advanced Data Structures](#advanced-data-structures)
- [CSV Module](#csv-module)
- [Pandas Data Analysis](#pandas-data-analysis)
- [Programming Challenges](#programming-challenges)
- [Advanced System Design](#advanced-system-design)
- [Database Operations](#database-operations)

---

## 🔤 Basic Data Structures

### Lists
```python
# Mutable, ordered collection
list1 = [1, 2, 3, 4, 5]
list1.append(6)        # Add to end
list1.remove(3)        # Remove by value
list1.insert(0, 0)     # Insert at position
list1.pop()            # Remove and return last
list1[0]               # Access by index
len(list1)             # Get length
```

### Tuples
```python
# Immutable, ordered collection
tuple1 = (1, 2, 3)
tuple1[0]              # Access by index
len(tuple1)            # Get length
# Cannot add/remove - immutable!
```

### Sets
```python
# Mutable, unordered collection of unique items
set1 = {1, 2, 3, 4}
set1.add(5)            # Add item
set1.discard(2)        # Remove item safely
set1 | set2            # Union
set1 & set2            # Intersection
set1 - set2            # Difference
```

### Dictionaries
```python
# Mutable, key-value mapping
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict1['d'] = 4         # Add/update
del dict1['b']         # Remove by key
dict1.keys()           # Get all keys
dict1.values()         # Get all values
dict1.items()          # Get key-value pairs
```

---

## 🎯 Advanced Data Structures

### defaultdict
```python
from collections import defaultdict
# Dictionary with default values for missing keys
dd = defaultdict(list)
dd['fruits'].append('apple')    # Automatically creates list
dd['missing_key']               # Returns empty list
```

### Counter
```python
from collections import Counter
# Dictionary for counting hashable objects
counter = Counter(['a', 'b', 'c', 'a', 'b', 'a'])
counter.most_common(2)          # Get 2 most common
counter.update(['a', 'd'])      # Add more counts
sum(counter.values())           # Total count
```

### OrderedDict
```python
from collections import OrderedDict
# Dictionary that maintains insertion order
od = OrderedDict([('first', 1), ('second', 2)])
od.move_to_end('first')         # Move key to end
od.move_to_end('second', last=False)  # Move to beginning
```

### deque
```python
from collections import deque
# Double-ended queue for efficient appends/pops
dq = deque([1, 2, 3, 4, 5])
dq.appendleft(0)               # Add to left (O(1))
dq.append(6)                   # Add to right (O(1))
dq.popleft()                   # Remove from left (O(1))
dq.pop()                       # Remove from right (O(1))
dq.rotate(2)                   # Rotate right by 2
```

### namedtuple
```python
from collections import namedtuple
# Tuple subclass with named fields
Person = namedtuple('Person', ['name', 'age', 'city'])
person = Person('Alice', 30, 'New York')
person.name                    # Access by name
person._replace(age=31)        # Create new with changed field
```

### ChainMap
```python
from collections import ChainMap
# Single view of multiple mappings
dict_a = {'a': 1, 'b': 2}
dict_b = {'b': 3, 'c': 4}
chain = ChainMap(dict_a, dict_b)
chain['b']                     # Returns 2 (from first dict)
```

### frozenset
```python
# Immutable version of set
fs = frozenset([1, 2, 3, 4, 5])
fs.union(other_set)            # Set operations available
fs.intersection(other_set)
# Cannot add/remove - immutable!
```

### dataclass
```python
from dataclasses import dataclass
@dataclass
class Student:
    name: str
    grade: int
    subjects: list = None
    
    def __post_init__(self):
        if self.subjects is None:
            self.subjects = []

student = Student('Bob', 85, ['Math', 'Science'])
```

---

## 📄 CSV Module

### Writing CSV Files
```python
import csv
# Basic writer
with open('file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age', 'city'])    # Write header
    writer.writerows(data_rows)                 # Write multiple rows

# Dictionary writer
with open('file.csv', 'w', newline='') as f:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 30, 'city': 'NYC'})
```

### Reading CSV Files
```python
import csv
# Basic reader
with open('file.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)                              # List of strings

# Dictionary reader
with open('file.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])          # Access by column name
```

---

## 🐼 Pandas Data Analysis

### DataFrame Creation
```python
import pandas as pd
# From dictionary
data = {'name': ['Alice', 'Bob'], 'age': [25, 30]}
df = pd.DataFrame(data)

# Basic info
df.shape                       # (rows, columns)
df.columns                     # Column names
df.dtypes                      # Data types
df.head()                      # First 5 rows
df.tail()                      # Last 5 rows
df.info()                      # Summary info
df.describe()                  # Statistical summary
```

### Data Selection & Filtering
```python
# Column selection
df['name']                     # Single column (Series)
df[['name', 'age']]           # Multiple columns (DataFrame)

# Row filtering
df[df['age'] > 25]            # Boolean indexing
df[df['name'].str.contains('A')] # String pattern matching
df[df['city'].isin(['NYC', 'LA'])] # Multiple values

# Advanced indexing
df.loc[df['age'] > 25, ['name', 'salary']]  # Label-based
df.iloc[:3, -2:]              # Position-based

# Query method
df.query('25 <= age <= 35')   # SQL-like syntax
```

### Data Manipulation
```python
# Adding columns
df['salary_k'] = df['salary'] / 1000
df['age_group'] = df['age'].apply(lambda x: 'Young' if x < 30 else 'Experienced')

# Conditional assignment
df['capped_salary'] = df['salary'].where(df['salary'] <= 60000, 60000)

# Sorting
df.sort_values('salary', ascending=False)
df.sort_values(['age_group', 'salary'])
```

### Grouping & Aggregation
```python
# Basic grouping
df.groupby('city')['salary'].mean()

# Multiple aggregations
df.groupby('age_group').agg({
    'salary': ['mean', 'max', 'count'],
    'age': 'mean'
})

# Custom aggregation functions
def salary_range(series):
    return series.max() - series.min()

df.groupby('city')['salary'].agg(['mean', 'std', salary_range])
```

### String Operations
```python
# Extract parts
df['first_name'] = df['full_name'].str.split().str[0]
df['last_name'] = df['full_name'].str.split().str[-1]

# Pattern matching with regex
df['domain'] = df['email'].str.extract(r'@(.+)')

# Cleaning
df['phone_clean'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
```

### Date/Time Operations
```python
# Convert to datetime
df['hire_date'] = pd.to_datetime(df['hire_date'])

# Extract components
df['hire_year'] = df['hire_date'].dt.year
df['hire_month'] = df['hire_date'].dt.month
df['hire_weekday'] = df['hire_date'].dt.day_name()

# Calculate differences
df['years_service'] = (pd.to_datetime('2023-12-31') - df['hire_date']).dt.days / 365.25
```

### Missing Data Handling
```python
# Detect missing data
df.isnull().sum()             # Count nulls per column
df.notnull().all()            # Check if any non-nulls

# Fill missing data
df['salary'].fillna(df['salary'].mean())      # Fill with mean
df['city'].fillna('Unknown')                  # Fill with constant
df['age'].fillna(method='ffill')              # Forward fill

# Drop missing data
df.dropna()                   # Drop rows with any null
df.dropna(subset=['salary'])  # Drop rows with null in specific column
```

### File I/O
```python
# CSV operations
df.to_csv('data.csv', index=False)
df_loaded = pd.read_csv('data.csv')

# Excel operations  
df.to_excel('data.xlsx', index=False)
df_loaded = pd.read_excel('data.xlsx')
```

### Advanced Operations
```python
# Transform (within groups)
df['salary_normalized'] = df.groupby('age_group')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Rolling window operations
df['salary_rolling_avg'] = df['salary'].rolling(window=3, min_periods=1).mean()

# Pivot tables
pivot = df.pivot_table(values='salary', index='age_group', aggfunc='mean')
```

---

## 🧩 Programming Challenges

### Basic Algorithms
```python
# Fibonacci with memoization
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

# Two sum problem
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return None
```

### Dynamic Programming
```python
# Longest common subsequence
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### String Algorithms
```python
# Run-length encoding for string compression
def string_count(string):
    """Compress consecutive characters with counts."""
    if not string:
        return ""
    
    result = ""
    counter = 1
    
    for index, letter in enumerate(string):
        if index > 0 and index < len(string):
            if letter == string[index - 1]:
                counter = counter + 1
            else:
                result = result + str(counter) + string[index - 1]
                counter = 1
        if index == len(string) - 1:
            result = result + str(counter) + letter
    return result

# Example: 'aaabbb' -> '3a3b'
```

---

## 🏗️ Advanced System Design

### Rate Limiting
```python
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
```

### LRU Cache
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
```

### Circuit Breaker
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout_duration=60):
        self.failure_threshold = failure_threshold
        self.timeout_duration = timeout_duration
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout_duration:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

---

## 🗄️ Database Operations

### Basic SQLite Operations
```python
import sqlite3

# Connect and execute
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

# Insert data
cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', 
               ('Alice', 'alice@example.com'))

# Query data
cursor.execute('SELECT * FROM users WHERE name = ?', ('Alice',))
results = cursor.fetchall()

# Batch operations
users_data = [('Bob', 'bob@example.com'), ('Charlie', 'charlie@example.com')]
cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users_data)

conn.commit()
conn.close()
```

### Database Design Principles
```sql
-- Normalized schema design
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexing strategies
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Performance optimization
-- Use EXPLAIN ANALYZE to check query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
```

### ACID Principles
- **Atomicity**: Transactions either complete fully or not at all
- **Consistency**: Database remains in valid state after transactions
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes survive system failures

---

## 🔧 Advanced Concepts

### Performance Optimization
```python
# Use list comprehensions for better performance
squares = [x**2 for x in range(1000)]

# Use generators for memory efficiency
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use sets for fast membership testing
valid_ids = {1, 2, 3, 4, 5}
if user_id in valid_ids:  # O(1) lookup
    process_user()
```

### Error Handling & Logging
```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_function():
    try:
        # Risky operation
        result = process_data()
        logger.info(f"Successfully processed: {result}")
        return result
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        raise
    finally:
        cleanup_resources()
```

### Testing Strategies
```python
import pytest

def test_fibonacci():
    assert fibonacci_memo(0) == 0
    assert fibonacci_memo(1) == 1
    assert fibonacci_memo(5) == 5
    assert fibonacci_memo(10) == 55

def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(2, 1)  # 2 requests per second
    assert limiter.allow_request() == True
    assert limiter.allow_request() == True
    assert limiter.allow_request() == False  # Should be rate limited
```

---

## 📚 References & Best Practices

### Code Style
- Use meaningful variable names
- Follow PEP 8 style guidelines
- Add docstrings for functions and classes
- Use type hints for better code documentation

### Performance Tips
- Use appropriate data structures for the task
- Avoid premature optimization
- Profile code to identify bottlenecks
- Use built-in functions and libraries when possible

### Security Considerations
- Validate and sanitize all inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Log security events for monitoring

---

*Generated from CodeIt Python Learning System - Interactive Python concepts with hands-on examples*
