import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.api.schemas import PrivacyPolicyCreate, PrivacyPolicyUpdate, PrivacyPolicyResponse
from app.api.databases import get_db_connection

# Initialize logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/privacy", tags=["Privacy Policy"])

# ✅ Create Privacy Policy
@router.post("/", response_model=PrivacyPolicyResponse)
async def create_privacy_policy(policy_data: PrivacyPolicyCreate):
    """Create a new privacy policy."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO privacy_policies (title, content, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW()) RETURNING id, title, content, created_at, updated_at;
                """,
                (policy_data.title, policy_data.content)
            )
            new_policy = cursor.fetchone()
            connection.commit()
        return {
            "id": new_policy[0],
            "title": new_policy[1],
            "content": new_policy[2],
            "created_at": new_policy[3],
            "updated_at": new_policy[4]
        }
    except Exception as e:
        logger.error(f"Error creating privacy policy: {e}")
        raise HTTPException(status_code=500, detail="Error creating privacy policy")
    finally:
        connection.close()

# ✅ Get All Privacy Policies
@router.get("/", response_model=List[PrivacyPolicyResponse])
async def get_all_privacy_policies():
    """Retrieve all privacy policies."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, content, created_at, updated_at FROM privacy_policies;")
            policies = cursor.fetchall()
        
        if not policies:
            raise HTTPException(status_code=404, detail="No privacy policies found")

        return [
            {"id": p[0], "title": p[1], "content": p[2], "created_at": p[3], "updated_at": p[4]}
            for p in policies
        ]
    except Exception as e:
        logger.error(f"Error fetching privacy policies: {e}")
        raise HTTPException(status_code=500, detail="Error fetching privacy policies")
    finally:
        connection.close()

# ✅ Get Privacy Policy by ID
@router.get("/{policy_id}", response_model=PrivacyPolicyResponse)
async def get_privacy_policy(policy_id: int):
    """Retrieve a specific privacy policy by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, content, created_at, updated_at FROM privacy_policies WHERE id = %s;", 
                (policy_id,)
            )
            policy = cursor.fetchone()
        
        if not policy:
            raise HTTPException(status_code=404, detail="Privacy policy not found")

        return {
            "id": policy[0],
            "title": policy[1],
            "content": policy[2],
            "created_at": policy[3],
            "updated_at": policy[4]
        }
    except Exception as e:
        logger.error(f"Error fetching privacy policy: {e}")
        raise HTTPException(status_code=500, detail="Error fetching privacy policy")
    finally:
        connection.close()

# ✅ Update Privacy Policy
@router.put("/", response_model=PrivacyPolicyResponse)
async def update_privacy_policy(policy_data: PrivacyPolicyUpdate):
    """Update an existing privacy policy."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM privacy_policies WHERE id = %s;", (policy_data.id,)
            )
            existing_policy = cursor.fetchone()
        
        if not existing_policy:
            raise HTTPException(status_code=404, detail="Privacy policy not found")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE privacy_policies 
                SET title = %s, content = %s, updated_at = NOW()
                WHERE id = %s 
                RETURNING id, title, content, created_at, updated_at;
                """,
                (policy_data.title, policy_data.content, policy_data.id)
            )
            updated_policy = cursor.fetchone()
            connection.commit()
        
        return {
            "id": updated_policy[0],
            "title": updated_policy[1],
            "content": updated_policy[2],
            "created_at": updated_policy[3],
            "updated_at": updated_policy[4]
        }
    except Exception as e:
        logger.error(f"Error updating privacy policy: {e}")
        raise HTTPException(status_code=500, detail="Error updating privacy policy")
    finally:
        connection.close()

# ✅ Delete Privacy Policy
@router.delete("/{policy_id}")
async def delete_privacy_policy(policy_id: int):
    """Delete a privacy policy by ID."""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM privacy_policies WHERE id = %s;", (policy_id,))
            existing_policy = cursor.fetchone()
        
        if not existing_policy:
            raise HTTPException(status_code=404, detail="Privacy policy not found")

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM privacy_policies WHERE id = %s;", (policy_id,))
            connection.commit()
        
        return {"message": "Privacy policy deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting privacy policy: {e}")
        raise HTTPException(status_code=500, detail="Error deleting privacy policy")
    finally:
        connection.close()
