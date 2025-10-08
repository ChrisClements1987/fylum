# Fylum - AI Agent Context

This document provides context for AI coding assistants working on the Fylum project.

## Project Overview

Fylum is a smart file organizer CLI tool built with Python. It helps users automatically organize files based on customizable rules defined in YAML configuration.

**Repository**: https://github.com/ChrisClements1987/fylum

## Tech Stack

- **Language**: Python 3.8+
- **CLI Framework**: Typer
- **Configuration**: PyYAML + Pydantic for validation
- **Testing**: pytest, pytest-cov, pytest-mock
- **Packaging**: PyInstaller for standalone executables

## Project Structure

```
fylum/
├── app.py                  # Main CLI entry point
├── src/
│   ├── config.py          # Configuration loading & validation
│   ├── engine.py          # RuleEngine - file matching logic
│   ├── processor.py       # FileProcessor - file operations
│   └── undo.py            # UndoManager - revert operations
├── tests/
│   ├── test_config.py     # Config unit tests
│   ├── test_engine.py     # Engine unit tests
│   ├── test_processor.py  # Processor unit tests
│   ├── test_integration.py        # Integration tests
│   └── test_security_edge_cases.py # Security & edge case tests
├── architecture/          # ADRs and design docs
├── config.yaml           # User configuration file (gitignored)
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── setup.py             # Package configuration
├── build_executable.py  # Build script for executable
└── README.md           # User documentation
```

## Core Components

### 1. Config Module (`src/config.py`)
- **Purpose**: Load and validate YAML configuration
- **Key Classes**:
  - `Config`: Main configuration model (Pydantic)
  - `Rule`: Individual file organization rule (Pydantic)
- **Key Functions**:
  - `load_config()`: Loads config.yaml, creates default if missing
  - `create_default_config()`: Generates default config.yaml

### 2. Rule Engine (`src/engine.py`)
- **Purpose**: Scan directories and match files to rules
- **Key Class**: `RuleEngine`
- **Key Method**: `process_directories()` → Returns list of (source, destination) tuples
- **Behavior**:
  - Recursively scans target directories
  - Matches files against rules by extension (case-insensitive)
  - Respects ignore patterns
  - First matching rule wins

### 3. File Processor (`src/processor.py`)
- **Purpose**: Execute file operations (move/rename)
- **Key Classes**:
  - `FileProcessor`: Handles file operations
  - `FileAction`: Represents a single file operation
- **Key Methods**:
  - `apply_rename_format()`: Applies date/name templates
  - `process_actions()`: Executes or simulates file operations
  - `_write_manifest()`: Creates index files
- **Features**:
  - Dry run support
  - Duplicate filename handling (appends _1, _2, etc.)
  - Creates both .md and .json manifest files

### 4. Undo Manager (`src/undo.py`)
- **Purpose**: Revert file operations
- **Key Class**: `UndoManager`
- **Key Methods**:
  - `get_last_run()`: Reads last operation from manifest
  - `revert_last_run()`: Moves files back to original locations
  - `_remove_last_run()`: Updates manifest after undo

### 5. CLI (`app.py`)
- **Commands**:
  - `clean [--dry-run]`: Organize files
  - `undo`: Revert last operation
- **Framework**: Typer for CLI interface

## Common Development Tasks

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_integration.py -v

# With coverage
pytest --cov=src tests/
```

### Building Executable

```bash
python build_executable.py
```

The executable will be in `dist/fylum.exe` (Windows) or `dist/fylum` (macOS/Linux).

### Running the App (Development)

```bash
# Using Python
python app.py clean --dry-run
python app.py clean
python app.py undo

# Using installed package
fylum clean --dry-run
```

## Code Conventions

### Style
- **Formatting**: Follow PEP 8
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Include docstrings for classes and public methods
- **Imports**: Group imports (stdlib, third-party, local)

### Testing
- **Coverage**: Aim for >80% code coverage
- **Test Structure**: Arrange-Act-Assert pattern
- **Fixtures**: Use pytest fixtures for common setups
- **Naming**: `test_<functionality>_<scenario>`

### Error Handling
- **User-Facing Errors**: Use `typer.echo()` for messages
- **Graceful Failures**: Exit with `raise typer.Exit()` or `raise SystemExit()`
- **Validation**: Use Pydantic for config validation

## Key Design Decisions

See `architecture/` for full ADRs:

1. **CLI-First Approach** (ADR001): Build CLI before GUI to establish core logic
2. **YAML Configuration**: Human-readable, easy to version control
3. **Pydantic Validation**: Strong typing and validation for config
4. **Dual Manifest Format**: Both .md (human) and .json (machine) for flexibility
5. **Dry Run by Default**: Safety-first approach for user confidence

## Testing Strategy

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test end-to-end workflows
3. **Security Tests**: Path traversal, permissions, edge cases
4. **UAT**: Manual testing via `UAT_TEST_PLAN.md`

## Branching Strategy

- `master`: Main development branch
- `uat/v*.*.* `: UAT testing branches (stable snapshots)
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches

## Common Issues & Solutions

### Issue: PyInstaller build fails
**Solution**: Check hidden imports in `build_executable.py` - may need to add modules

### Issue: Config not loading
**Solution**: Ensure config.yaml is in working directory, check YAML syntax

### Issue: Files not matching rules
**Solution**: Extensions are case-insensitive but must include the dot (`.jpg` not `jpg`)

### Issue: Permission errors on Windows
**Solution**: May need to handle read-only files, check file permissions before moving

## Roadmap Context

**Current Version**: V1.0.0 (CLI Foundation)
- Focus: Robust CLI tool with core features
- Next: Complete standalone executable packaging

**Next Version**: V2.0.0 (GUI Experience)
- Focus: Desktop GUI application
- Features: Interactive mode, scheduling, notifications

See `ROADMAP.md` for full details.

## Important Notes for AI Assistants

1. **Config File Location**: `config.yaml` is gitignored - it's user-specific
2. **Manifest Files**: `_fylum_index.*` files are gitignored - generated per run
3. **Test Isolation**: Tests create temp directories and clean up manifests
4. **Windows Paths**: Handle both forward and backslashes in paths
5. **Case Sensitivity**: File extensions matched case-insensitively
6. **Dry Run**: Always test with `--dry-run` first when adding new features

## Useful Commands Reference

```bash
# Development setup
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix
pip install -r requirements-dev.txt

# Testing
pytest -v
pytest --cov=src tests/ --cov-report=html

# Building
python build_executable.py

# Git workflow
git checkout -b feature/new-feature
# ... make changes ...
pytest  # Ensure tests pass
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

## Contact & Resources

- **GitHub**: https://github.com/ChrisClements1987/fylum
- **Issues**: https://github.com/ChrisClements1987/fylum/issues
- **Author**: Chris Clements
