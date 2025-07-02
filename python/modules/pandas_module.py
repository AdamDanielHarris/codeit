#!/usr/bin/env python3
"""
Pandas Module

Demonstrates data manipulation and analysis using the pandas library.
Shows DataFrames, Series, data reading/writing, and common operations.
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

def pandas_module(step=False):
    """
    Demonstrates pandas data manipulation and analysis.
    Shows DataFrames, Series, data operations, and file I/O.
    If step=True, drops into interactive shell after every line in this block.
    """
    def pandas_block():
        # First try to import numpy separately to provide better error messages
        try:
            import numpy as np
        except ImportError as e:
            error_msg = str(e).lower()
            
            # Check for the misleading "source directory" error that's actually a library issue
            if "you should not try to import numpy from its source directory" in error_msg:
                print("❌ Error: Numpy C-extension loading failed!")
                print("🔧 This error message is misleading - it's usually a system library issue.")
                print("💡 Solutions:")
                print("   1. Install system development libraries:")
                print("      - Ubuntu/Debian: sudo apt-get install build-essential libstdc++-12-dev")
                print("      - CentOS/RHEL: sudo yum install gcc-c++ libstdc++-devel")
                print("   2. Try using system packages instead:")
                print("      - Ubuntu/Debian: sudo apt-get install python3-numpy python3-pandas")
                print("   3. Use conda instead of pip: conda install numpy pandas")
                print("   4. Try numpy compiled for your system: pip install --only-binary=all numpy pandas")
                return
            else:
                print(f"❌ Error importing numpy: {e}")
                print("📦 Numpy is required for pandas. Install it with:")
                print("   pip install numpy pandas")
                print("   or use --install-packages numpy pandas to install in managed environment")
                return
        
        # Now try to import pandas
        try:
            import pandas as pd
        except ImportError as e:
            print(f"❌ Error importing pandas: {e}")
            print("📦 Pandas is not installed. Install it with:")
            print("   pip install pandas")
            print("   or use --install-packages pandas to install in managed environment")
            return
        except Exception as e:
            print(f"❌ Unexpected error importing pandas: {e}")
            print("💡 Try using a managed environment: python python/learn_python.py --setup-env")
            return
        
        set_context('pandas')  # Set context for cs() function
        print("🐼 Pandas Data Analysis Demonstration")
        print("=" * 50)
        
        # Create a simple DataFrame
        data = {
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'age': [25, 30, 35, 28, 32],
            'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
            'salary': [50000, 60000, 70000, 55000, 65000]
        }
        df = pd.DataFrame(data)
        print("Created DataFrame:")
        print(df)
        print()
        
        # Export snippet if snippet mode is enabled
        snippet_section([
            "# Create a simple DataFrame",
            "data = {",
            "    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],",
            "    'age': [25, 30, 35, 28, 32],",
            "    'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],",
            "    'salary': [50000, 60000, 70000, 55000, 65000]",
            "}",
            "df = pd.DataFrame(data)",
            "print('Created DataFrame:')",
            "print(df)"
        ], "Creating a DataFrame from dictionary")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Basic DataFrame operations
        set_context('dataframe')
        print("DataFrame Info:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types:\n{df.dtypes}")
        print()
        
        # Export snippet for DataFrame info
        snippet_section([
            "# Basic DataFrame operations",
            "print('DataFrame Info:')",
            "print(f'Shape: {df.shape}')",
            "print(f'Columns: {list(df.columns)}')",
            "print(f'Data types:\\n{df.dtypes}')"
        ], "Basic DataFrame information")
        print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Data selection and filtering
        set_context('dataframe_selection')
        print("Data Selection Examples:")
        print("Ages greater than 30:")
        filtered_df = df[df['age'] > 30]
        print(filtered_df)
        print()
        
        print("Names and salaries only:")
        subset_df = df[['name', 'salary']]
        print(subset_df)
        print()
        
        # Export snippet for data selection
        snippet_section([
            "# Data selection and filtering",
            "print('Ages greater than 30:')",
            "filtered_df = df[df['age'] > 30]",
            "print(filtered_df)",
            "",
            "print('Names and salaries only:')",
            "subset_df = df[['name', 'salary']]",
            "print(subset_df)"
        ], "Data selection and filtering")
        print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Statistical operations
        set_context('dataframe_stats')
        print("Statistical Summary:")
        print(df.describe())
        print()
        
        print("Average salary by city:")
        avg_salary = df.groupby('city')['salary'].mean()
        print(avg_salary)
        print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Adding new columns
        set_context('dataframe_modify')
        print("Adding calculated columns:")
        df['salary_k'] = df['salary'] / 1000  # Salary in thousands
        df['age_group'] = df['age'].apply(lambda x: 'Young' if x < 30 else 'Experienced')
        print(df)
        print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Series operations
        set_context('series')
        print("Series Operations:")
        ages = df['age']
        print(f"Age Series:\n{ages}")
        print(f"Mean age: {ages.mean():.1f}")
        print(f"Max age: {ages.max()}")
        print(f"Min age: {ages.min()}")
        print()
        
        # Export snippet for Series operations
        snippet_section([
            "# Series operations",
            "ages = df['age']",
            "print(f'Age Series:\\n{ages}')",
            "print(f'Mean age: {ages.mean():.1f}')",
            "print(f'Max age: {ages.max()}')",
            "print(f'Min age: {ages.min()}')"
        ], "Series operations and statistics")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Advanced Filtering & Boolean Indexing
        set_context('advanced_filtering')
        print("Advanced Filtering & Boolean Indexing:")
        print("=" * 40)
        
        # Multiple conditions with & and |
        print("Multiple conditions (age > 28 AND salary < 65000):")
        complex_filter = df[(df['age'] > 28) & (df['salary'] < 65000)]
        print(complex_filter)
        print()
        
        # String pattern matching
        print("Names containing 'a' (case insensitive):")
        name_filter = df[df['name'].str.lower().str.contains('a')]
        print(name_filter[['name', 'city']])
        print()
        
        # Using .isin() for multiple values
        print("People from London or Paris:")
        city_filter = df[df['city'].isin(['London', 'Paris'])]
        print(city_filter)
        print()
        
        # Using .query() method
        print("Using query method (age between 28 and 33):")
        query_result = df.query('28 <= age <= 33')
        print(query_result)
        print()
        
        # Export snippet for advanced filtering
        snippet_section([
            "# Advanced Filtering & Boolean Indexing",
            "",
            "# Multiple conditions",
            "complex_filter = df[(df['age'] > 28) & (df['salary'] < 65000)]",
            "print(complex_filter)",
            "",
            "# String pattern matching",
            "name_filter = df[df['name'].str.lower().str.contains('a')]",
            "print(name_filter[['name', 'city']])",
            "",
            "# Using .isin() for multiple values",
            "city_filter = df[df['city'].isin(['London', 'Paris'])]",
            "print(city_filter)",
            "",
            "# Using .query() method",
            "query_result = df.query('28 <= age <= 33')",
            "print(query_result)"
        ], "Advanced filtering and boolean indexing")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Complex Data Manipulation
        set_context('advanced_manipulation')
        print("Complex Data Manipulation:")
        print("=" * 40)
        
        # .loc and .iloc advanced indexing
        print("Using .loc for label-based indexing:")
        print("People aged 30 or more, showing name and salary:")
        loc_result = df.loc[df['age'] >= 30, ['name', 'salary']]
        print(loc_result)
        print()
        
        print("Using .iloc for position-based indexing (first 3 rows, last 2 columns):")
        iloc_result = df.iloc[:3, -2:]
        print(iloc_result)
        print()
        
        # Conditional assignment with .where()
        print("Conditional assignment - cap salaries at 60k:")
        df_copy = df.copy()
        df_copy['capped_salary'] = df_copy['salary'].where(df_copy['salary'] <= 60000, 60000)
        print(df_copy[['name', 'salary', 'capped_salary']])
        print()
        
        # Advanced groupby operations
        print("Advanced groupby - multiple aggregations:")
        agg_result = df.groupby('age_group').agg({
            'salary': ['mean', 'max', 'count'],
            'age': 'mean'
        })
        print(agg_result)
        print()
        
        # Export snippet for complex manipulation
        snippet_section([
            "# Complex Data Manipulation",
            "",
            "# .loc for label-based indexing",
            "loc_result = df.loc[df['age'] >= 30, ['name', 'salary']]",
            "print(loc_result)",
            "",
            "# .iloc for position-based indexing",
            "iloc_result = df.iloc[:3, -2:]",
            "print(iloc_result)",
            "",
            "# Conditional assignment with .where()",
            "df_copy = df.copy()",
            "df_copy['capped_salary'] = df_copy['salary'].where(df_copy['salary'] <= 60000, 60000)",
            "print(df_copy[['name', 'salary', 'capped_salary']])",
            "",
            "# Advanced groupby operations",
            "agg_result = df.groupby('age_group').agg({",
            "    'salary': ['mean', 'max', 'count'],",
            "    'age': 'mean'",
            "})",
            "print(agg_result)"
        ], "Complex data manipulation techniques")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # String Operations & Pattern Matching
        set_context('string_operations')
        print("String Operations & Pattern Matching:")
        print("=" * 40)
        
        # Create a DataFrame with more complex string data
        string_data = {
            'full_name': ['Alice Johnson', 'Bob Smith-Wilson', 'Charlie Brown', 'Diana Lee', 'Eve Davis'],
            'email': ['alice.j@email.com', 'bob.sw@company.org', 'charlie@test.net', 'diana@work.com', 'eve.d@site.co.uk'],
            'phone': ['(555) 123-4567', '555-987-6543', '(555) 246-8135', '555.369.2580', '(555) 147-2589']
        }
        df_strings = pd.DataFrame(string_data)
        print("String data DataFrame:")
        print(df_strings)
        print()
        
        # Extract first and last names
        print("Extracting first and last names:")
        df_strings['first_name'] = df_strings['full_name'].str.split().str[0]
        df_strings['last_name'] = df_strings['full_name'].str.split().str[-1]
        print(df_strings[['full_name', 'first_name', 'last_name']])
        print()
        
        # Extract email domains
        print("Extracting email domains:")
        df_strings['domain'] = df_strings['email'].str.extract(r'@(.+)')
        print(df_strings[['email', 'domain']])
        print()
        
        # Clean phone numbers
        print("Cleaning phone numbers (digits only):")
        df_strings['phone_clean'] = df_strings['phone'].str.replace(r'[^\d]', '', regex=True)
        print(df_strings[['phone', 'phone_clean']])
        print()
        
        # Export snippet for string operations
        snippet_section([
            "# String Operations & Pattern Matching",
            "",
            "# Extract first and last names",
            "df_strings['first_name'] = df_strings['full_name'].str.split().str[0]",
            "df_strings['last_name'] = df_strings['full_name'].str.split().str[-1]",
            "",
            "# Extract email domains using regex",
            "df_strings['domain'] = df_strings['email'].str.extract(r'@(.+)')",
            "",
            "# Clean phone numbers (keep digits only)",
            "df_strings['phone_clean'] = df_strings['phone'].str.replace(r'[^\\d]', '', regex=True)"
        ], "String operations and pattern matching")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Advanced Aggregations & Transforms
        set_context('advanced_aggregations')
        print("Advanced Aggregations & Transforms:")
        print("=" * 40)
        
        # Custom aggregation function
        def salary_range(series):
            return series.max() - series.min()
        
        print("Custom aggregation - salary range by age group:")
        custom_agg = df.groupby('age_group')['salary'].agg(['mean', 'std', salary_range])
        print(custom_agg)
        print()
        
        # Transform vs Apply
        print("Transform - normalize salaries within age groups:")
        df_transform = df.copy()
        df_transform['salary_normalized'] = df_transform.groupby('age_group')['salary'].transform(
            lambda x: (x - x.mean()) / x.std()
        )
        print(df_transform[['name', 'age_group', 'salary', 'salary_normalized']])
        print()
        
        # Rolling window operations
        print("Rolling window - 3-period moving average of salary:")
        df_sorted = df.sort_values('age')
        df_sorted['salary_rolling_avg'] = df_sorted['salary'].rolling(window=3, min_periods=1).mean()
        print(df_sorted[['name', 'age', 'salary', 'salary_rolling_avg']].round(2))
        print()
        
        # Export snippet for advanced aggregations
        snippet_section([
            "# Advanced Aggregations & Transforms",
            "",
            "# Custom aggregation function",
            "def salary_range(series):",
            "    return series.max() - series.min()",
            "",
            "custom_agg = df.groupby('age_group')['salary'].agg(['mean', 'std', salary_range])",
            "print(custom_agg)",
            "",
            "# Transform - normalize within groups",
            "df_transform = df.copy()",
            "df_transform['salary_normalized'] = df_transform.groupby('age_group')['salary'].transform(",
            "    lambda x: (x - x.mean()) / x.std()",
            ")",
            "",
            "# Rolling window operations",
            "df_sorted = df.sort_values('age')",
            "df_sorted['salary_rolling_avg'] = df_sorted['salary'].rolling(window=3, min_periods=1).mean()"
        ], "Advanced aggregations and transforms")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Date/Time Operations
        set_context('datetime_operations')
        print("Date/Time Operations:")
        print("=" * 40)
        
        # Create datetime data
        date_data = {
            'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'hire_date': ['2020-01-15', '2019-06-30', '2021-03-10', '2020-11-22', '2018-09-05'],
            'last_review': ['2023-01-15', '2023-06-30', '2023-03-10', '2023-11-22', '2023-09-05']
        }
        df_dates = pd.DataFrame(date_data)
        
        # Convert to datetime
        df_dates['hire_date'] = pd.to_datetime(df_dates['hire_date'])
        df_dates['last_review'] = pd.to_datetime(df_dates['last_review'])
        print("DataFrame with datetime columns:")
        print(df_dates)
        print()
        
        # Calculate time differences
        print("Years of service (as of 2023-12-31):")
        reference_date = pd.to_datetime('2023-12-31')
        df_dates['years_service'] = (reference_date - df_dates['hire_date']).dt.days / 365.25
        print(df_dates[['name', 'hire_date', 'years_service']].round(2))
        print()
        
        # Extract date components
        print("Hire date components:")
        df_dates['hire_year'] = df_dates['hire_date'].dt.year
        df_dates['hire_month'] = df_dates['hire_date'].dt.month
        df_dates['hire_weekday'] = df_dates['hire_date'].dt.day_name()
        print(df_dates[['name', 'hire_date', 'hire_year', 'hire_month', 'hire_weekday']])
        print()
        
        # Export snippet for datetime operations
        snippet_section([
            "# Date/Time Operations",
            "",
            "# Convert to datetime",
            "df_dates['hire_date'] = pd.to_datetime(df_dates['hire_date'])",
            "df_dates['last_review'] = pd.to_datetime(df_dates['last_review'])",
            "",
            "# Calculate time differences",
            "reference_date = pd.to_datetime('2023-12-31')",
            "df_dates['years_service'] = (reference_date - df_dates['hire_date']).dt.days / 365.25",
            "",
            "# Extract date components",
            "df_dates['hire_year'] = df_dates['hire_date'].dt.year",
            "df_dates['hire_month'] = df_dates['hire_date'].dt.month",
            "df_dates['hire_weekday'] = df_dates['hire_date'].dt.day_name()"
        ], "Date and time operations")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Missing Data Handling
        set_context('missing_data')
        print("Missing Data Handling:")
        print("=" * 40)
        
        # Introduce some missing data
        df_missing = df.copy()
        df_missing.loc[1, 'salary'] = None  # Bob's salary missing
        df_missing.loc[3, 'city'] = None    # Diana's city missing
        df_missing.loc[4, 'age'] = None     # Eve's age missing
        
        print("DataFrame with missing values:")
        print(df_missing)
        print()
        
        print("Missing data info:")
        print(f"Missing values per column:\n{df_missing.isnull().sum()}")
        print()
        
        # Different filling strategies
        print("Fill missing salaries with mean:")
        df_filled = df_missing.copy()
        df_filled['salary'] = df_filled['salary'].fillna(df_filled['salary'].mean())
        print(df_filled[['name', 'salary']])
        print()
        
        print("Fill missing cities with 'Unknown':")
        df_filled['city'] = df_filled['city'].fillna('Unknown')
        print(df_filled[['name', 'city']])
        print()
        
        print("Forward fill missing ages:")
        df_filled['age'] = df_filled['age'].fillna(method='ffill')
        print(df_filled[['name', 'age']])
        print()
        
        # Dropping rows with missing data
        print("Drop rows with any missing values:")
        df_dropped = df_missing.dropna()
        print(f"Original shape: {df_missing.shape}, After dropping: {df_dropped.shape}")
        print(df_dropped)
        print()
        
        # Export snippet for missing data handling
        snippet_section([
            "# Missing Data Handling",
            "",
            "# Check for missing values",
            "print(f'Missing values per column:\\n{df_missing.isnull().sum()}')",
            "",
            "# Fill missing values with different strategies",
            "df_filled = df_missing.copy()",
            "df_filled['salary'] = df_filled['salary'].fillna(df_filled['salary'].mean())",
            "df_filled['city'] = df_filled['city'].fillna('Unknown')",
            "df_filled['age'] = df_filled['age'].fillna(method='ffill')",
            "",
            "# Drop rows with missing values",
            "df_dropped = df_missing.dropna()",
            "print(f'Original shape: {df_missing.shape}, After dropping: {df_dropped.shape}')"
        ], "Missing data handling strategies")
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # File I/O operations
        set_context('pandas_io')
        print("File I/O Operations:")
        
        # Use a container-friendly temp directory
        if os.path.exists('/workspace'):
            # We're in Docker container, use /tmp which is writable
            temp_dir = '/tmp'
        else:
            # We're on host system, use project temp directory
            temp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
            os.makedirs(temp_dir, exist_ok=True)
        
        # Save to CSV
        csv_file = os.path.join(temp_dir, 'pandas_data.csv')
        df.to_csv(csv_file, index=False)
        print(f"Saved DataFrame to: {csv_file}")
        
        # Read from CSV
        df_loaded = pd.read_csv(csv_file)
        print("Loaded DataFrame from CSV:")
        print(df_loaded.head())
        print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Data manipulation examples
        set_context('dataframe_manipulation')
        print("Data Manipulation Examples:")
        
        # Sorting
        df_sorted = df.sort_values('salary', ascending=False)
        print("Sorted by salary (descending):")
        print(df_sorted[['name', 'salary']])
        print()
        
        # Pivot operations
        if len(df) > 3:  # Only if we have enough data
            pivot_data = df.pivot_table(values='salary', index='age_group', aggfunc='mean')
            print("Average salary by age group:")
            print(pivot_data)
            print()
        
        # Check for interactive mode breakpoint
        check_interactive_mode()
        
        # Clean up
        try:
            os.remove(csv_file)
            print(f"Cleaned up: {csv_file}")
        except OSError:
            pass
        
        print("🎉 Pandas demonstration completed!")
    
    if step:
        step_through_function(pandas_block, globals(), locals())
    else:
        pandas_block()

# Module metadata
DESCRIPTION = 'Pandas Data Analysis'
FUNCTION = pandas_module
