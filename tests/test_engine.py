
import os
from pathlib import Path
import pytest
from src.config import Config, Rule
from src.engine import RuleEngine

@pytest.fixture
def create_test_files(tmp_path: Path):
    """Creates a temporary directory structure with files for testing."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "image1.jpg").touch()
    (test_dir / "image2.png").touch()
    (test_dir / "document1.txt").touch()
    (test_dir / "unmatched.pdf").touch()
    (test_dir / "ignored.txt").touch()
    return test_dir

@pytest.fixture
def test_config(create_test_files) -> Config:
    """Provides a basic config for testing."""
    return Config(
        target_directories=[str(create_test_files)],
        rules=[
            Rule(name="Images", extensions=[".jpg", ".png"], destination=str(create_test_files / "Images")),
            Rule(name="Docs", extensions=[".txt"], destination=str(create_test_files / "Docs")),
        ],
        ignore_patterns=["ignored.txt"]
    )

def test_engine_initialization(test_config: Config):
    """Tests that the RuleEngine can be initialized."""
    engine = RuleEngine(config=test_config)
    assert engine.config == test_config
    assert not engine.dry_run

def test_engine_identifies_actions(test_config: Config, create_test_files):
    """Tests that the engine correctly identifies file operations."""
    engine = RuleEngine(config=test_config)
    actions = engine.process_directories()

    # We expect 3 actions: image1.jpg, image2.png, document1.txt
    assert len(actions) == 3

    # Convert actions to a dictionary for easier lookup
    actions_dict = {action[0].name: action for action in actions}

    # Check image1.jpg
    assert "image1.jpg" in actions_dict
    source_path, dest_path = actions_dict["image1.jpg"]
    assert source_path.name == "image1.jpg"
    assert dest_path.name == "image1.jpg"
    assert dest_path.parent.name == "Images"

    # Check document1.txt
    assert "document1.txt" in actions_dict
    source_path, dest_path = actions_dict["document1.txt"]
    assert source_path.name == "document1.txt"
    assert dest_path.parent.name == "Docs"

    # Check that unmatched and ignored files are not in actions
    assert "unmatched.pdf" not in actions_dict
    assert "ignored.txt" not in actions_dict

