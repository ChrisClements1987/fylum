
import yaml
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# --- Pydantic Models for Configuration Validation ---

class Rule(BaseModel):
    """Defines a rule for classifying and moving a file."""
    name: str
    extensions: List[str]
    destination: str

class Config(BaseModel):
    """Top-level configuration model."""
    target_directories: List[str] = Field(default_factory=list)
    ignore_patterns: List[str] = Field(default_factory=list)
    rename_format: str = "{date:%Y-%m-%d}_{original_filename}"
    rules: List[Rule] = Field(default_factory=list)

# --- Default Configuration ---

DEFAULT_CONFIG = {
    'target_directories': [
        '~/Downloads',
        '~/Desktop'
    ],
    'ignore_patterns': [
        '.DS_Store',
        '*.tmp',
        '~$*',
    ],
    'rename_format': '{date:%Y-%m-%d}_{original_filename}',
    'rules': [
        {
            'name': 'Images',
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'destination': '~/Pictures/Fylum/Images'
        },
        {
            'name': 'Documents',
            'extensions': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md', '.csv'],
            'destination': '~/Documents/Fylum/Documents'
        },
        {
            'name': 'Archives',
            'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'destination': '~/Documents/Fylum/Archives'
        },
        {
            'name': 'Installers',
            'extensions': ['.exe', '.msi', '.dmg'],
            'destination': '~/Documents/Fylum/Installers'
        }
    ]
}

CONFIG_FILE_PATH = "config.yaml"

# --- Configuration Management Functions ---

def create_default_config() -> None:
    """Creates a default config.yaml file."""
    with open(CONFIG_FILE_PATH, "w") as f:
        yaml.dump(DEFAULT_CONFIG, f, sort_keys=False)

def load_config() -> Config:
    """Loads and validates the configuration from config.yaml."""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config_data = yaml.safe_load(f)
        return Config(**config_data)
    except FileNotFoundError:
        print(f"Configuration file not found at '{CONFIG_FILE_PATH}'.")
        print("Creating a default config.yaml for you...")
        create_default_config()
        print("Please review the default settings in config.yaml before running a clean operation.")
        # Exit gracefully after creating the file
        raise SystemExit()
    except Exception as e:
        print(f"Error loading or parsing configuration: {e}")
        # Exit gracefully on validation errors
        raise SystemExit()

