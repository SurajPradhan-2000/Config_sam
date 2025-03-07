import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import SocialMediaCreate, SocialMediaUpdate, SocialMediaResponse
from app.api.databases import get_db_connection

# Initialize logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/social", tags=["Social Media Management"])

# ✅ Add Social Media Link (Anyone can create)
@router.post("/", response_model=SocialMediaResponse)
async def add_social_media(social_data: SocialMediaCreate):
    """Create a new social media link (Anyone can create)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO social_media (platform, link) VALUES (%s, %s) RETURNING id, created_at, updated_at",
                (social_data.platform, social_data.link)
            )
            new_social = cursor.fetchone()
            conn.commit()

        return SocialMediaResponse(
            id=new_social[0],
            platform=social_data.platform,
            link=social_data.link,
            created_at=new_social[1],
            updated_at=new_social[2]
        )
    except Exception as e:
        logger.error(f"Error adding social media link: {e}")
        raise HTTPException(status_code=500, detail="Error adding social media link")
    finally:
        conn.close()

# ✅ Get All Social Media Links (Anyone can view)
@router.get("/", response_model=List[SocialMediaResponse])
async def list_social_media():
    """Retrieve all social media links (Anyone can view)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, platform, link, created_at, updated_at FROM social_media")
            social_links = cursor.fetchall()

        return [
            SocialMediaResponse(
                id=link[0], platform=link[1], link=link[2], created_at=link[3], updated_at=link[4]
            ) for link in social_links
        ]
    except Exception as e:
        logger.error(f"Error fetching social media links: {e}")
        raise HTTPException(status_code=500, detail="Error fetching social media links")
    finally:
        conn.close()

# ✅ Get Social Media Link by ID (Anyone can view)
@router.get("/{social_id}", response_model=SocialMediaResponse)
async def get_social_media_by_id(social_id: int):
    """Retrieve a social media link by ID (Anyone can view)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, platform, link, created_at, updated_at FROM social_media WHERE id=%s", (social_id,))
            social = cursor.fetchone()

        if not social:
            raise HTTPException(status_code=404, detail="Social media link not found")

        return SocialMediaResponse(
            id=social[0], platform=social[1], link=social[2], created_at=social[3], updated_at=social[4]
        )
    except Exception as e:
        logger.error(f"Error fetching social media link by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching social media link")
    finally:
        conn.close()

# ✅ Update Social Media Link (Anyone can update)
@router.put("/", response_model=SocialMediaResponse)
async def update_social_media(social_data: SocialMediaUpdate):
    """Update an existing social media link (Anyone can update)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE social_media SET platform=%s, link=%s, updated_at=NOW() WHERE id=%s RETURNING id, created_at, updated_at",
                (social_data.platform, social_data.link, social_data.id)
            )
            updated_social = cursor.fetchone()
            conn.commit()

        if not updated_social:
            raise HTTPException(status_code=404, detail="Social media link not found")

        return SocialMediaResponse(
            id=updated_social[0],
            platform=social_data.platform,
            link=social_data.link,
            created_at=updated_social[1],
            updated_at=updated_social[2]
        )
    except Exception as e:
        logger.error(f"Error updating social media link: {e}")
        raise HTTPException(status_code=500, detail="Error updating social media link")
    finally:
        conn.close()
@router.delete("/{social_id}")
async def delete_social_media(social_id: int):
    """Delete a social media link by ID."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM social_media WHERE id=%s RETURNING id", (social_id,))
            deleted_social = cursor.fetchone()
            conn.commit()

        if not deleted_social:
            raise HTTPException(status_code=404, detail="Social media link not found")

        return {"message": "Social media link deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting social media link: {e}")
        raise HTTPException(status_code=500, detail="Error deleting social media link")
    finally:
        conn.close()