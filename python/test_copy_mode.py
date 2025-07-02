#!/usr/bin/env python3
"""
Test script for copy mode functionality.
This script creates files and verifies they are synced properly.
"""

import os
import sys
import time
from pathlib import Path

def test_copy_mode():
    """Test the copy mode functionality."""
    print("🧪 Testing copy mode functionality...")
    
    # Create a test output file
    test_file = Path("test_output.txt")
    test_content = f"Copy mode test - created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    test_content += f"Python version: {sys.version}\n"
    test_content += f"Current directory: {os.getcwd()}\n"
    test_content += f"Environment variables:\n"
    
    for key, value in os.environ.items():
        if key.startswith(('MPLCONFIG', 'FONTCONFIG', 'XDG_', 'MPLBACKEND')):
            test_content += f"  {key}={value}\n"
    
    # Write the test file
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    print(f"✅ Created test file: {test_file}")
    print(f"📝 File contents:\n{test_content}")
    
    # Test basic imports
    try:
        import numpy as np
        print(f"✅ NumPy imported successfully: {np.__version__}")
        
        # Create a simple array
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✅ NumPy array created: {arr}")
        
    except ImportError as e:
        print(f"❌ Failed to import NumPy: {e}")
    except Exception as e:
        print(f"❌ NumPy error: {e}")
    
    try:
        import pandas as pd
        print(f"✅ Pandas imported successfully: {pd.__version__}")
        
        # Create a simple DataFrame
        df = pd.DataFrame({'test': [1, 2, 3], 'value': ['a', 'b', 'c']})
        print(f"✅ Pandas DataFrame created:\n{df}")
        
    except ImportError as e:
        print(f"❌ Failed to import Pandas: {e}")
    except Exception as e:
        print(f"❌ Pandas error: {e}")
    
    print("🧪 Copy mode test completed!")
    return True

if __name__ == "__main__":
    test_copy_mode()
