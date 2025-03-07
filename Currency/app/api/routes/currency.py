import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import CurrencyCreate, CurrencyResponse, CurrencyUpdate
from app.api.databases import get_db_connection

# Initialize Logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["Currency"])

# ✅ Add Currency (Anyone can create)
@router.post("/", response_model=CurrencyResponse)
async def add_currency(currency_data: CurrencyCreate):
    """Create a new currency (Anyone can create)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO currencies (currencyname, country) VALUES (%s, %s) RETURNING id, createdat, updatedat",
                (currency_data.currencyname, currency_data.country)
            )
            new_currency = cursor.fetchone()
            conn.commit()
        
        return CurrencyResponse(
            id=new_currency[0],
            currencyname=currency_data.currencyname,
            country=currency_data.country,
            createdat=new_currency[1],
            updatedat=new_currency[2]
        )
    except Exception as e:
        logger.error(f"Error adding currency: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()

# ✅ Get All Currencies (Anyone can view)
@router.get("/", response_model=List[CurrencyResponse])
async def list_currencies():
    """Retrieve all currencies (Anyone can view)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, currencyname, country, createdat, updatedat FROM currencies")
            currencies = cursor.fetchall()
        
        return [
            CurrencyResponse(
                id=cur[0], currencyname=cur[1], country=cur[2], createdat=cur[3], updatedat=cur[4]
            ) for cur in currencies
        ]
    except Exception as e:
        logger.error(f"Error fetching currencies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()

# ✅ Update Currency (Anyone can update)
@router.put("/", response_model=CurrencyResponse)
async def update_currency(currency_data: CurrencyUpdate):
    """Update an existing currency by ID (Anyone can update)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE currencies SET currencyname=%s, country=%s, updatedat=NOW() WHERE id=%s RETURNING id, createdat, updatedat",
                (currency_data.currencyname, currency_data.country, currency_data.id)
            )
            updated_currency = cursor.fetchone()
            conn.commit()
        
        if not updated_currency:
            raise HTTPException(status_code=404, detail="Currency not found")
        
        return CurrencyResponse(
            id=updated_currency[0],
            currencyname=currency_data.currencyname,
            country=currency_data.country,
            createdat=updated_currency[1],
            updatedat=updated_currency[2]
        )
    except Exception as e:
        logger.error(f"Error updating currency: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()

# ✅ Delete Currency (Anyone can delete)
@router.delete("/{id}")
async def delete_currency(id: int):
    """Delete a currency by ID (Anyone can delete)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM currencies WHERE id=%s RETURNING id", (id,))
            deleted_currency = cursor.fetchone()
            conn.commit()
        
        if not deleted_currency:
            raise HTTPException(status_code=404, detail="Currency not found")
        
        return {"message": "Currency deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting currency: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
