#!/usr/bin/env python3
"""Test script to verify the new directory structure works"""

import sys
import os

def test_new_structure():
    """Test the new structure with main.py and config.py both in src/"""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")
    
    print("\n=== Testing new directory structure ===")
    
    try:
        import src.main
        print("✅ src.main import successful")
    except Exception as e:
        print(f"❌ src.main import failed: {e}")
    
    try:
        import src.config
        print("✅ src.config import successful")
    except Exception as e:
        print(f"❌ src.config import failed: {e}")
    
    try:
        import src.routers.minutes
        print("✅ src.routers.minutes import successful")
    except Exception as e:
        print(f"❌ src.routers.minutes import failed: {e}")
    
    try:
        import src.modules.azure_openai_client
        print("✅ src.modules.azure_openai_client import successful")
    except Exception as e:
        print(f"❌ src.modules.azure_openai_client import failed: {e}")
    
    try:
        from src.config import settings
        print("✅ settings import from src.config successful")
    except Exception as e:
        print(f"❌ settings import from src.config failed: {e}")

if __name__ == "__main__":
    test_new_structure()
