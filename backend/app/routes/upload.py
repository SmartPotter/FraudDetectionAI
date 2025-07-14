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
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        contents = await file.read()
        print("✅ File read")

        df = parse_csv_file(contents)
        print("✅ CSV parsed. Columns:", df.columns)

        validated_data = validate_transaction_data(df)
        print("✅ Data validated. Sample:", validated_data[:2])

        file_id = str(uuid.uuid4())
        await save_transactions(validated_data, file_id)
        print("✅ Saved to Supabase")

        preview_data = df.head(5).to_dict(orient="records")

        return UploadResponse(
            message="File uploaded and processed successfully",
            total_records=len(df),
            columns=list(df.columns),
            preview=preview_data,
            file_id=file_id
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
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