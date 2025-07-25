#!/usr/bin/env python3
"""Test script to verify import resolution after directory restructuring"""

import sys
import os

def test_imports():
    """Test importing src modules after moving to root level"""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")
    
    print("\n=== Testing imports after directory restructuring ===")
    
    try:
        import src.main
        print("✅ src.main import successful")
    except Exception as e:
        print(f"❌ src.main import failed: {e}")
    
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
        import src.modules.transcript_processor
        print("✅ src.modules.transcript_processor import successful")
    except Exception as e:
        print(f"❌ src.modules.transcript_processor import failed: {e}")
    
    try:
        import config
        print("✅ config import successful")
    except Exception as e:
        print(f"❌ config import failed: {e}")

if __name__ == "__main__":
    test_imports()
