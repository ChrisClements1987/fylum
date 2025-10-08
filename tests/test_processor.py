
import pytest
from pathlib import Path
from datetime import datetime
from src.processor import FileProcessor, FileAction
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


def test_apply_rename_format(temp_dir):
    test_file = temp_dir / "test_file.txt"
    test_file.write_text("test content")
    
    processor = FileProcessor(rename_format="{date:%Y-%m-%d}_{original_filename}")
    new_name = processor.apply_rename_format(test_file)
    
    today = datetime.now().strftime("%Y-%m-%d")
    assert new_name == f"{today}_test_file.txt"


def test_process_actions_dry_run(temp_dir):
    source_file = temp_dir / "source.txt"
    source_file.write_text("test")
    
    dest_dir = temp_dir / "destination"
    dest_file = dest_dir / "dest.txt"
    
    processor = FileProcessor(rename_format="{original_filename}", dry_run=True)
    actions = [(source_file, dest_file)]
    
    processed = processor.process_actions(actions)
    
    assert processed == 1
    assert source_file.exists()
    assert not dest_file.exists()
    assert len(processor.actions_log) == 1


def test_process_actions_real_move(temp_dir):
    source_file = temp_dir / "source.txt"
    source_file.write_text("test content")
    
    dest_dir = temp_dir / "destination"
    dest_file = dest_dir / "dest.txt"
    
    processor = FileProcessor(rename_format="{original_filename}", dry_run=False)
    actions = [(source_file, dest_file)]
    
    processed = processor.process_actions(actions)
    
    assert processed == 1
    assert not source_file.exists()
    assert (dest_dir / "source.txt").exists()


def test_handle_duplicate_filename(temp_dir):
    source_file = temp_dir / "source.txt"
    source_file.write_text("test")
    
    dest_dir = temp_dir / "destination"
    dest_dir.mkdir()
    existing_file = dest_dir / "source.txt"
    existing_file.write_text("existing")
    
    processor = FileProcessor(rename_format="{original_filename}", dry_run=False)
    actions = [(source_file, dest_dir / "dest.txt")]
    
    processed = processor.process_actions(actions)
    
    assert processed == 1
    assert (dest_dir / "source_1.txt").exists()
    assert existing_file.exists()
