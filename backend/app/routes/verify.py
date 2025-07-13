from fastapi import APIRouter, HTTPException
from datetime import datetime
import hashlib
import json

from app.models.schemas import VerifyReceiptRequest, VerifyReceiptResponse
from app.services.blockchain import BlockchainLogger
from app.services.supabase_client import get_receipt_data

router = APIRouter()

# Initialize blockchain service
blockchain_logger = BlockchainLogger()

@router.post("/verify-receipt", response_model=VerifyReceiptResponse)
async def verify_receipt(request: VerifyReceiptRequest):
    """
    Verify receipt authenticity using blockchain records
    """
    try:
        # Determine verification method
        if request.qr_data:
            # Parse QR code data
            receipt_data = parse_qr_data(request.qr_data)
            transaction_id = receipt_data.get("transaction_id")
            receipt_hash = receipt_data.get("hash")
        elif request.transaction_id:
            transaction_id = request.transaction_id
            receipt_hash = None
        elif request.receipt_hash:
            receipt_hash = request.receipt_hash
            transaction_id = None
        else:
            raise HTTPException(status_code=400, detail="Must provide QR data, transaction ID, or receipt hash")
        
        # Get receipt data from Supabase
        receipt_record = await get_receipt_data(
            transaction_id=transaction_id,
            receipt_hash=receipt_hash
        )
        
        if not receipt_record:
            return VerifyReceiptResponse(
                is_valid=False,
                transaction_id=transaction_id or "unknown",
                amount=0.0,
                timestamp=datetime.now(),
                store="unknown",
                blockchain_hash="",
                status="not_found",
                confirmations=0
            )
        
        # Verify blockchain record
        blockchain_verified = await verify_blockchain_record(receipt_record)
        
        # Calculate receipt hash if not provided
        if not receipt_hash:
            receipt_hash = calculate_receipt_hash(receipt_record)
        
        response = VerifyReceiptResponse(
            is_valid=blockchain_verified["is_valid"],
            transaction_id=receipt_record["transaction_id"],
            amount=receipt_record["amount"],
            timestamp=receipt_record["timestamp"],
            store=receipt_record["store"],
            blockchain_hash=blockchain_verified["blockchain_hash"],
            status="verified" if blockchain_verified["is_valid"] else "invalid",
            confirmations=blockchain_verified["confirmations"]
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Receipt verification failed: {str(e)}")

@router.get("/verify-receipt/qr-info")
async def get_qr_info():
    """
    Get information about QR code format and requirements
    """
    return {
        "format": "JSON",
        "required_fields": [
            "transaction_id",
            "amount",
            "timestamp",
            "store",
            "hash"
        ],
        "example": {
            "transaction_id": "TXN_001234",
            "amount": 89.99,
            "timestamp": "2024-01-15T14:23:45Z",
            "store": "Store 1523",
            "hash": "0x1234567890abcdef..."
        }
    }

@router.post("/verify-receipt/batch")
async def verify_receipts_batch(receipts: list[VerifyReceiptRequest]):
    """
    Verify multiple receipts in batch
    """
    try:
        results = []
        
        for receipt_request in receipts:
            try:
                result = await verify_receipt(receipt_request)
                results.append(result)
            except Exception as e:
                # Add error result for failed verification
                results.append({
                    "is_valid": False,
                    "error": str(e),
                    "transaction_id": receipt_request.transaction_id or "unknown"
                })
        
        return {
            "results": results,
            "total_processed": len(results),
            "valid_count": sum(1 for r in results if r.get("is_valid", False)),
            "invalid_count": sum(1 for r in results if not r.get("is_valid", False))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch verification failed: {str(e)}")

def parse_qr_data(qr_data: str) -> dict:
    """
    Parse QR code data into receipt information
    """
    try:
        # Assume QR data is JSON format
        return json.loads(qr_data)
    except json.JSONDecodeError:
        # Handle other formats if needed
        raise HTTPException(status_code=400, detail="Invalid QR code format")

def calculate_receipt_hash(receipt_data: dict) -> str:
    """
    Calculate hash for receipt data
    """
    # Create deterministic hash from receipt data
    hash_input = f"{receipt_data['transaction_id']}{receipt_data['amount']}{receipt_data['timestamp']}{receipt_data['store']}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

async def verify_blockchain_record(receipt_record: dict) -> dict:
    """
    Verify receipt against blockchain records
    """
    try:
        # Check if transaction exists on blockchain
        blockchain_record = await blockchain_logger.get_transaction_by_id(
            receipt_record["transaction_id"]
        )
        
        if blockchain_record:
            return {
                "is_valid": True,
                "blockchain_hash": blockchain_record["transaction_hash"],
                "confirmations": blockchain_record.get("confirmations", 0)
            }
        else:
            return {
                "is_valid": False,
                "blockchain_hash": "",
                "confirmations": 0
            }
            
    except Exception:
        return {
            "is_valid": False,
            "blockchain_hash": "",
            "confirmations": 0
        }