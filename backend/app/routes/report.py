from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import uuid
import os

from app.models.schemas import ReportRequest, ReportResponse
from app.services.pdf_generator import PDFReportGenerator
from app.services.supabase_client import get_fraud_analytics_data

router = APIRouter()

# Initialize PDF generator
pdf_generator = PDFReportGenerator()

@router.post("/generate-report", response_model=ReportResponse)
async def generate_fraud_report(request: ReportRequest):
    """
    Generate comprehensive fraud analysis report
    """
    try:
        # Calculate date range
        end_date = request.end_date or datetime.now()
        
        if request.date_range == "1d":
            start_date = end_date - timedelta(days=1)
        elif request.date_range == "7d":
            start_date = end_date - timedelta(days=7)
        elif request.date_range == "30d":
            start_date = end_date - timedelta(days=30)
        elif request.date_range == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = request.start_date or (end_date - timedelta(days=7))
        
        # Get analytics data from Supabase
        analytics_data = await get_fraud_analytics_data(
            start_date=start_date,
            end_date=end_date,
            filters=request.filters
        )
        
        # Generate PDF report
        report_id = str(uuid.uuid4())
        pdf_path = await pdf_generator.generate_report(
            report_type=request.report_type,
            data=analytics_data,
            start_date=start_date,
            end_date=end_date,
            report_id=report_id
        )
        
        # Get file size
        file_size = os.path.getsize(pdf_path)
        file_size_mb = f"{file_size / (1024 * 1024):.2f} MB"
        
        # Generate download URL (in production, this would be a signed URL)
        download_url = f"/api/report/download/{report_id}"
        
        response = ReportResponse(
            report_id=report_id,
            download_url=download_url,
            generated_at=datetime.now(),
            file_size=file_size_mb,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/report/download/{report_id}")
async def download_report(report_id: str):
    """
    Download generated report PDF
    """
    try:
        pdf_path = f"reports/{report_id}.pdf"
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="Report not found or expired")
        
        return FileResponse(
            path=pdf_path,
            filename=f"fraud_report_{report_id}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report download failed: {str(e)}")

@router.get("/report/list")
async def list_reports(limit: int = 20, offset: int = 0):
    """
    List previously generated reports
    """
    try:
        # In production, this would query a reports table in Supabase
        reports = [
            {
                "report_id": "rpt_001",
                "report_type": "summary",
                "generated_at": "2024-01-15T14:00:00",
                "file_size": "2.3 MB",
                "status": "completed"
            },
            {
                "report_id": "rpt_002",
                "report_type": "detailed",
                "generated_at": "2024-01-15T10:30:00",
                "file_size": "4.1 MB",
                "status": "completed"
            }
        ]
        
        return {
            "reports": reports,
            "total": len(reports),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report listing failed: {str(e)}")

@router.delete("/report/{report_id}")
async def delete_report(report_id: str):
    """
    Delete a generated report
    """
    try:
        pdf_path = f"reports/{report_id}.pdf"
        
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            return {"message": f"Report {report_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Report not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report deletion failed: {str(e)}")

@router.get("/report/analytics/summary")
async def get_analytics_summary():
    """
    Get summary analytics for dashboard
    """
    try:
        # This would typically aggregate data from Supabase
        summary = {
            "total_transactions": 245000,
            "fraud_detected": 1247,
            "fraud_rate": 0.51,
            "blocked_users": 342,
            "high_risk_alerts": 89,
            "avg_risk_score": 0.23,
            "top_risk_factors": [
                "Unusual amount",
                "New device",
                "High velocity",
                "Location anomaly"
            ],
            "trend_data": {
                "fraud_rate_trend": "+2.3%",
                "detection_accuracy": "94.2%",
                "false_positive_rate": "3.1%"
            }
        }
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics summary failed: {str(e)}")