from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional

from app.models.schemas import BlockchainLogRequest, BlockchainLogResponse
from app.services.blockchain import BlockchainLogger

router = APIRouter()

# Initialize blockchain service
blockchain_logger = BlockchainLogger()

@router.post("/log-to-blockchain", response_model=BlockchainLogResponse)
async def log_fraud_event(request: BlockchainLogRequest):
    """
    Log fraud event to blockchain for immutable record
    """
    try:
        # Log to blockchain
        tx_result = await blockchain_logger.log_fraud_event(
            user_id_hash=request.user_id_hash,
            risk_score=request.risk_score,
            action=request.action,
            metadata=request.metadata or {}
        )
        
        response = BlockchainLogResponse(
            success=True,
            transaction_hash=tx_result["transaction_hash"],
            block_number=tx_result.get("block_number"),
            gas_used=tx_result.get("gas_used"),
            logged_at=datetime.now()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain logging failed: {str(e)}")

@router.get("/blockchain/logs")
async def get_blockchain_logs(
    limit: int = 50,
    offset: int = 0,
    action_filter: Optional[str] = None
):
    """
    Retrieve fraud events from blockchain
    """
    try:
        logs = await blockchain_logger.get_fraud_logs(
            limit=limit,
            offset=offset,
            action_filter=action_filter
        )
        
        return {
            "logs": logs,
            "total": len(logs),
            "contract_address": blockchain_logger.contract_address,
            "network": "Polygon Mumbai"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log retrieval failed: {str(e)}")

@router.get("/blockchain/transaction/{tx_hash}")
async def get_transaction_details(tx_hash: str):
    """
    Get detailed information about a blockchain transaction
    """
    try:
        details = await blockchain_logger.get_transaction_details(tx_hash)
        
        return {
            "transaction_hash": tx_hash,
            "block_number": details.get("block_number"),
            "gas_used": details.get("gas_used"),
            "gas_price": details.get("gas_price"),
            "status": details.get("status"),
            "timestamp": details.get("timestamp"),
            "from_address": details.get("from"),
            "to_address": details.get("to"),
            "event_data": details.get("event_data")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction details retrieval failed: {str(e)}")

@router.get("/blockchain/contract-info")
async def get_contract_info():
    """
    Get information about the deployed smart contract
    """
    try:
        info = await blockchain_logger.get_contract_info()
        
        return {
            "contract_address": blockchain_logger.contract_address,
            "network": "Polygon Mumbai",
            "abi_version": "1.0.0",
            "deployment_block": info.get("deployment_block"),
            "total_events": info.get("total_events"),
            "last_event_block": info.get("last_event_block")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contract info retrieval failed: {str(e)}")

@router.post("/blockchain/verify-event")
async def verify_blockchain_event(tx_hash: str, expected_data: dict):
    """
    Verify that a blockchain event contains expected data
    """
    try:
        is_valid = await blockchain_logger.verify_event_data(tx_hash, expected_data)
        
        return {
            "transaction_hash": tx_hash,
            "is_valid": is_valid,
            "verified_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event verification failed: {str(e)}")