# Fylum v1.0.0 Release Notes

**Release Date:** October 10, 2025

## 🎉 Initial Release

Fylum v1.0.0 is a smart file organizer CLI tool that automatically organizes your files based on customizable rules.

## ✨ Features

### Core Functionality
- **🎯 Smart File Organization**: Automatically categorize and move files based on type, extension, or custom rules
- **📝 Customizable Rules**: Define your own organization patterns via YAML configuration
- **🔄 File Renaming**: Apply consistent naming patterns with date prefixes (e.g., `2025-10-10_vacation-photo.jpg`)
- **📊 Dual Manifest Tracking**: Both human-readable (.md) and machine-readable (.json) logs of all operations
- **↩️ Undo Support**: Revert the last organization operation with a single command
- **🔍 Dry Run Mode**: Preview changes before applying them
- **🛡️ Safe Operations**: Built-in duplicate handling, path safety checks, and permission handling

### Command Line Interface
- `fylum clean` - Organize files based on rules
- `fylum clean --dry-run` - Preview operations without making changes
- `fylum undo` - Revert last organization operation

### Configuration
- YAML-based configuration file (`config.yaml`)
- Customizable target directories
- Flexible ignore patterns
- Extensible rule system
- Custom rename format templates

### Quality Assurance
- ✅ 23 passing unit/integration tests
- ✅ Security and edge case testing
- ✅ Full UAT coverage
- ✅ Cross-platform support (Windows, macOS, Linux)

## 📦 Installation

### Option 1: Download Standalone Executable
Download `fylum.exe` (Windows) from the Assets below. No Python installation required!

### Option 2: Install from Source
```bash
git clone https://github.com/ChrisClements1987/fylum.git
cd fylum
pip install -r requirements.txt
python app.py --help
```

### Option 3: Install as Package
```bash
pip install -e .
fylum --help
```

## 🚀 Quick Start

1. **First run** (creates default config):
   ```bash
   fylum clean
   ```

2. **Edit `config.yaml`** to customize your rules

3. **Preview changes**:
   ```bash
   fylum clean --dry-run
   ```

4. **Organize your files**:
   ```bash
   fylum clean
   ```

5. **Undo if needed**:
   ```bash
   fylum undo
   ```

## 📖 Documentation

- **README.md** - Complete usage guide with examples
- **AGENTS.md** - AI assistant context and development guide
- **UAT_TEST_PLAN.md** - User acceptance testing procedures
- **ROADMAP.md** - Future development plans

## 🧪 Testing

Comprehensive test suite includes:
- Unit tests for all core modules
- Integration tests for end-to-end workflows
- Security tests (path traversal, permissions, unicode)
- Edge case handling
- Manual UAT validation

Run tests:
```bash
pytest tests/ -v
```

## 🔒 Security

- Path traversal prevention
- Safe file permission handling
- Duplicate filename protection
- Unicode and special character support
- Read-only file detection

## 🛠️ Technical Details

### Built With
- **Python 3.8+**
- **Typer** - CLI framework
- **Pydantic** - Data validation
- **PyYAML** - Configuration parsing
- **PyInstaller** - Executable packaging

### System Requirements
- Python 3.8 or higher (for source installation)
- Windows, macOS, or Linux
- Read/write access to target directories

## 📝 Example Configuration

```yaml
target_directories:
  - "~/Downloads"
  - "~/Desktop"

ignore_patterns:
  - ".DS_Store"
  - "*.tmp"

rename_format: "{date:%Y-%m-%d}_{original_filename}"

rules:
  - name: "Images"
    extensions: [".jpg", ".png", ".gif"]
    destination: "~/Pictures/Organized"
  
  - name: "Documents"
    extensions: [".pdf", ".docx", ".txt"]
    destination: "~/Documents/Organized"
```

## 🙏 Acknowledgments

Built with love by Chris Clements.

Special thanks to:
- Typer for the excellent CLI framework
- Pydantic for robust data validation
- The Python community

## 📄 License

MIT License - see LICENSE file for details

## 🐛 Known Issues

- Symlink handling is platform-dependent (test skipped on Windows)

## 🗺️ Roadmap

See ROADMAP.md for planned features:
- **V2.0.0**: GUI application with interactive mode and scheduling
- **Future**: Duplicate detection, plugin architecture, internationalization

## 💬 Support

- **Issues**: https://github.com/ChrisClements1987/fylum/issues
- **Discussions**: https://github.com/ChrisClements1987/fylum/discussions

---

**Made with ❤️ by Chris Clements**
