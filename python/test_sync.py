#!/usr/bin/env python3
"""
Test script to manually test copy mode sync functionality
"""

import sys
import os
sys.path.append('/home/adam/git/codeit/python')

from docker_manager import DockerEnvironmentManager

def test_sync():
    print("🧪 Testing copy mode sync functionality...")
    
    # Create manager and enable copy mode
    manager = DockerEnvironmentManager()
    manager.copy_mode = True
    
    # Check if container is running
    if not manager.is_container_running():
        print("❌ Container is not running. Please start it first with:")
        print("   python learn_python.py --cm --setup-env")
        return False
    
    print("✅ Container is running")
    
    # Test sync from container
    print("\n📁 Testing sync from container...")
    success = manager.sync_from_container()
    
    if success:
        print("✅ Sync completed successfully!")
        
        # Check if specific files exist
        test_files = [
            '/home/adam/git/codeit/practice/pandas/001.py',
            '/home/adam/git/codeit/practice/pandas'
        ]
        
        for file_path in test_files:
            if os.path.exists(file_path):
                print(f"✅ Found: {file_path}")
            else:
                print(f"❌ Missing: {file_path}")
    else:
        print("❌ Sync failed!")
    
    return success

if __name__ == "__main__":
    test_sync()
