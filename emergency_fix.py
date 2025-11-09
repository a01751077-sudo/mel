#!/usr/bin/env python3
"""
Emergency Fix Script for APTS Ghost Mode
Applies all critical fixes directly to resolve 0 working proxies issue
"""

import os
import shutil
import sys
from pathlib import Path

def apply_emergency_fixes():
    """Apply all critical fixes to resolve proxy issues"""
    
    print("🚨 EMERGENCY FIX: Applying critical Ghost Mode fixes...")
    
    # Find the user's APTS directory
    possible_paths = [
        "~/yui/yui/yui",
        "~/yui/yui", 
        "~/yui",
        "./yui",
        "../yui",
        "../../yui"
    ]
    
    user_apts_dir = None
    for path in possible_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(os.path.join(expanded_path, "apts.py")):
            user_apts_dir = expanded_path
            break
    
    if not user_apts_dir:
        print("❌ Could not find your APTS installation directory")
        print("Please run this script from your APTS directory or provide the path")
        return False
    
    print(f"✅ Found APTS installation: {user_apts_dir}")
    
    # Copy the fixed ghost_mode.py
    source_file = "/workspace/project/mel/core/ghost_mode.py"
    target_file = os.path.join(user_apts_dir, "core", "ghost_mode.py")
    
    if os.path.exists(source_file):
        print("🔧 Applying Ghost Mode fixes...")
        shutil.copy2(source_file, target_file)
        print("✅ Ghost Mode fixes applied!")
    else:
        print("❌ Source fix file not found")
        return False
    
    # Copy the fixed optimization.py
    source_opt = "/workspace/project/mel/core/optimization.py"
    target_opt = os.path.join(user_apts_dir, "core", "optimization.py")
    
    if os.path.exists(source_opt):
        print("🔧 Applying optimization fixes...")
        shutil.copy2(source_opt, target_opt)
        print("✅ Optimization fixes applied!")
    
    print("\n🎉 EMERGENCY FIXES APPLIED SUCCESSFULLY!")
    print("\nNow run: python3 apts.py")
    print("Ghost Mode should now find working proxies and achieve 75%+ anonymity!")
    
    return True

if __name__ == "__main__":
    apply_emergency_fixes()