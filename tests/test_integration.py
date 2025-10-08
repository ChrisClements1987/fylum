
import pytest
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from src.config import Config, Rule
from src.engine import RuleEngine
from src.processor import FileProcessor
from src.undo import UndoManager
import json


@pytest.fixture
def integration_workspace():
    """Creates a complete test workspace with files and config."""
    workspace = Path(tempfile.mkdtemp())
    
    downloads_dir = workspace / "Downloads"
    downloads_dir.mkdir()
    
    (downloads_dir / "photo1.jpg").write_text("fake image data")
    (downloads_dir / "photo2.png").write_text("fake image data")
    (downloads_dir / "report.pdf").write_text("fake pdf data")
    (downloads_dir / "document.docx").write_text("fake word doc")
    (downloads_dir / "archive.zip").write_text("fake zip data")
    (downloads_dir / "installer.exe").write_text("fake exe data")
    (downloads_dir / ".DS_Store").write_text("system file")
    (downloads_dir / "temp.tmp").write_text("temp file")
    
    yield workspace
    
    shutil.rmtree(workspace)


def test_end_to_end_clean_workflow(integration_workspace):
    """Test the complete clean workflow from detection to organization."""
    downloads = integration_workspace / "Downloads"
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[".DS_Store", "*.tmp"],
        rename_format="{date:%Y-%m-%d}_{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg", ".png"], destination=str(integration_workspace / "Pictures")),
            Rule(name="Documents", extensions=[".pdf", ".docx"], destination=str(integration_workspace / "Documents")),
            Rule(name="Archives", extensions=[".zip"], destination=str(integration_workspace / "Archives")),
            Rule(name="Installers", extensions=[".exe"], destination=str(integration_workspace / "Installers")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    assert len(actions) == 6
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processed = processor.process_actions(actions)
    
    assert processed == 6
    
    pictures_dir = integration_workspace / "Pictures"
    documents_dir = integration_workspace / "Documents"
    archives_dir = integration_workspace / "Archives"
    installers_dir = integration_workspace / "Installers"
    
    assert pictures_dir.exists()
    assert documents_dir.exists()
    assert archives_dir.exists()
    assert installers_dir.exists()
    
    today = datetime.now().strftime("%Y-%m-%d")
    assert (pictures_dir / f"{today}_photo1.jpg").exists()
    assert (pictures_dir / f"{today}_photo2.png").exists()
    assert (documents_dir / f"{today}_report.pdf").exists()
    assert (documents_dir / f"{today}_document.docx").exists()
    assert (archives_dir / f"{today}_archive.zip").exists()
    assert (installers_dir / f"{today}_installer.exe").exists()
    
    assert (downloads / ".DS_Store").exists()
    assert (downloads / "temp.tmp").exists()
    
    manifest_md = Path("_fylum_index.md")
    manifest_json = Path("_fylum_index.json")
    assert manifest_md.exists()
    assert manifest_json.exists()
    
    manifest_md.unlink()
    manifest_json.unlink()


def test_dry_run_mode(integration_workspace):
    """Test that dry run mode doesn't actually move files."""
    downloads = integration_workspace / "Downloads"
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[".DS_Store", "*.tmp"],
        rules=[
            Rule(name="Images", extensions=[".jpg", ".png"], destination=str(integration_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=True)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format="{original_filename}", dry_run=True)
    processed = processor.process_actions(actions)
    
    assert processed == 2
    
    assert (downloads / "photo1.jpg").exists()
    assert (downloads / "photo2.png").exists()
    
    pictures_dir = integration_workspace / "Pictures"
    assert not pictures_dir.exists()


def test_undo_workflow(integration_workspace):
    """Test that undo successfully reverts file operations."""
    downloads = integration_workspace / "Downloads"
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(integration_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    assert (integration_workspace / "Pictures" / "photo1.jpg").exists()
    assert not (downloads / "photo1.jpg").exists()
    
    undo_manager = UndoManager()
    reverted = undo_manager.revert_last_run()
    
    assert reverted == 1
    assert (downloads / "photo1.jpg").exists()
    assert not (integration_workspace / "Pictures" / "photo1.jpg").exists()
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_duplicate_filename_handling(integration_workspace):
    """Test that duplicate filenames are handled correctly."""
    downloads = integration_workspace / "Downloads"
    pictures = integration_workspace / "Pictures"
    pictures.mkdir()
    
    (pictures / "photo1.jpg").write_text("existing file")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(pictures)),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    assert (pictures / "photo1.jpg").exists()
    assert (pictures / "photo1_1.jpg").exists()
    
    original_content = (pictures / "photo1.jpg").read_text()
    new_content = (pictures / "photo1_1.jpg").read_text()
    
    assert original_content == "existing file"
    assert new_content == "fake image data"
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_special_characters_in_filenames(integration_workspace):
    """Test handling of filenames with special characters."""
    downloads = integration_workspace / "Downloads"
    
    (downloads / "file with spaces.jpg").write_text("data")
    (downloads / "file-with-dashes.jpg").write_text("data")
    (downloads / "file_with_underscores.jpg").write_text("data")
    (downloads / "file (with) parens.jpg").write_text("data")
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(integration_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processed = processor.process_actions(actions)
    
    assert processed == 5
    
    pictures = integration_workspace / "Pictures"
    assert (pictures / "file with spaces.jpg").exists()
    assert (pictures / "file-with-dashes.jpg").exists()
    assert (pictures / "file_with_underscores.jpg").exists()
    assert (pictures / "file (with) parens.jpg").exists()
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_manifest_format_and_structure(integration_workspace):
    """Test that manifest files are created with correct format."""
    downloads = integration_workspace / "Downloads"
    
    config = Config(
        target_directories=[str(downloads)],
        ignore_patterns=[],
        rename_format="{original_filename}",
        rules=[
            Rule(name="Images", extensions=[".jpg"], destination=str(integration_workspace / "Pictures")),
        ]
    )
    
    engine = RuleEngine(config=config, dry_run=False)
    actions = engine.process_directories()
    
    processor = FileProcessor(rename_format=config.rename_format, dry_run=False)
    processor.process_actions(actions)
    
    manifest_json = Path("_fylum_index.json")
    assert manifest_json.exists()
    
    with open(manifest_json, "r") as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == 1
    
    run = data[0]
    assert "timestamp" in run
    assert "actions" in run
    assert len(run["actions"]) == 1
    
    action = run["actions"][0]
    assert "source" in action
    assert "destination" in action
    
    manifest_md = Path("_fylum_index.md")
    assert manifest_md.exists()
    
    content = manifest_md.read_text()
    assert "## Fylum Run" in content
    assert "| Original Path | New Path |" in content
    
    Path("_fylum_index.md").unlink()
    Path("_fylum_index.json").unlink()
