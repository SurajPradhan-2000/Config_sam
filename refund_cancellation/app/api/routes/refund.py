import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import RefundCancellationCreate, RefundCancellationUpdate, RefundCancellationResponse
from app.api.databases import get_db_connection

# Initialize logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/refund", tags=["Refund & Cancellation"])

# ✅ Create Refund Policy
@router.post("/", response_model=RefundCancellationResponse)
async def create_refund(refund_data: RefundCancellationCreate):
    """Create a new Refund & Cancellation policy."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO refund_cancellation (title, content, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW()) RETURNING id, title, content, created_at, updated_at;
                """,
                (refund_data.title, refund_data.content)
            )
            new_refund = cursor.fetchone()
            connection.commit()
        return {
            "id": new_refund[0],
            "title": new_refund[1],
            "content": new_refund[2],
            "created_at": new_refund[3],
            "updated_at": new_refund[4]
        }
    except Exception as e:
        logger.error(f"Error creating Refund Policy: {e}")
        raise HTTPException(status_code=500, detail="Error creating Refund Policy")
    finally:
        connection.close()

# ✅ Get All Refund Policies
@router.get("/", response_model=List[RefundCancellationResponse])
async def get_all_refunds():
    """Retrieve all Refund & Cancellation policies."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, content, created_at, updated_at FROM refund_cancellation;")
            refunds = cursor.fetchall()

        if not refunds:
            raise HTTPException(status_code=404, detail="No refund policies found")

        return [
            {"id": r[0], "title": r[1], "content": r[2], "created_at": r[3], "updated_at": r[4]}
            for r in refunds
        ]
    except Exception as e:
        logger.error(f"Error fetching Refund Policies: {e}")
        raise HTTPException(status_code=500, detail="Error fetching refund policies")
    finally:
        connection.close()

# ✅ Get Refund Policy by ID
@router.get("/{refund_id}", response_model=RefundCancellationResponse)
async def get_refund(refund_id: int):
    """Retrieve a specific Refund & Cancellation policy by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, content, created_at, updated_at FROM refund_cancellation WHERE id = %s;",
                (refund_id,)
            )
            refund = cursor.fetchone()

        if not refund:
            raise HTTPException(status_code=404, detail="Refund policy not found")

        return {
            "id": refund[0],
            "title": refund[1],
            "content": refund[2],
            "created_at": refund[3],
            "updated_at": refund[4]
        }
    except Exception as e:
        logger.error(f"Error fetching Refund Policy: {e}")
        raise HTTPException(status_code=500, detail="Error fetching refund policy")
    finally:
        connection.close()

# ✅ Update Refund Policy
@router.put("/", response_model=RefundCancellationResponse)
async def update_refund(refund_data: RefundCancellationUpdate):
    """Update an existing Refund & Cancellation policy."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM refund_cancellation WHERE id = %s;", (refund_data.id,))
            existing_refund = cursor.fetchone()

        if not existing_refund:
            raise HTTPException(status_code=404, detail="Refund policy not found")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE refund_cancellation
                SET title = %s, content = %s, updated_at = NOW()
                WHERE id = %s 
                RETURNING id, title, content, created_at, updated_at;
                """,
                (refund_data.title, refund_data.content, refund_data.id)
            )
            updated_refund = cursor.fetchone()
            connection.commit()

        return {
            "id": updated_refund[0],
            "title": updated_refund[1],
            "content": updated_refund[2],
            "created_at": updated_refund[3],
            "updated_at": updated_refund[4]
        }
    except Exception as e:
        logger.error(f"Error updating Refund Policy: {e}")
        raise HTTPException(status_code=500, detail="Error updating refund policy")
    finally:
        connection.close()

# ✅ Delete Refund Policy
@router.delete("/{refund_id}")
async def delete_refund(refund_id: int):
    """Delete a Refund & Cancellation policy by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM refund_cancellation WHERE id = %s;", (refund_id,))
            existing_refund = cursor.fetchone()

        if not existing_refund:
            raise HTTPException(status_code=404, detail="Refund policy not found")

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM refund_cancellation WHERE id = %s RETURNING id;", (refund_id,))
            deleted_id = cursor.fetchone()
            connection.commit()

        return {"message": "Refund policy deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting Refund Policy: {e}")
        raise HTTPException(status_code=500, detail="Error deleting refund policy")
    finally:
        connection.close()
