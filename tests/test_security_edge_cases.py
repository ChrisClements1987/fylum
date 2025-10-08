
import pytest
import tempfile
import shutil
from pathlib import Path
from src.config import Config, Rule
from src.engine import RuleEngine
from src.processor import FileProcessor


@pytest.fixture
def security_workspace():
    """Creates a workspace for security testing."""
    workspace = Path(tempfile.mkdtemp())
    yield workspace
    shutil.rmtree(workspace)


def test_path_traversal_in_destination(security_workspace):
    """Test that path traversal attempts in destination are handled safely."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    (downloads / "test.jpg").write_text("data")
    
    sensitive_folder = security_workspace / "sensitive"
    sensitive_folder.mkdir()
    (sensitive_folder / "secret.txt").write_text("secret data")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(downloads / ".." / "sensitive")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    secret_file = sensitive_folder / "secret.txt"
    assert secret_file.exists()
    assert secret_file.read_text() == "secret data"
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_empty_directory_handling(security_workspace):
    """Test behavior when target directory is empty."""
    empty_dir = security_workspace / "empty"
    empty_dir.mkdir()
    
    config = Config(
        target_directories=[str(empty_dir)],
        ignore_patterns=[],
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "dest")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    assert len(actions) == 0


def test_non_existent_directory(security_workspace):
    """Test behavior when target directory doesn't exist."""
    non_existent = security_workspace / "does_not_exist"
    
    config = Config(
        target_directories=[str(non_existent)],
        ignore_patterns=[],
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "dest")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    assert len(actions) == 0


def test_files_in_use_simulation(security_workspace):
    """Test handling of potential file permission issues."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    test_file = downloads / "locked.txt"
    test_file.write_text("data")
    
    if test_file.exists():
        test_file.chmod(0o444)
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Docs", extensions=[".txt"], destination=str(security_workspace / "Documents")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    
    try:
        processor.process_actions(actions)
        
        moved_file = security_workspace / "Documents" / "locked.txt"
        if moved_file.exists():
            moved_file.chmod(0o644)
    except PermissionError:
        pytest.skip("Permission test not applicable on this platform")
    finally:
        if test_file.exists():
            test_file.chmod(0o644)
        Path("_fylum_index.md").unlink(missing_ok=True)
        Path("_fylum_index.json").unlink(missing_ok=True)


def test_unicode_filename_handling(security_workspace):
    """Test handling of unicode characters in filenames."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    try:
        (downloads / "文件.jpg").write_text("chinese")
        (downloads / "файл.jpg").write_text("russian")
        (downloads / "αρχείο.jpg").write_text("greek")
        (downloads / "emoji😀.jpg").write_text("emoji")
    except (UnicodeEncodeError, OSError):
        pytest.skip("Unicode filenames not supported on this filesystem")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processed = processor.process_actions(actions)
    
    assert processed >= 1
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_very_long_filename(security_workspace):
    """Test handling of very long filenames."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    long_name = "a" * 200 + ".jpg"
    
    try:
        (downloads / long_name).write_text("data")
    except OSError:
        pytest.skip("Filesystem doesn't support this filename length")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processed = processor.process_actions(actions)
    
    assert processed == 1
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_symlink_handling(security_workspace):
    """Test behavior with symbolic links."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    real_file = downloads / "real.jpg"
    real_file.write_text("real data")
    
    link_file = downloads / "link.jpg"
    
    try:
        link_file.symlink_to(real_file)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks not supported on this platform")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_deeply_nested_directory_structure(security_workspace):
    """Test handling of deeply nested directories."""
    deep_path = security_workspace / "a" / "b" / "c" / "d" / "e" / "f" / "g"
    deep_path.mkdir(parents=True)
    
    (deep_path / "deep.jpg").write_text("deep file")
    
    config = Config(
        target_directories=[str(security_workspace)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    assert len(actions) >= 1
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    pictures = security_workspace / "Pictures"
    assert (pictures / "deep.jpg").exists()
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_case_insensitive_extension_matching(security_workspace):
    """Test that file extensions are matched case-insensitively."""
    downloads = security_workspace / "Downloads"
    downloads.mkdir()
    
    (downloads / "file1.JPG").write_text("uppercase")
    (downloads / "file2.jpg").write_text("lowercase")
    (downloads / "file3.JpG").write_text("mixedcase")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(security_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    assert len(actions) == 3
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processed = processor.process_actions(actions)
    
    assert processed == 3
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)
