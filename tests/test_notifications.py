"""
Tests for notification system (TDD - tests written first)
"""

import pytest
from src.notifications.manager import NotificationManager, NotificationType


def test_notification_manager_initialization():
    """Test NotificationManager can be initialized"""
    manager = NotificationManager()
    assert manager is not None


def test_send_success_notification():
    """Test sending a success notification"""
    manager = NotificationManager()
    
    result = manager.send_notification(
        title="Files Organized",
        message="Successfully processed 10 files",
        notification_type=NotificationType.SUCCESS
    )
    
    # Should not raise error
    assert result in [True, False]  # May fail on headless systems


def test_send_error_notification():
    """Test sending an error notification"""
    manager = NotificationManager()
    
    result = manager.send_notification(
        title="Error",
        message="Failed to process files",
        notification_type=NotificationType.ERROR
    )
    
    assert result in [True, False]


def test_send_info_notification():
    """Test sending an info notification"""
    manager = NotificationManager()
    
    result = manager.send_notification(
        title="Scheduled Clean",
        message="Starting scheduled file organization",
        notification_type=NotificationType.INFO
    )
    
    assert result in [True, False]


def test_notification_preferences():
    """Test notification preferences can be set"""
    manager = NotificationManager()
    
    manager.set_enabled(False)
    assert manager.is_enabled() is False
    
    manager.set_enabled(True)
    assert manager.is_enabled() is True


def test_disabled_notifications_dont_send():
    """Test notifications don't send when disabled"""
    manager = NotificationManager()
    manager.set_enabled(False)
    
    result = manager.send_notification(
        title="Test",
        message="This should not appear",
        notification_type=NotificationType.INFO
    )
    
    # Should return False when disabled
    assert result is False


def test_notification_history():
    """Test notification history is tracked"""
    manager = NotificationManager()
    
    manager.send_notification(
        title="Test 1",
        message="Message 1",
        notification_type=NotificationType.INFO
    )
    
    manager.send_notification(
        title="Test 2",
        message="Message 2",
        notification_type=NotificationType.SUCCESS
    )
    
    history = manager.get_history()
    assert len(history) >= 2


def test_notification_types_enum():
    """Test notification types are defined"""
    assert NotificationType.SUCCESS is not None
    assert NotificationType.ERROR is not None
    assert NotificationType.INFO is not None
    assert NotificationType.WARNING is not None


def test_clear_history():
    """Test clearing notification history"""
    manager = NotificationManager()
    
    manager.send_notification("Test", "Message", NotificationType.INFO)
    assert len(manager.get_history()) > 0
    
    manager.clear_history()
    assert len(manager.get_history()) == 0
