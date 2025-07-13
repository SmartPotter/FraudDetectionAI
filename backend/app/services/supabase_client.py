import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import (
    TransactionData, ScoreResponse, BlockUserRequest, 
    BlockedUser, UploadResponse
)

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be provided")
        
        self.client: Client = create_client(self.url, self.key)
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    async def _run_sync(self, func, *args, **kwargs):
        """Run synchronous Supabase operations in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args, **kwargs)

# Initialize global client
supabase_client = SupabaseClient()

async def save_transactions(transactions: List[Dict[str, Any]], file_id: str) -> bool:
    """Save uploaded transactions to Supabase"""
    try:
        # Prepare transaction records
        records = []
        for tx in transactions:
            record = {
                "transaction_id": tx.get("transaction_id"),
                "user_id": tx.get("user_id"),
                "amount": float(tx.get("amount", 0)),
                "timestamp": tx.get("timestamp"),
                "location": tx.get("location"),
                "device_id": tx.get("device_id"),
                "payment_method": tx.get("payment_method"),
                "merchant_category": tx.get("merchant_category"),
                "file_id": file_id,
                "created_at": datetime.now().isoformat()
            }
            records.append(record)
        
        # Insert into transactions table
        def insert_transactions():
            return supabase_client.client.table("transactions").insert(records).execute()
        
        result = await supabase_client._run_sync(insert_transactions)
        return len(result.data) > 0
        
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False

async def save_fraud_score(score_response: ScoreResponse) -> bool:
    """Save fraud score to Supabase"""
    try:
        record = {
            "transaction_id": score_response.transaction_id,
            "risk_score": score_response.risk_score,
            "risk_level": score_response.risk_level.value,
            "flags": score_response.flags,
            "confidence": score_response.confidence,
            "model_version": score_response.model_version,
            "scored_at": datetime.now().isoformat()
        }
        
        def insert_score():
            return supabase_client.client.table("fraud_scores").insert(record).execute()
        
        result = await supabase_client._run_sync(insert_score)
        return len(result.data) > 0
        
    except Exception as e:
        print(f"Error saving fraud score: {e}")
        return False

async def add_to_blocklist(request: BlockUserRequest) -> Dict[str, Any]:
    """Add user to blocklist"""
    try:
        record = {
            "user_id": request.user_id,
            "device_id": request.device_id,
            "reason": request.reason,
            "risk_score": request.risk_score,
            "blocked_by": request.blocked_by,
            "block_type": request.block_type,
            "blocked_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        def insert_block():
            return supabase_client.client.table("blocklist").insert(record).execute()
        
        result = await supabase_client._run_sync(insert_block)
        return result.data[0] if result.data else {}
        
    except Exception as e:
        print(f"Error adding to blocklist: {e}")
        raise

async def get_blocklist(
    limit: int = 100, 
    offset: int = 0, 
    search: str = None, 
    status: str = None
) -> List[BlockedUser]:
    """Get blocklist with optional filtering"""
    try:
        def query_blocklist():
            query = supabase_client.client.table("blocklist").select("*")
            
            if search:
                query = query.or_(f"user_id.ilike.%{search}%,reason.ilike.%{search}%")
            
            if status:
                query = query.eq("status", status)
            
            return query.range(offset, offset + limit - 1).order("blocked_at", desc=True).execute()
        
        result = await supabase_client._run_sync(query_blocklist)
        
        blocked_users = []
        for record in result.data:
            blocked_user = BlockedUser(
                id=record["id"],
                user_id=record["user_id"],
                device_id=record.get("device_id"),
                reason=record["reason"],
                risk_score=record["risk_score"],
                blocked_by=record["blocked_by"],
                blocked_at=datetime.fromisoformat(record["blocked_at"]),
                status=record["status"]
            )
            blocked_users.append(blocked_user)
        
        return blocked_users
        
    except Exception as e:
        print(f"Error getting blocklist: {e}")
        return []

async def remove_from_blocklist(user_id: str, reason: str) -> bool:
    """Remove user from blocklist"""
    try:
        def update_block():
            return supabase_client.client.table("blocklist").update({
                "status": "removed",
                "removed_at": datetime.now().isoformat(),
                "removal_reason": reason
            }).eq("user_id", user_id).eq("status", "active").execute()
        
        result = await supabase_client._run_sync(update_block)
        return len(result.data) > 0
        
    except Exception as e:
        print(f"Error removing from blocklist: {e}")
        return False

async def get_fraud_analytics_data(
    start_date: datetime, 
    end_date: datetime, 
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Get fraud analytics data for reports"""
    try:
        # Get transaction counts
        def get_transaction_stats():
            return supabase_client.client.table("transactions").select(
                "count", head=True
            ).gte("timestamp", start_date.isoformat()).lte(
                "timestamp", end_date.isoformat()
            ).execute()
        
        # Get fraud scores
        def get_fraud_stats():
            return supabase_client.client.table("fraud_scores").select(
                "*"
            ).gte("scored_at", start_date.isoformat()).lte(
                "scored_at", end_date.isoformat()
            ).execute()
        
        # Get blocklist stats
        def get_block_stats():
            return supabase_client.client.table("blocklist").select(
                "count", head=True
            ).gte("blocked_at", start_date.isoformat()).lte(
                "blocked_at", end_date.isoformat()
            ).execute()
        
        transaction_result = await supabase_client._run_sync(get_transaction_stats)
        fraud_result = await supabase_client._run_sync(get_fraud_stats)
        block_result = await supabase_client._run_sync(get_block_stats)
        
        # Process fraud scores
        high_risk_count = sum(1 for score in fraud_result.data if score["risk_score"] >= 0.8)
        medium_risk_count = sum(1 for score in fraud_result.data if 0.5 <= score["risk_score"] < 0.8)
        low_risk_count = sum(1 for score in fraud_result.data if score["risk_score"] < 0.5)
        
        analytics_data = {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "transaction_stats": {
                "total_transactions": transaction_result.count or 0,
                "fraud_detected": high_risk_count,
                "fraud_rate": (high_risk_count / max(len(fraud_result.data), 1)) * 100
            },
            "risk_distribution": {
                "high_risk": high_risk_count,
                "medium_risk": medium_risk_count,
                "low_risk": low_risk_count
            },
            "blocklist_stats": {
                "users_blocked": block_result.count or 0
            },
            "top_flags": [
                "Unusual amount",
                "New device",
                "High velocity",
                "Location anomaly"
            ]
        }
        
        return analytics_data
        
    except Exception as e:
        print(f"Error getting analytics data: {e}")
        return {}

async def get_receipt_data(
    transaction_id: Optional[str] = None, 
    receipt_hash: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get receipt data for verification"""
    try:
        def query_receipt():
            query = supabase_client.client.table("receipts").select("*")
            
            if transaction_id:
                query = query.eq("transaction_id", transaction_id)
            elif receipt_hash:
                query = query.eq("receipt_hash", receipt_hash)
            else:
                return None
            
            return query.single().execute()
        
        result = await supabase_client._run_sync(query_receipt)
        return result.data if result.data else None
        
    except Exception as e:
        print(f"Error getting receipt data: {e}")
        return None