
import os
import yaml
import pytest
from src.config import load_config, create_default_config, CONFIG_FILE_PATH, DEFAULT_CONFIG, Config

@pytest.fixture(autouse=True)
def manage_config_file():
    """Fixture to ensure the config file is cleaned up before and after each test."""
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
    
    yield
    
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)

def test_load_config_creates_default_when_missing(capsys):
    """Tests that load_config creates a default file if it doesn't exist."""
    # Expect SystemExit because the function exits after creating the file
    with pytest.raises(SystemExit):
        load_config()
    
    # Check that the file was created
    assert os.path.exists(CONFIG_FILE_PATH)
    
    # Check that the content is the same as the default config
    with open(CONFIG_FILE_PATH, "r") as f:
        created_config = yaml.safe_load(f)
    assert created_config == DEFAULT_CONFIG

    # Check that the correct messages were printed to stdout
    captured = capsys.readouterr()
    assert "Configuration file not found" in captured.out
    assert "Creating a default config.yaml" in captured.out

def test_load_config_loads_existing_file():
    """Tests that load_config correctly loads an existing, valid config file."""
    # Create a dummy config file
    create_default_config()
    
    # Load the config
    config = load_config()
    
    # Assert that the loaded config is a valid Config object
    assert isinstance(config, Config)
    assert config.rename_format == DEFAULT_CONFIG['rename_format']
    assert len(config.rules) == len(DEFAULT_CONFIG['rules'])

def test_load_config_exits_on_invalid_file(capsys):
    """Tests that load_config exits if the config file is invalid."""
    # Create an invalid config file (e.g., missing a required field)
    invalid_config = {"rules": [{"name": "Incomplete Rule"}]}
    with open(CONFIG_FILE_PATH, "w") as f:
        yaml.dump(invalid_config, f)

    # Expect SystemExit because the function exits on validation error
    with pytest.raises(SystemExit):
        load_config()
    
    # Check that an error message was printed
    captured = capsys.readouterr()
    assert "Error loading or parsing configuration" in captured.out

