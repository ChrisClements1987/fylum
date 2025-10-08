# Fylum V1.0.0 - User Acceptance Testing (UAT) Plan

## Overview
This document outlines the manual testing procedures for validating Fylum's functionality in real-world scenarios.

---

## Prerequisites

- Python virtual environment activated
- Fylum installed and accessible via `python app.py`
- Test folders and files prepared (see Setup section)

---

## Test Setup

### Create Test Environment

1. Create a test Downloads folder: `C:\TestFylum\Downloads` (or `~/TestFylum/Downloads` on macOS/Linux)
2. Create test files with the following:

```
TestFylum/
└── Downloads/
    ├── vacation-photo.jpg
    ├── screenshot.png
    ├── tax-document-2024.pdf
    ├── resume.docx
    ├── budget.xlsx
    ├── presentation.pptx
    ├── notes.txt
    ├── project-files.zip
    ├── game-installer.exe
    ├── .DS_Store (macOS only)
    ├── temp.tmp
    ├── file with spaces.jpg
    ├── file-with-émojis-😀.png
    ├── very_long_filename_that_exceeds_normal_length_expectations_for_testing_purposes_document.pdf
```

3. Create a custom `config.yaml`:

```yaml
target_directories:
  - "C:/TestFylum/Downloads"  # Adjust path for your OS

ignore_patterns:
  - ".DS_Store"
  - "*.tmp"
  - "~$*"

rename_format: "{date:%Y-%m-%d}_{original_filename}"

rules:
  - name: "Images"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    destination: "C:/TestFylum/Organized/Images"
  
  - name: "Documents"
    extensions: [".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"]
    destination: "C:/TestFylum/Organized/Documents"
  
  - name: "Archives"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz"]
    destination: "C:/TestFylum/Organized/Archives"
  
  - name: "Installers"
    extensions: [".exe", ".msi", ".dmg"]
    destination: "C:/TestFylum/Organized/Installers"
```

---

## Test Cases

### TC-001: Dry Run Mode
**Objective:** Verify that dry run mode previews operations without making changes

**Steps:**
1. Run: `python app.py clean --dry-run`
2. Observe console output
3. Check that files remain in `Downloads` folder
4. Verify no `Organized` folder is created
5. Verify no `_fylum_index.md` or `_fylum_index.json` files are created

**Expected Result:**
- Console shows "[DRY RUN MODE]" message
- Lists all files that would be moved
- No actual file operations occur
- All files remain in original location

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-002: Basic Clean Operation
**Objective:** Verify files are organized correctly

**Steps:**
1. Run: `python app.py clean`
2. Check console output
3. Navigate to `C:/TestFylum/Organized/` folders
4. Verify file locations and renamed filenames

**Expected Result:**
- Console shows successful processing message
- Images moved to `Organized/Images/` with date prefix
- Documents moved to `Organized/Documents/` with date prefix
- Archives moved to `Organized/Archives/` with date prefix
- Installers moved to `Organized/Installers/` with date prefix
- Ignored files (`.DS_Store`, `temp.tmp`) remain in Downloads
- All files renamed to format: `YYYY-MM-DD_original-filename.ext`

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-003: Index Manifest Creation
**Objective:** Verify manifest files are created correctly

**Steps:**
1. After running clean, check for `_fylum_index.md` and `_fylum_index.json`
2. Open `_fylum_index.md` and verify format
3. Open `_fylum_index.json` and verify structure

**Expected Result:**
- Both manifest files exist in the root directory
- `_fylum_index.md` contains:
  - Timestamp header
  - Table with "Original Path" and "New Path" columns
  - All file movements logged
- `_fylum_index.json` contains:
  - Array with one run object
  - Timestamp in ISO format
  - Actions array with source/destination for each file

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-004: Undo Functionality
**Objective:** Verify that undo reverts the last clean operation

**Steps:**
1. After a successful clean, run: `python app.py undo`
2. Check console output
3. Navigate to `Downloads` folder
4. Verify files are restored to original locations with original names

**Expected Result:**
- Console shows "Successfully reverted X files" message
- All files moved back to `Downloads` folder
- Files restored to original filenames (without date prefix)
- `Organized` folders become empty (or don't exist)
- Manifest files updated (last run removed)

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-005: Duplicate Filename Handling
**Objective:** Verify duplicate filenames are handled correctly

**Steps:**
1. Run clean operation
2. Copy a new file with same name to Downloads (e.g., `vacation-photo.jpg`)
3. Run clean operation again
4. Check the destination folder

**Expected Result:**
- Original file remains as `YYYY-MM-DD_vacation-photo.jpg`
- New file saved as `YYYY-MM-DD_vacation-photo_1.jpg`
- Both files exist without overwriting

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-006: Special Characters in Filenames
**Objective:** Verify files with special characters are handled correctly

**Steps:**
1. Ensure test files with spaces, dashes, emojis exist
2. Run clean operation
3. Verify all files are moved and renamed correctly

**Expected Result:**
- Files with spaces: Successfully moved and renamed
- Files with dashes/underscores: Successfully moved and renamed
- Files with unicode/emojis: Successfully moved and renamed (if OS supports)
- No errors in console

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-007: Empty Directories
**Objective:** Verify behavior when target directories are empty

**Steps:**
1. Create a new empty folder: `C:/TestFylum/EmptyFolder`
2. Add to `config.yaml` target_directories
3. Run clean operation

**Expected Result:**
- Console shows "No files found that match the rules"
- No errors occur
- Application exits gracefully

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-008: Invalid Configuration
**Objective:** Verify error handling for invalid config

**Steps:**
1. Modify `config.yaml` with invalid YAML syntax
2. Run clean operation
3. Observe error handling

**Expected Result:**
- Application shows clear error message
- Does not crash
- Suggests how to fix the issue

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-009: Missing Configuration File
**Objective:** Verify default config creation

**Steps:**
1. Delete or rename `config.yaml`
2. Run clean operation

**Expected Result:**
- Console shows "Configuration file not found" message
- Creates default `config.yaml` automatically
- Shows message to review settings before running
- Exits gracefully without performing operations

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-010: Large Volume Testing
**Objective:** Test performance with many files

**Steps:**
1. Create 500+ test files of various types
2. Run clean operation
3. Measure time taken
4. Verify all files processed correctly

**Expected Result:**
- All files processed without errors
- Reasonable performance (< 30 seconds for 500 files)
- Manifest correctly logs all operations

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-011: Nested Directories
**Objective:** Verify recursive scanning of subdirectories

**Steps:**
1. Create nested structure in Downloads:
   ```
   Downloads/
   ├── subfolder1/
   │   └── image.jpg
   └── subfolder2/
       └── document.pdf
   ```
2. Run clean operation

**Expected Result:**
- Files in subfolders are detected
- Files moved to appropriate organized folders
- Original subfolder structure not preserved (all files go to rule destination)

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-012: Read-Only Files (Security)
**Objective:** Test behavior with read-only files

**Steps:**
1. Create a file and set it to read-only
2. Run clean operation
3. Observe error handling

**Expected Result:**
- Application shows error message for read-only file
- Continues processing other files
- Does not crash

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-013: Path Traversal Prevention (Security)
**Objective:** Verify protection against malicious paths

**Steps:**
1. Modify `config.yaml` with paths like `../../sensitive-folder`
2. Run clean operation
3. Verify no files accessed outside intended scope

**Expected Result:**
- Application handles paths safely
- Does not allow access to parent directories via `../`
- Or shows appropriate error/warning

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-014: Multiple Undo Operations
**Objective:** Verify undo works for multiple sequential runs

**Steps:**
1. Run clean operation (Run 1)
2. Add more files to Downloads
3. Run clean operation (Run 2)
4. Run undo (should revert Run 2)
5. Run undo again (should revert Run 1)

**Expected Result:**
- First undo reverts Run 2 files only
- Second undo reverts Run 1 files only
- Manifest updated correctly after each undo

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

### TC-015: No Matching Rules
**Objective:** Verify behavior when files don't match any rules

**Steps:**
1. Add files with extensions not in rules (e.g., `.mkv`, `.mp3`)
2. Run clean operation

**Expected Result:**
- Console shows these files are not matched
- Files remain in Downloads folder
- No errors occur

**Status:** [ ] Pass [ ] Fail

**Notes:**
___________________________________________________________________________

---

## Test Summary

| Test Case | Status | Priority | Notes |
|-----------|--------|----------|-------|
| TC-001: Dry Run Mode | [ ] | High | |
| TC-002: Basic Clean | [ ] | High | |
| TC-003: Manifest Creation | [ ] | High | |
| TC-004: Undo Functionality | [ ] | High | |
| TC-005: Duplicate Filenames | [ ] | High | |
| TC-006: Special Characters | [ ] | Medium | |
| TC-007: Empty Directories | [ ] | Medium | |
| TC-008: Invalid Config | [ ] | Medium | |
| TC-009: Missing Config | [ ] | Medium | |
| TC-010: Large Volume | [ ] | Low | |
| TC-011: Nested Directories | [ ] | Medium | |
| TC-012: Read-Only Files | [ ] | Medium | |
| TC-013: Path Traversal | [ ] | High | Security |
| TC-014: Multiple Undo | [ ] | Medium | |
| TC-015: No Matching Rules | [ ] | Low | |

---

## Sign-Off

**Tester Name:** _____________________

**Date:** _____________________

**Overall Result:** [ ] Pass [ ] Fail

**Comments:**
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
