from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List

from app.models.schemas import BlockUserRequest, BlockUserResponse, BlockedUser
from app.services.supabase_client import add_to_blocklist, get_blocklist, remove_from_blocklist

router = APIRouter()

@router.post("/block-user", response_model=BlockUserResponse)
async def block_user(request: BlockUserRequest):
    """
    Add user/device to blocklist
    """
    try:
        # Add to Supabase blocklist
        block_record = await add_to_blocklist(request)
        
        response = BlockUserResponse(
            success=True,
            message=f"User {request.user_id} successfully blocked",
            block_id=block_record["id"],
            blocked_at=datetime.now()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User blocking failed: {str(e)}")

@router.get("/blocklist", response_model=List[BlockedUser])
async def get_blocked_users(
    limit: int = 100,
    offset: int = 0,
    search: str = None,
    status: str = None
):
    """
    Get list of blocked users with optional filtering
    """
    try:
        blocked_users = await get_blocklist(
            limit=limit,
            offset=offset,
            search=search,
            status=status
        )
        
        return blocked_users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blocklist retrieval failed: {str(e)}")

@router.delete("/block-user/{user_id}")
async def unblock_user(user_id: str, reason: str = "Manual review completed"):
    """
    Remove user from blocklist
    """
    try:
        success = await remove_from_blocklist(user_id, reason)
        
        if success:
            return {"message": f"User {user_id} successfully unblocked", "success": True}
        else:
            raise HTTPException(status_code=404, detail="User not found in blocklist")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User unblocking failed: {str(e)}")

@router.get("/block-user/{user_id}/status")
async def check_user_status(user_id: str):
    """
    Check if user is currently blocked
    """
    try:
        # Check user status in blocklist
        status = await get_user_block_status(user_id)
        
        return {
            "user_id": user_id,
            "is_blocked": status["is_blocked"],
            "block_reason": status.get("reason"),
            "blocked_at": status.get("blocked_at"),
            "block_type": status.get("block_type")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.put("/block-user/{user_id}/status")
async def update_block_status(user_id: str, new_status: str, reason: str = None):
    """
    Update block status (permanent, temporary, under_review)
    """
    try:
        valid_statuses = ["permanent", "temporary", "under_review", "removed"]
        
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        success = await update_user_block_status(user_id, new_status, reason)
        
        if success:
            return {"message": f"User {user_id} status updated to {new_status}", "success": True}
        else:
            raise HTTPException(status_code=404, detail="User not found in blocklist")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status update failed: {str(e)}")

# Helper functions (would be implemented in supabase_client.py)
async def get_user_block_status(user_id: str):
    """Get current block status for user"""
    # Implementation would query Supabase
    return {
        "is_blocked": False,
        "reason": None,
        "blocked_at": None,
        "block_type": None
    }

async def update_user_block_status(user_id: str, new_status: str, reason: str = None):
    """Update user block status"""
    # Implementation would update Supabase record
    return True