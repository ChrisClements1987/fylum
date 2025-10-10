# Fylum UAT Testing Guide

**For UAT Testers and QA Team**

This guide will walk you through the complete process of testing Fylum UAT releases, from installation to reporting your findings.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Running the Test Script](#running-the-test-script)
5. [Creating an Execution Report](#creating-an-execution-report)
6. [Submitting Your Report](#submitting-your-report)

---

## Overview

User Acceptance Testing (UAT) validates that Fylum works correctly in real-world scenarios before official release. As a UAT tester, you'll:

1. Install a specific UAT version (release candidate)
2. Execute a standardized test script
3. Document your findings
4. Submit your test execution report

**Time Required:** Approximately 30-45 minutes

---

## Prerequisites

### Required Software

- **Python 3.8 or higher**
  - Check: Open terminal/command prompt and run `python --version`
  - Download from: https://www.python.org/downloads/

- **Git** (for checking out UAT branches)
  - Check: Run `git --version`
  - Download from: https://git-scm.com/downloads

- **Text Editor** (VS Code, Notepad++, or similar)

### System Requirements

- Windows, macOS, or Linux
- At least 100 MB free disk space
- Read/write permissions for creating test folders

---

## Installation Steps

### Step 1: Clone the Repository

```bash
# Open terminal/command prompt
git clone https://github.com/ChrisClements1987/fylum.git
cd fylum
```

### Step 2: Checkout the UAT Release Tag

**You will be given a specific tag to test** (e.g., `v1.0.0-rc1`, `v1.0.0-rc2`)

```bash
# Replace TAG_NAME with the tag provided by developers
git checkout TAG_NAME

# Example:
# git checkout v1.0.0-rc2
```

**Verify you're on the correct tag:**
```bash
git describe --tags
```

### Step 3: Create Python Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**You should see `(.venv)` prefix in your terminal prompt**

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Verify installation:**
```bash
python app.py --help
```

You should see Fylum's help menu.

### Step 5: Verify Test Suite (Optional but Recommended)

```bash
pip install -r requirements-dev.txt
pytest --maxfail=1 --disable-warnings -v
```

**Expected:** Most tests should pass. Note any failures.

---

## Running the Test Script

### Test Environment Setup

#### Create Test Workspace

```bash
# Create a test directory (NOT in the fylum repo)
mkdir ~/FylumUATTest
cd ~/FylumUATTest

# Create test target folder
mkdir test-downloads
```

#### Create Sample Test Files

Create the following files in `test-downloads/`:

```bash
cd test-downloads

# Create sample files (adjust commands for your OS)
# Windows PowerShell:
echo "sample" > vacation-photo.jpg
echo "sample" > screenshot.png
echo "sample" > report.pdf
echo "sample" > resume.docx
echo "sample" > project.zip
echo "sample" > installer.exe
echo "sample" > notes.txt
echo "sample" > .DS_Store

# macOS/Linux:
touch vacation-photo.jpg screenshot.png report.pdf resume.docx project.zip installer.exe notes.txt .DS_Store
```

#### Create Test Configuration

Navigate back to the Fylum directory:

```bash
cd /path/to/fylum
```

Create `config.yaml` with this content:

```yaml
target_directories:
  - "~/FylumUATTest/test-downloads"

ignore_patterns:
  - ".DS_Store"
  - "*.tmp"

rename_format: "{date:%Y-%m-%d}_{original_filename}"

rules:
  - name: "Images"
    extensions: [".jpg", ".png"]
    destination: "~/FylumUATTest/organized/Images"
  
  - name: "Documents"
    extensions: [".pdf", ".docx", ".txt"]
    destination: "~/FylumUATTest/organized/Documents"
  
  - name: "Archives"
    extensions: [".zip"]
    destination: "~/FylumUATTest/organized/Archives"
  
  - name: "Installers"
    extensions: [".exe"]
    destination: "~/FylumUATTest/organized/Installers"
```

---

### Test Execution Script

Follow these test cases in order. **Document results for each test.**

---

#### **Test Case 1: Dry Run Mode**

**Command:**
```bash
python app.py clean --dry-run
```

**Expected Result:**
- Console shows "[DRY RUN MODE]" message
- Lists files that would be moved
- Shows expected destinations
- No actual file movement occurs
- No folders created

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 2: Actual Clean Operation**

**Command:**
```bash
python app.py clean
```

**Expected Result:**
- Files moved from `test-downloads` to organized folders
- Files renamed with date prefix (e.g., `2025-10-10_vacation-photo.jpg`)
- `.DS_Store` remains in `test-downloads` (ignored)
- Manifest files created:
  - `_fylum_index.md` (human-readable)
  - `_fylum_index.json` (machine-readable)

**Verification Steps:**
1. Check `~/FylumUATTest/organized/Images/` contains the JPG and PNG
2. Check `~/FylumUATTest/organized/Documents/` contains PDF, DOCX, TXT
3. Check filenames have date prefixes
4. Open `_fylum_index.md` and verify contents

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 3: Undo Operation**

**Command:**
```bash
python app.py undo
```

**Expected Result:**
- Files moved back to `test-downloads` with original names
- Original file structure restored
- Manifest updated (last run removed)

**Verification Steps:**
1. Check all files back in `test-downloads`
2. Verify original filenames (no date prefix)

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 4: Double Undo (Edge Case)**

**Command:**
```bash
python app.py undo
```

**Expected Result:**
- Message: "No previous run found to undo."
- No errors or crashes
- No files affected

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 5: Empty Directory Handling**

**Setup:**
```bash
rm ~/FylumUATTest/test-downloads/*
# Or manually delete all files in test-downloads
```

**Command:**
```bash
python app.py clean --dry-run
```

**Expected Result:**
- Clear message about no files found
- Helpful suggestions (empty directories, no matches, etc.)
- Graceful exit without errors

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 6: Pytest Test Suite**

**Command:**
```bash
pytest --maxfail=1 --disable-warnings -v
```

**Expected Result:**
- 23+ tests pass
- 0-1 tests skipped (symlink test on Windows is OK)
- No import errors
- No critical failures

**Status:** [ ] Pass [ ] Fail

**Number of Tests Passed:** ______ / ______

**Notes:**
___________________________________________________________________________

---

#### **Test Case 7: Special Characters in Filenames**

**Setup:**
```bash
cd ~/FylumUATTest/test-downloads
# Create files with special characters
echo "test" > "file with spaces.jpg"
echo "test" > "file-with-dashes.jpg"
echo "test" > "file_with_underscores.jpg"
```

**Command:**
```bash
python app.py clean
```

**Expected Result:**
- All files processed successfully
- No encoding errors
- Files moved to correct destinations

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

#### **Test Case 8: Duplicate Filename Handling**

**Setup:**
```bash
# Run clean once to organize files
python app.py clean

# Create duplicate file in source
echo "new" > ~/FylumUATTest/test-downloads/vacation-photo.jpg

# Run clean again
python app.py clean
```

**Expected Result:**
- Original file remains as `YYYY-MM-DD_vacation-photo.jpg`
- New file saved as `YYYY-MM-DD_vacation-photo_1.jpg`
- No overwriting occurs

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

## Creating an Execution Report

### Report Template

Create a file named `rX.X.X-test-execution-uat-run-N.md` where:
- `X.X.X` is the version (e.g., `1.0.0`)
- `N` is the run number (e.g., `1`, `2`)

Example: `r1.0.0-test-execution-uat-run-2.md`

### Report Structure

```markdown
# Fylum UAT Test Execution Report (Run N)

**Test Run Details**
- **Run by:** [Your Name/Team]
- **Test Run Start Datetime:** [Date and Time]
- **Test Run End Datetime:** [Date and Time]
- **Test Run Branch/Tag:** [e.g., v1.0.0-rc2]
- **Test Run Environment:** [OS, Python Version, Environment Details]

---

## Tests Executed

### 1. [Test Case Name]
- **Command:** [Command executed]
- **Result:** Pass / Fail
- **Details:** [Brief description of outcome]

[Repeat for each test case]

---

## Bugs/Issues Identified

- **Issue Title:**
  - Description: [What went wrong]
  - Steps to Reproduce: [How to recreate the issue]
  - Expected Behavior: [What should happen]
  - Actual Behavior: [What actually happened]
  - Severity: Critical / High / Medium / Low

[List all issues found]

---

## Suggestions

- [Any improvements or UX feedback]

---

## Summary

[Overall assessment: Ready for release? Critical blockers? General feedback]
```

### Example Report

See `tests/test-execution-reports/r1.0.0-test-execution-uat-run-2.md` for a complete example.

---

## Submitting Your Report

### Option 1: GitHub (Preferred)

1. **Fork the repository** (if you don't have write access)
2. **Create a new branch:**
   ```bash
   git checkout -b uat-report-[yourname]-[date]
   ```

3. **Add your report:**
   ```bash
   # Create report in tests/test-execution-reports/
   git add tests/test-execution-reports/rX.X.X-test-execution-uat-run-N.md
   git commit -m "Add UAT test execution report for vX.X.X-rcN"
   git push origin uat-report-[yourname]-[date]
   ```

4. **Create Pull Request** to the `uat/vX.X.X` branch

### Option 2: Email

Send your report to the development team at the designated email address with:
- Subject: `UAT Report - Fylum vX.X.X-rcN`
- Attach your `.md` report file
- Optionally include screenshots or logs

### Option 3: Issue Tracker

Create a new issue in GitHub with:
- Title: `[UAT Report] vX.X.X-rcN Test Results`
- Label: `uat`, `testing`
- Paste your report content

---

## Cleanup

After testing, you can clean up:

```bash
# Deactivate virtual environment
deactivate

# Remove test workspace
rm -rf ~/FylumUATTest

# Optional: Remove Fylum clone if done testing
# cd ..
# rm -rf fylum
```

---

## Troubleshooting

### Python not found
- Ensure Python 3.8+ is installed
- Windows: Check "Add Python to PATH" during installation
- Try `python3` instead of `python`

### Virtual environment activation fails
- Windows: Run as Administrator or change execution policy:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Import errors in tests
- Ensure you've installed dev dependencies: `pip install -r requirements-dev.txt`
- Verify you're in the correct directory with activated venv

### Git checkout fails
- Ensure you're in a clean state: `git status`
- Stash changes if needed: `git stash`
- Fetch latest tags: `git fetch --tags`

---

## Contact

- **Questions:** Open an issue on GitHub with label `question`
- **Urgent Issues:** Contact development team directly
- **Documentation:** See README.md and AGENTS.md

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Activate venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Run Fylum
python app.py clean --dry-run
python app.py clean
python app.py undo

# Run tests
pytest --maxfail=1 --disable-warnings -v

# Check version/tag
git describe --tags
```

### File Locations

- **Fylum repo:** `/path/to/fylum/`
- **Test workspace:** `~/FylumUATTest/`
- **Test files:** `~/FylumUATTest/test-downloads/`
- **Organized files:** `~/FylumUATTest/organized/`
- **Manifests:** `_fylum_index.md`, `_fylum_index.json` (in repo root)
- **Reports:** `tests/test-execution-reports/`

---

**Thank you for testing Fylum! Your feedback helps make it better.** 🙏
