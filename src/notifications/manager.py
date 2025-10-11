"""
Notification system for Fylum V2.0.0
Cross-platform desktop notifications
"""

from enum import Enum
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass


class NotificationType(Enum):
    """Types of notifications"""
    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


@dataclass
class NotificationRecord:
    """Record of a sent notification"""
    title: str
    message: str
    notification_type: NotificationType
    timestamp: datetime


class NotificationManager:
    """Manages desktop notifications"""
    
    def __init__(self):
        self.enabled = True
        self.history: List[NotificationRecord] = []
        self._init_notifier()
    
    def _init_notifier(self):
        """Initialize the notification backend"""
        try:
            from plyer import notification
            self.notification = notification
            self.available = True
        except ImportError:
            self.notification = None
            self.available = False
    
    def send_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO
    ) -> bool:
        """Send a desktop notification"""
        # Add to history
        record = NotificationRecord(
            title=title,
            message=message,
            notification_type=notification_type,
            timestamp=datetime.now()
        )
        self.history.append(record)
        
        # Don't send if disabled
        if not self.enabled:
            return False
        
        # Check if plyer is available
        if not self.available or not self.notification:
            return False
        
        try:
            # Map notification type to app name for visual distinction
            app_name_prefix = {
                NotificationType.SUCCESS: "[OK]",
                NotificationType.ERROR: "[ERROR]",
                NotificationType.INFO: "[INFO]",
                NotificationType.WARNING: "[WARN]"
            }.get(notification_type, "")
            
            self.notification.notify(
                title=f"{app_name_prefix} {title}",
                message=message,
                app_name="Fylum",
                timeout=10
            )
            return True
        except Exception:
            return False
    
    def set_enabled(self, enabled: bool):
        """Enable or disable notifications"""
        self.enabled = enabled
    
    def is_enabled(self) -> bool:
        """Check if notifications are enabled"""
        return self.enabled
    
    def get_history(self) -> List[NotificationRecord]:
        """Get notification history"""
        return self.history
    
    def clear_history(self):
        """Clear notification history"""
        self.history.clear()
    
    def is_available(self) -> bool:
        """Check if notification system is available"""
        return self.available
