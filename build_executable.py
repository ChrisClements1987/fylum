#!/usr/bin/env python
"""
Build script for creating standalone Fylum executables.
Run this script to package Fylum as a single executable file.
"""

import sys
import subprocess
import shutil
from pathlib import Path


def build_executable():
    """Build the standalone executable using PyInstaller."""
    print("=" * 60)
    print("Building Fylum Standalone Executable")
    print("=" * 60)
    
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"])
        print("✓ PyInstaller installed")
    
    print("\n Building executable with PyInstaller...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=fylum",
        "--clean",
        "--noconfirm",
        "app.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build completed successfully!")
        
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("fylum*"))
            if exe_files:
                print(f"\n Executable location: {exe_files[0]}")
                print(f" Size: {exe_files[0].stat().st_size / (1024*1024):.2f} MB")
        
        print("\n" + "=" * 60)
        print("Build Complete!")
        print("=" * 60)
        print("\nTo test the executable:")
        if sys.platform == "win32":
            print("  .\\dist\\fylum.exe --help")
        else:
            print("  ./dist/fylum --help")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
