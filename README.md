# Fylum 📁

A smart file organizer CLI tool that automatically organizes your files based on customizable rules.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

## ✨ Features

- **🎯 Smart File Organization**: Automatically categorize and move files based on type, extension, or custom rules
- **📝 Customizable Rules**: Define your own organization patterns via YAML configuration
- **🔄 Rename Files**: Apply consistent naming patterns with date prefixes
- **📊 Index Manifest**: Track all file movements with detailed logs
- **↩️ Undo Support**: Revert the last organization operation
- **🔍 Dry Run Mode**: Preview changes before applying them
- **🛡️ Safe Operations**: Built-in duplicate handling and path safety checks

## 🚀 Quick Start

### Installation

#### Option 1: Install from source

```bash
git clone https://github.com/ChrisClements1987/fylum.git
cd fylum
pip install -r requirements.txt
```

#### Option 2: Install as package

```bash
pip install -e .
```

#### Option 3: Download standalone executable

Download the latest release from the [Releases](https://github.com/ChrisClements1987/fylum/releases) page.

### Basic Usage

1. **Create a configuration file** (first run will create a default `config.yaml`):

```bash
python app.py clean
```

2. **Preview what would be organized** (dry run):

```bash
python app.py clean --dry-run
```

3. **Organize your files**:

```bash
python app.py clean
```

4. **Undo the last operation**:

```bash
python app.py undo
```

## 📖 Configuration

Fylum uses a `config.yaml` file to define how files should be organized. Here's an example:

```yaml
target_directories:
  - "~/Downloads"
  - "~/Desktop"

ignore_patterns:
  - ".DS_Store"
  - "*.tmp"
  - "~$*"

rename_format: "{date:%Y-%m-%d}_{original_filename}"

rules:
  - name: "Images"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    destination: "~/Pictures/Fylum/Images"
  
  - name: "Documents"
    extensions: [".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md"]
    destination: "~/Documents/Fylum/Documents"
  
  - name: "Archives"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz"]
    destination: "~/Documents/Fylum/Archives"
  
  - name: "Installers"
    extensions: [".exe", ".msi", ".dmg"]
    destination: "~/Documents/Fylum/Installers"
```

### Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `target_directories` | Directories to scan for files | `["~/Downloads"]` |
| `ignore_patterns` | File patterns to skip | `["*.tmp", ".DS_Store"]` |
| `rename_format` | Template for renaming files | `"{date:%Y-%m-%d}_{original_filename}"` |
| `rules` | Organization rules (see below) | See example above |

### Rule Configuration

Each rule defines how files should be categorized:

- **name**: Descriptive name for the rule
- **extensions**: List of file extensions to match (case-insensitive)
- **destination**: Where matching files should be moved

### Rename Format Variables

- `{date}`: File modification date (supports Python strftime formatting)
- `{original_filename}`: Original filename without extension

Examples:
- `"{date:%Y-%m-%d}_{original_filename}"` → `2024-03-15_vacation-photo.jpg`
- `"{date:%Y%m%d}_{original_filename}"` → `20240315_vacation-photo.jpg`
- `"{original_filename}"` → `vacation-photo.jpg` (no renaming)

## 🎯 Usage Examples

### Organize Downloads Folder

```bash
# Preview what would happen
python app.py clean --dry-run

# Actually organize files
python app.py clean
```

### Organize Multiple Folders

Update your `config.yaml`:

```yaml
target_directories:
  - "~/Downloads"
  - "~/Desktop"
  - "~/Documents/Unsorted"
```

Then run:

```bash
python app.py clean
```

### Custom File Categories

Add custom rules to `config.yaml`:

```yaml
rules:
  - name: "Videos"
    extensions: [".mp4", ".avi", ".mkv", ".mov"]
    destination: "~/Videos/Organized"
  
  - name: "Audio"
    extensions: [".mp3", ".wav", ".flac", ".aac"]
    destination: "~/Music/Organized"
  
  - name: "Code"
    extensions: [".py", ".js", ".java", ".cpp", ".rs"]
    destination: "~/Code/Snippets"
```

### Undo Last Operation

If you need to revert the last organization:

```bash
python app.py undo
```

This will:
- Move all files back to their original locations
- Restore original filenames
- Update the manifest

## 📊 Index Manifest

Fylum creates two manifest files to track operations:

### `_fylum_index.md`
Human-readable Markdown table:

```markdown
## Fylum Run - 2024-03-15 14:30:22

| Original Path | New Path |
|---------------|----------|
| /Users/chris/Downloads/photo.jpg | /Users/chris/Pictures/2024-03-15_photo.jpg |
```

### `_fylum_index.json`
Machine-readable JSON format:

```json
[
  {
    "timestamp": "2024-03-15T14:30:22",
    "actions": [
      {
        "source": "/Users/chris/Downloads/photo.jpg",
        "destination": "/Users/chris/Pictures/2024-03-15_photo.jpg"
      }
    ]
  }
]
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/ChrisClements1987/fylum.git
cd fylum
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_integration.py -v
```

### Build Standalone Executable

```bash
python build_executable.py
```

The executable will be created in the `dist/` directory.

## 🧪 Testing

Fylum has comprehensive test coverage:

- **Unit Tests**: Core functionality (config, engine, processor)
- **Integration Tests**: End-to-end workflows
- **Security Tests**: Path traversal, permissions, edge cases
- **UAT Tests**: Manual testing guide in `UAT_TEST_PLAN.md`

Run the test suite:

```bash
pytest tests/ -v
```

## 🔒 Security

Fylum implements several security measures:

- ✅ Path traversal prevention
- ✅ Safe file permission handling
- ✅ Duplicate filename protection
- ✅ Unicode and special character support
- ✅ Read-only file detection

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features.

### V1.0.0 (Current)
- ✅ CLI tool with dry-run mode
- ✅ YAML configuration
- ✅ Smart file renaming
- ✅ Index manifest
- ✅ Undo functionality
- 🔄 Standalone executable

### V2.0.0 (Planned)
- GUI application
- Interactive approval mode
- Scheduled operations
- System notifications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/ChrisClements1987/fylum/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ChrisClements1987/fylum/discussions)

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Pydantic](https://pydantic.dev/) - Data validation
- [PyYAML](https://pyyaml.org/) - YAML parsing

---

**Made with ❤️ by Chris Clements**
