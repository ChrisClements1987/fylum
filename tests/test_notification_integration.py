"""
Tests for notification integration with operations (TDD)
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from src.processor import FileProcessor
from src.notifications.manager import NotificationManager, NotificationType


@pytest.fixture
def temp_workspace():
    """Create temp workspace"""
    workspace = Path(tempfile.mkdtemp())
    yield workspace
    shutil.rmtree(workspace)


def test_processor_sends_notification_on_success(temp_workspace):
    """Test FileProcessor sends success notification after processing"""
    downloads = temp_workspace / "downloads"
    downloads.mkdir()
    (downloads / "test.jpg").write_text("test")
    
    dest = temp_workspace / "pictures"
    
    notifier = NotificationManager()
    processor = FileProcessor(
        rename_format="{original_filename}",
        dry_run=False,
        notification_manager=notifier
    )
    
    actions = [(downloads / "test.jpg", dest / "test.jpg")]
    processed = processor.process_actions(actions)
    
    assert processed == 1
    # Should have sent a notification
    history = notifier.get_history()
    assert len(history) > 0
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_processor_with_notification_manager_optional(temp_workspace):
    """Test FileProcessor works without notification manager (backward compatible)"""
    downloads = temp_workspace / "downloads"
    downloads.mkdir()
    (downloads / "test.jpg").write_text("test")
    
    dest = temp_workspace / "pictures"
    
    # No notification manager provided
    processor = FileProcessor(
        rename_format="{original_filename}",
        dry_run=False,
        notification_manager=None
    )
    
    actions = [(downloads / "test.jpg", dest / "test.jpg")]
    processed = processor.process_actions(actions)
    
    # Should work fine without notifications
    assert processed == 1
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_scheduler_sends_notification_after_run():
    """Test scheduler sends notification after scheduled clean"""
    from src.scheduler.manager import ScheduleManager
    from src.config import create_default_config
    
    # Ensure config exists
    config_path = Path("config.yaml")
    if not config_path.exists():
        create_default_config()
    
    manager = ScheduleManager()
    manager.notification_manager = NotificationManager()
    
    # Execute a clean (simulated scheduled run)
    manager._execute_clean()
    
    # Should have notification in history
    history = manager.notification_manager.get_history()
    # Should have sent a notification (either success or info)
    assert len(history) > 0
    
    Path("_fylum_index.md").unlink(missing_ok=True)
    Path("_fylum_index.json").unlink(missing_ok=True)


def test_dry_run_does_not_send_notification(temp_workspace):
    """Test dry run doesn't send completion notifications"""
    downloads = temp_workspace / "downloads"
    downloads.mkdir()
    (downloads / "test.jpg").write_text("test")
    
    dest = temp_workspace / "pictures"
    
    notifier = NotificationManager()
    processor = FileProcessor(
        rename_format="{original_filename}",
        dry_run=True,
        notification_manager=notifier
    )
    
    actions = [(downloads / "test.jpg", dest / "test.jpg")]
    processor.process_actions(actions)
    
    # Dry run shouldn't send completion notifications
    history = notifier.get_history()
    # History may be empty or contain info notifications, but not success
    assert all(n.notification_type != NotificationType.SUCCESS for n in history)
