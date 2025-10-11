"""
Notification endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from src.notifications.manager import NotificationManager, NotificationType

router = APIRouter()
notification_manager = NotificationManager()


class NotificationSend(BaseModel):
    """Model for sending a notification"""
    title: str
    message: str
    notification_type: str = "info"


class NotificationPreferences(BaseModel):
    """Model for notification preferences"""
    enabled: bool


@router.post("/send")
async def send_notification(notification: NotificationSend):
    """Send a notification"""
    try:
        notification_type = NotificationType(notification.notification_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification type")
    
    sent = notification_manager.send_notification(
        title=notification.title,
        message=notification.message,
        notification_type=notification_type
    )
    
    return {"sent": sent, "message": "Notification sent" if sent else "Notification queued"}


@router.get("/preferences")
async def get_preferences():
    """Get notification preferences"""
    return {
        "enabled": notification_manager.is_enabled(),
        "available": notification_manager.is_available()
    }


@router.post("/preferences")
async def update_preferences(prefs: NotificationPreferences):
    """Update notification preferences"""
    notification_manager.set_enabled(prefs.enabled)
    
    return {
        "enabled": notification_manager.is_enabled(),
        "message": "Preferences updated"
    }


@router.get("/history")
async def get_history():
    """Get notification history"""
    history = notification_manager.get_history()
    
    return {
        "notifications": [
            {
                "title": record.title,
                "message": record.message,
                "type": record.notification_type.value,
                "timestamp": record.timestamp.isoformat()
            }
            for record in history
        ]
    }


@router.delete("/history")
async def clear_history():
    """Clear notification history"""
    notification_manager.clear_history()
    return {"message": "History cleared"}


@router.post("/test")
async def send_test_notification():
    """Send a test notification"""
    sent = notification_manager.send_notification(
        title="Fylum Test Notification",
        message="If you see this, notifications are working correctly!",
        notification_type=NotificationType.INFO
    )
    
    return {
        "sent": sent,
        "message": "Test notification sent" if sent else "Notifications may not be available on this system"
    }


@router.get("/available")
async def check_availability():
    """Check if notification system is available"""
    return {
        "available": notification_manager.is_available(),
        "enabled": notification_manager.is_enabled()
    }
