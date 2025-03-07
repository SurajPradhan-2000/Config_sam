import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from app.api.databases import get_db_connection

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/language", tags=["Language Management"])

# ✅ Add Language
@router.post("/", response_model=LanguageResponse)
async def add_language(language_data: LanguageCreate):
    """Create a new language (Anyone can create)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO languages (language, country) VALUES (%s, %s) RETURNING id, createdat, updatedat",
                (language_data.language, language_data.country)
            )
            new_language = cursor.fetchone()
            conn.commit()

        return LanguageResponse(
            id=new_language[0],
            language=language_data.language,
            country=language_data.country,
            createdat=new_language[1],
            updatedat=new_language[2]
        )
    except Exception as e:
        logger.error(f"Error adding language: {e}")
        raise HTTPException(status_code=500, detail="Error adding language")
    finally:
        conn.close()

# ✅ Get All Languages
@router.get("/", response_model=List[LanguageResponse])
async def get_languages():
    """Retrieve all languages (Anyone can view)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, language, country, createdat, updatedat FROM languages")
            languages = cursor.fetchall()

        return [
            LanguageResponse(
                id=lang[0], language=lang[1], country=lang[2], createdat=lang[3], updatedat=lang[4]
            ) for lang in languages
        ]
    except Exception as e:
        logger.error(f"Error fetching languages: {e}")
        raise HTTPException(status_code=500, detail="Error fetching languages")
    finally:
        conn.close()

# ✅ Update Language
@router.put("/", response_model=LanguageResponse)
async def update_language(language_data: LanguageUpdate):
    """Update an existing language (Anyone can update)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE languages SET language=%s, country=%s, updatedat=NOW() WHERE id=%s RETURNING id, createdat, updatedat",
                (language_data.language, language_data.country, language_data.id)
            )
            updated_language = cursor.fetchone()
            conn.commit()

        if not updated_language:
            raise HTTPException(status_code=404, detail="Language not found")

        return LanguageResponse(
            id=updated_language[0],
            language=language_data.language,
            country=language_data.country,
            createdat=updated_language[1],
            updatedat=updated_language[2]
        )
    except Exception as e:
        logger.error(f"Error updating language: {e}")
        raise HTTPException(status_code=500, detail="Error updating language")
    finally:
        conn.close()
# ✅ Get Language by ID
@router.get("/{id}", response_model=LanguageResponse)
async def get_language_by_id(id: int):
    """Retrieve a language by its ID (Anyone can view)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, language, country, createdat, updatedat FROM languages WHERE id=%s", (id,))
            language = cursor.fetchone()

        if not language:
            raise HTTPException(status_code=404, detail="Language not found")

        return LanguageResponse(
            id=language[0], language=language[1], country=language[2], createdat=language[3], updatedat=language[4]
        )
    except Exception as e:
        logger.error(f"Error fetching language by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching language")
    finally:
        conn.close()
# ✅ Delete Language
@router.delete("/{id}")
async def delete_language(id: int):
    """Delete a language (Anyone can delete)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM languages WHERE id=%s RETURNING id", (id,))
            deleted_language = cursor.fetchone()
            conn.commit()

        if not deleted_language:
            raise HTTPException(status_code=404, detail="Language not found")

        return {"message": "Language deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting language: {e}")
        raise HTTPException(status_code=500, detail="Error deleting language")
    finally:
        conn.close()
