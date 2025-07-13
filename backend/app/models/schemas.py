from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    BLOCKED = "blocked"
    UNDER_REVIEW = "under_review"

# Upload Models
class TransactionData(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    timestamp: datetime
    location: str
    device_id: Optional[str] = None
    payment_method: Optional[str] = None
    merchant_category: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    total_records: int
    columns: List[str]
    preview: List[Dict[str, Any]]
    file_id: str

# Scoring Models
class ScoreRequest(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    location: str
    device_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class ScoreResponse(BaseModel):
    transaction_id: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    flags: List[str]
    confidence: float
    model_version: str

# Explanation Models
class ExplanationRequest(BaseModel):
    transaction_id: str
    risk_score: float
    flags: List[str]
    transaction_data: Dict[str, Any]

class ExplanationResponse(BaseModel):
    transaction_id: str
    explanation: str
    key_factors: List[str]
    recommendations: List[str]
    generated_at: datetime

# Blocklist Models
class BlockUserRequest(BaseModel):
    user_id: str
    device_id: Optional[str] = None
    reason: str
    risk_score: float
    blocked_by: str
    block_type: str = "permanent"  # permanent, temporary, under_review

class BlockUserResponse(BaseModel):
    success: bool
    message: str
    block_id: str
    blocked_at: datetime

class BlockedUser(BaseModel):
    id: str
    user_id: str
    device_id: Optional[str]
    reason: str
    risk_score: float
    blocked_by: str
    blocked_at: datetime
    status: str

# Blockchain Models
class BlockchainLogRequest(BaseModel):
    user_id_hash: str
    risk_score: float
    action: str
    metadata: Optional[Dict[str, Any]] = None

class BlockchainLogResponse(BaseModel):
    success: bool
    transaction_hash: str
    block_number: Optional[int]
    gas_used: Optional[int]
    logged_at: datetime

# Report Models
class ReportRequest(BaseModel):
    report_type: str = "summary"  # summary, detailed, blockchain, user-risk
    date_range: str = "7d"  # 1d, 7d, 30d, 90d, custom
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    filters: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    report_id: str
    download_url: str
    generated_at: datetime
    file_size: str
    expires_at: datetime

# Verification Models
class VerifyReceiptRequest(BaseModel):
    receipt_hash: Optional[str] = None
    transaction_id: Optional[str] = None
    qr_data: Optional[str] = None

class VerifyReceiptResponse(BaseModel):
    is_valid: bool
    transaction_id: str
    amount: float
    timestamp: datetime
    store: str
    blockchain_hash: str
    status: str
    confirmations: int

# General Response Models
class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime

class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None