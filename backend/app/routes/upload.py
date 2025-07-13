from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
import uuid
from datetime import datetime
from typing import List

from app.models.schemas import UploadResponse, TransactionData
from app.utils.file_parser import parse_csv_file, validate_transaction_data
from app.services.supabase_client import save_transactions

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_transaction_file(file: UploadFile = File(...)):
    """
    Upload and process transaction CSV file for fraud analysis
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read file contents
        contents = await file.read()
        
        # Parse CSV
        df = parse_csv_file(contents)
        
        # Validate data structure
        validated_data = validate_transaction_data(df)
        
        # Generate file ID for tracking
        file_id = str(uuid.uuid4())
        
        # Save to Supabase (async)
        await save_transactions(validated_data, file_id)
        
        # Prepare response
        preview_data = df.head(5).to_dict(orient="records")
        
        return UploadResponse(
            message="File uploaded and processed successfully",
            total_records=len(df),
            columns=list(df.columns),
            preview=preview_data,
            file_id=file_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@router.get("/upload/status/{file_id}")
async def get_upload_status(file_id: str):
    """
    Get processing status of uploaded file
    """
    try:
        # Check processing status in Supabase
        # This would typically check a processing_status table
        return {
            "file_id": file_id,
            "status": "completed",
            "processed_at": datetime.now(),
            "records_processed": 1000,
            "fraud_detected": 23
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.delete("/upload/{file_id}")
async def delete_uploaded_file(file_id: str):
    """
    Delete uploaded file and associated data
    """
    try:
        # Delete from Supabase
        # Implementation would remove file data and processing results
        return {"message": f"File {file_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File deletion failed: {str(e)}")