import logging
import traceback
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import TaxCreate, TaxUpdate, TaxResponse
from app.api.databases import get_db_connection

# Initialize logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tax", tags=["Tax Management"])

# ✅ Add Tax
@router.post("/", response_model=TaxResponse)
async def add_tax(tax_data: TaxCreate):
    """Create a new tax entry."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO taxes (name, type, value) VALUES (%s, %s, %s) RETURNING id, created_at, updated_at",
                (tax_data.name, tax_data.type, tax_data.value)
            )
            new_tax = cursor.fetchone()
            conn.commit()

        if not new_tax:
            raise HTTPException(status_code=500, detail="Failed to create tax entry")

        return TaxResponse(
            id=new_tax[0],
            name=tax_data.name,
            type=tax_data.type,
            value=tax_data.value,
            created_at=new_tax[1],
            updated_at=new_tax[2]
        )
    except Exception as e:
        logger.error(f"Error adding tax: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error adding tax: {str(e)}")
    finally:
        conn.close()

# ✅ Get All Taxes
@router.get("/", response_model=List[TaxResponse])
async def get_taxes():
    """Retrieve all tax entries."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, type, value, created_at, updated_at FROM taxes")
            taxes = cursor.fetchall()

        return [
            TaxResponse(
                id=tax[0], name=tax[1], type=tax[2], value=tax[3], created_at=tax[4], updated_at=tax[5]
            ) for tax in taxes
        ]
    except Exception as e:
        logger.error(f"Error fetching taxes: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error fetching taxes")
    finally:
        conn.close()

# ✅ Get Tax by ID
@router.get("/{tax_id}", response_model=TaxResponse)
async def get_tax_by_id(tax_id: int):
    """Retrieve a tax entry by ID."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, type, value, created_at, updated_at FROM taxes WHERE id=%s", (tax_id,))
            tax = cursor.fetchone()

        if not tax:
            raise HTTPException(status_code=404, detail="Tax entry not found")

        return TaxResponse(
            id=tax[0], name=tax[1], type=tax[2], value=tax[3], created_at=tax[4], updated_at=tax[5]
        )
    except Exception as e:
        logger.error(f"Error fetching tax by ID: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error fetching tax")
    finally:
        conn.close()

# ✅ Update Tax
@router.put("/", response_model=TaxResponse)
async def update_tax(tax_data: TaxUpdate):
    """Update an existing tax entry."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE taxes SET name=%s, type=%s, value=%s, updated_at=NOW() WHERE id=%s RETURNING id, created_at, updated_at",
                (tax_data.name, tax_data.type, tax_data.value, tax_data.id)
            )
            updated_tax = cursor.fetchone()
            conn.commit()

        if not updated_tax:
            raise HTTPException(status_code=404, detail="Tax entry not found")

        return TaxResponse(
            id=updated_tax[0],
            name=tax_data.name,
            type=tax_data.type,
            value=tax_data.value,
            created_at=updated_tax[1],
            updated_at=updated_tax[2]
        )
    except Exception as e:
        logger.error(f"Error updating tax: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error updating tax")
    finally:
        conn.close()

# ✅ Delete Tax
@router.delete("/{tax_id}")
async def delete_tax(tax_id: int):
    """Delete a tax entry."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM taxes WHERE id=%s RETURNING id", (tax_id,))
            deleted_tax = cursor.fetchone()
            conn.commit()

        if not deleted_tax:
            raise HTTPException(status_code=404, detail="Tax entry not found")

        return {"message": "Tax entry deleted successfully", "id": deleted_tax[0]}
    except Exception as e:
        logger.error(f"Error deleting tax: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error deleting tax")
    finally:
        conn.close()
