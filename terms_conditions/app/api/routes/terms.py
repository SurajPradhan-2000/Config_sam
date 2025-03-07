import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import TermsCreate, TermsUpdate, TermsResponse
from app.api.databases import get_db_connection

# Initialize logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/terms", tags=["Terms & Conditions"])

# ✅ Create Terms
@router.post("/", response_model=TermsResponse)
async def create_terms(terms_data: TermsCreate):
    """Create a new Terms and Conditions entry."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO terms_conditions (title, content, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW()) RETURNING id, title, content, created_at, updated_at;
                """,
                (terms_data.title, terms_data.content)
            )
            new_terms = cursor.fetchone()
            connection.commit()
        return {
            "id": new_terms[0],
            "title": new_terms[1],
            "content": new_terms[2],
            "created_at": new_terms[3],
            "updated_at": new_terms[4]
        }
    except Exception as e:
        logger.error(f"Error creating Terms: {e}")
        raise HTTPException(status_code=500, detail="Error creating Terms and Conditions")
    finally:
        connection.close()

# ✅ Get All Terms
@router.get("/", response_model=List[TermsResponse])
async def get_all_terms():
    """Retrieve all Terms and Conditions."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, content, created_at, updated_at FROM terms_conditions;")
            terms = cursor.fetchall()
        
        if not terms:
            raise HTTPException(status_code=404, detail="No Terms and Conditions found")

        return [
            {"id": t[0], "title": t[1], "content": t[2], "created_at": t[3], "updated_at": t[4]}
            for t in terms
        ]
    except Exception as e:
        logger.error(f"Error fetching Terms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching Terms and Conditions")
    finally:
        connection.close()

# ✅ Get Terms by ID
@router.get("/{terms_id}", response_model=TermsResponse)
async def get_terms(terms_id: int):
    """Retrieve a specific Terms and Conditions entry by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, content, created_at, updated_at FROM terms_conditions WHERE id = %s;", 
                (terms_id,)
            )
            terms = cursor.fetchone()
        
        if not terms:
            raise HTTPException(status_code=404, detail="Terms and Conditions not found")

        return {
            "id": terms[0],
            "title": terms[1],
            "content": terms[2],
            "created_at": terms[3],
            "updated_at": terms[4]
        }
    except Exception as e:
        logger.error(f"Error fetching Terms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching Terms and Conditions")
    finally:
        connection.close()

# ✅ Update Terms
@router.put("/", response_model=TermsResponse)
async def update_terms(terms_data: TermsUpdate):
    """Update an existing Terms and Conditions entry."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM terms_conditions WHERE id = %s;", (terms_data.id,)
            )
            existing_terms = cursor.fetchone()
        
        if not existing_terms:
            raise HTTPException(status_code=404, detail="Terms and Conditions not found")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE terms_conditions 
                SET title = %s, content = %s, updated_at = NOW()
                WHERE id = %s 
                RETURNING id, title, content, created_at, updated_at;
                """,
                (terms_data.title, terms_data.content, terms_data.id)
            )
            updated_terms = cursor.fetchone()
            connection.commit()
        
        return {
            "id": updated_terms[0],
            "title": updated_terms[1],
            "content": updated_terms[2],
            "created_at": updated_terms[3],
            "updated_at": updated_terms[4]
        }
    except Exception as e:
        logger.error(f"Error updating Terms: {e}")
        raise HTTPException(status_code=500, detail="Error updating Terms and Conditions")
    finally:
        connection.close()

# ✅ Delete Terms
@router.delete("/{id}")
async def delete_terms(id: int):
    """Delete a Terms and Conditions entry by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM terms_conditions WHERE id = %s;", (id,))
            existing_terms = cursor.fetchone()
        
        if not existing_terms:
            raise HTTPException(status_code=404, detail="Terms and Conditions not found")

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM terms_conditions WHERE id = %s;", (id,))
            connection.commit()

        return {"message": "Terms and Conditions deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting Terms: {e}")
        raise HTTPException(status_code=500, detail="Error deleting Terms and Conditions")
    finally:
        connection.close()
