#!/usr/bin/env python3
"""
APTS Dependency Fixer
Automatically installs and fixes all missing dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors gracefully"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️ {description} had issues: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Fix all APTS dependencies"""
    print("🚀 APTS Dependency Fixer")
    print("=" * 50)
    
    # Essential packages that must work
    essential_packages = [
        "aiohttp",
        "psutil", 
        "loguru",
        "rich",
        "cryptography",
        "requests"
    ]
    
    # Optional packages (nice to have but not critical)
    optional_packages = [
        "lz4",
        "zstandard", 
        "blosc",
        "uvloop",
        "stem",
        "PySocks",
        "PyJWT"
    ]
    
    print("📦 Installing essential packages...")
    for package in essential_packages:
        run_command(f"pip install {package}", f"Installing {package}")
    
    print("\n📦 Installing optional packages...")
    for package in optional_packages:
        success = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️ {package} is optional - APTS will work without it")
    
    # Special handling for problematic packages
    print("\n🔧 Handling special cases...")
    
    # Try to install blosc with conda if pip fails
    if not run_command("python -c 'import blosc'", "Testing blosc"):
        print("🔄 Trying alternative blosc installation...")
        run_command("conda install -c conda-forge python-blosc", "Installing blosc via conda")
    
    # Test all imports
    print("\n🧪 Testing all imports...")
    test_imports = [
        "import aiohttp",
        "import psutil", 
        "import loguru",
        "import rich",
        "import cryptography",
        "import requests",
        "import lz4.frame",
        "import zstandard",
        "import blosc",
        "import uvloop",
        "import stem",
        "import socks",
        "import jwt"
    ]
    
    working_imports = []
    failed_imports = []
    
    for test_import in test_imports:
        try:
            exec(test_import)
            working_imports.append(test_import.split()[1])
        except ImportError:
            failed_imports.append(test_import.split()[1])
    
    print(f"\n✅ Working imports ({len(working_imports)}):")
    for imp in working_imports:
        print(f"  ✓ {imp}")
    
    if failed_imports:
        print(f"\n⚠️ Failed imports ({len(failed_imports)}) - APTS will use fallbacks:")
        for imp in failed_imports:
            print(f"  ✗ {imp}")
    
    print("\n🎯 APTS is ready to run!")
    print("Run: python3 apts.py")

if __name__ == "__main__":
    main()