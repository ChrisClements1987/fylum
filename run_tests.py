#!/usr/bin/env python
"""
Automated test runner for Fylum V2.0.0
Runs both backend (pytest) and frontend (vitest) tests
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode == 0


def main():
    """Run all tests"""
    success = True
    
    # 1. Run backend tests (pytest)
    print("\n[BACKEND TESTS] Python/FastAPI")
    backend_success = run_command([
        "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])
    
    if not backend_success:
        print("[FAIL] Backend tests failed")
        success = False
    else:
        print("[PASS] Backend tests passed")
    
    # 2. Run frontend tests (vitest)
    print("\n[FRONTEND TESTS] Svelte/Vitest")
    web_dir = Path("web")
    
    if web_dir.exists():
        # Windows needs cmd /c for npm
        if sys.platform == "win32":
            cmd = ["cmd", "/c", "npm", "run", "test", "--", "--run"]
        else:
            cmd = ["npm", "run", "test", "--", "--run"]
        
        frontend_success = run_command(cmd, cwd=str(web_dir))
        
        if not frontend_success:
            print("[FAIL] Frontend tests failed")
            success = False
        else:
            print("[PASS] Frontend tests passed")
    else:
        print("[WARN] Frontend directory not found, skipping frontend tests")
    
    # 3. Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if success:
        print("[PASS] All tests passed!")
        return 0
    else:
        print("[FAIL] Some tests failed. See output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
