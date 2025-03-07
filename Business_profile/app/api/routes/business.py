import logging
import shutil
import os
from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.api.schemas import BusinessProfileCreate, BusinessProfileUpdate, BusinessProfileResponse
from app.api.databases import get_db_connection

# Initialize logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/business", tags=["Business Profile"])

# Directory to store uploaded business profile logos
UPLOAD_DIR = "/tmp/uploads/business_logos"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists

# ✅ Create Business Profile with Image Upload
@router.post("/", response_model=BusinessProfileResponse)
async def add_business_profile(
    name: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    contact: str = Form(...),
    logo: UploadFile = File(...),
):
    """Create a new business profile with an uploaded logo image."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_DIR, logo.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)

        # Save profile in the database
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO business_profiles (name, email, logo, address, contact)
                VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at, updated_at
                """,
                (name, email, file_path, address, contact),
            )
            new_profile = cursor.fetchone()
            conn.commit()

        return BusinessProfileResponse(
            id=new_profile[0],
            name=name,
            email=email,
            logo=file_path,
            address=address,
            contact=contact,
            created_at=new_profile[1],
            updated_at=new_profile[2],
        )
    except Exception as e:
        logger.error(f"Error adding business profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()

# ✅ Get Single Business Profile
@router.get("/{id}", response_model=BusinessProfileResponse)
async def get_business_profile(id: int):
    """Retrieve a single business profile by ID."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, logo, address, contact, created_at, updated_at FROM business_profiles WHERE id=%s", (id,))
            profile = cursor.fetchone()

        if not profile:
            raise HTTPException(status_code=404, detail="Business profile not found")

        return BusinessProfileResponse(
            id=profile[0],
            name=profile[1],
            email=profile[2],
            logo=profile[3],
            address=profile[4],
            contact=profile[5],
            created_at=profile[6],
            updated_at=profile[7],
        )
    except Exception as e:
        logger.error(f"Error fetching business profile: {e}")
        raise HTTPException(status_code=500, detail="Error fetching business profile")
    finally:
        conn.close()

# ✅ Get All Business Profiles
@router.get("/", response_model=List[BusinessProfileResponse])
async def get_all_business_profiles():
    """Retrieve all business profiles."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, logo, address, contact, created_at, updated_at FROM business_profiles")
            profiles = cursor.fetchall()

        return [
            BusinessProfileResponse(
                id=profile[0], name=profile[1], email=profile[2], logo=profile[3], address=profile[4], contact=profile[5], created_at=profile[6], updated_at=profile[7]
            ) for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error fetching business profiles: {e}")
        raise HTTPException(status_code=500, detail="Error fetching business profiles")
    finally:
        conn.close()

# ✅ Update Business Profile
@router.put("/{id}", response_model=BusinessProfileResponse)
async def update_business_profile(
    id: int,
    name: str = Form(None),
    email: str = Form(None),
    address: str = Form(None),
    contact: str = Form(None),
    logo: UploadFile = File(None),
):
    """Update an existing business profile."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM business_profiles WHERE id=%s", (id,))
            existing_profile = cursor.fetchone()

            if not existing_profile:
                raise HTTPException(status_code=404, detail="Business profile not found")

            update_fields = []
            update_values = []

            if name:
                update_fields.append("name = %s")
                update_values.append(name)
            if email:
                update_fields.append("email = %s")
                update_values.append(email)
            if address:
                update_fields.append("address = %s")
                update_values.append(address)
            if contact:
                update_fields.append("contact = %s")
                update_values.append(contact)
            if logo:
                file_path = os.path.join(UPLOAD_DIR, logo.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(logo.file, buffer)
                update_fields.append("logo = %s")
                update_values.append(file_path)

            if update_fields:
                update_values.append(id)
                query = f"UPDATE business_profiles SET {', '.join(update_fields)}, updated_at = NOW() WHERE id = %s RETURNING id, created_at, updated_at"
                cursor.execute(query, tuple(update_values))
                updated_profile = cursor.fetchone()
                conn.commit()

                return BusinessProfileResponse(
                    id=updated_profile[0],
                    name=name or existing_profile[1],
                    email=email or existing_profile[2],
                    logo=file_path if logo else existing_profile[3],
                    address=address or existing_profile[4],
                    contact=contact or existing_profile[5],
                    created_at=updated_profile[1],
                    updated_at=updated_profile[2],
                )
    except Exception as e:
        logger.error(f"Error updating business profile: {e}")
        raise HTTPException(status_code=500, detail="Error updating business profile")
    finally:
        conn.close()
@router.delete("/{id}")
async def delete_business_profile(id: int):
    """Delete a business profile by ID."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            # Check if business profile exists
            cursor.execute("SELECT id FROM business_profiles WHERE id=%s", (id,))
            existing_profile = cursor.fetchone()

            if not existing_profile:
                raise HTTPException(status_code=404, detail="Business profile not found")

            # Delete business profile
            cursor.execute("DELETE FROM business_profiles WHERE id=%s", (id,))
            conn.commit()

        return {"message": "Business profile deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting business profile: {str(e)}")
    finally:
        conn.close()