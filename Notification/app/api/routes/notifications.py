import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from app.api.databases import get_db_connection

# Initialize logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["Notification Management"])

# ✅ Create Notification
@router.post("/", response_model=NotificationResponse)
async def create_notification(notification_data: NotificationCreate):
    """Create a new notification."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO notifications (message, module, action, read) VALUES (%s, %s, %s, %s) RETURNING id, created_at, updated_at",
                (notification_data.message, notification_data.module, notification_data.action, False)
            )
            new_notification = cursor.fetchone()
            conn.commit()

        return NotificationResponse(
            id=new_notification[0],
            message=notification_data.message,
            module=notification_data.module,
            action=notification_data.action,
            read=False,
            created_at=new_notification[1],
            updated_at=new_notification[2]
        )
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        raise HTTPException(status_code=500, detail="Error creating notification")
    finally:
        conn.close()

# ✅ Fetch All Notifications
@router.get("/", response_model=List[NotificationResponse])
async def get_notifications():
    """Retrieve all notifications."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, message, module, action, read, created_at, updated_at FROM notifications")
            notifications = cursor.fetchall()

        return [
            NotificationResponse(
                id=notif[0], message=notif[1], module=notif[2], action=notif[3], read=notif[4], created_at=notif[5], updated_at=notif[6]
            ) for notif in notifications
        ]
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        raise HTTPException(status_code=500, detail="Error fetching notifications")
    finally:
        conn.close()

# ✅ Update Notification Settings (Enable/Disable)
@router.put("/settings")
async def update_notification_settings(module: str, action: str, enabled: bool):
    """Enable or disable a specific notification setting."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM notifications WHERE module=%s AND action=%s", (module, action))
            existing_setting = cursor.fetchone()

            if existing_setting:
                cursor.execute("UPDATE notifications SET read=%s, updated_at=NOW() WHERE id=%s", (enabled, existing_setting[0]))
            else:
                cursor.execute(
                    "INSERT INTO notifications (message, module, action, read) VALUES (%s, %s, %s, %s)",
                    (f"Notification for {action} updated", module, action, enabled)
                )
            conn.commit()

        return {"message": "Notification settings updated"}
    except Exception as e:
        logger.error(f"Error updating notification settings: {e}")
        raise HTTPException(status_code=500, detail="Error updating notification settings")
    finally:
        conn.close()

# ✅ Mark Notification as Read
@router.put("/")
async def mark_notification_as_read(notification_data: NotificationUpdate):
    """Mark a notification as read."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM notifications WHERE id=%s", (notification_data.id,))
            existing_notification = cursor.fetchone()

            if not existing_notification:
                raise HTTPException(status_code=404, detail="Notification not found")

            cursor.execute("UPDATE notifications SET read=%s, updated_at=NOW() WHERE id=%s", (notification_data.read, notification_data.id))
            conn.commit()

        return {"message": "Notification marked as read"}
    except Exception as e:
        logger.error(f"Error updating notification: {e}")
        raise HTTPException(status_code=500, detail="Error updating notification")
    finally:
        conn.close()

# ✅ Delete Notification by ID (ID in URL)
@router.delete("/{id}")
async def delete_notification(id: int):
    """Delete a notification by its ID."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            # Check if the notification exists
            cursor.execute("SELECT id FROM notifications WHERE id=%s", (id,))
            existing_notification = cursor.fetchone()

            if not existing_notification:
                raise HTTPException(status_code=404, detail="Notification not found")

            # Delete the notification
            cursor.execute("DELETE FROM notifications WHERE id=%s", (id,))
            conn.commit()

        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {e}")
        raise HTTPException(status_code=500, detail="Error deleting notification")
    finally:
        conn.close()
