from fastapi import APIRouter, HTTPException
from datetime import datetime
import numpy as np
from typing import List

from app.models.schemas import ScoreRequest, ScoreResponse, RiskLevel
from app.services.ml_engine import FraudMLEngine
from app.services.supabase_client import save_fraud_score

router = APIRouter()

# Initialize ML engine
ml_engine = FraudMLEngine()

@router.post("/score", response_model=ScoreResponse)
async def score_transaction(request: ScoreRequest):
    """
    Score a transaction for fraud risk using ML model
    """
    try:
        # Extract features for ML model
        features = ml_engine.extract_features(request)
        
        # Get risk score from ML model
        risk_score = ml_engine.predict_fraud_probability(features)
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.5:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Generate flags based on rules and model
        flags = ml_engine.generate_flags(request, risk_score)
        
        # Calculate confidence
        confidence = ml_engine.get_prediction_confidence(features)
        
        # Prepare response
        response = ScoreResponse(
            transaction_id=request.transaction_id,
            risk_score=float(risk_score),
            risk_level=risk_level,
            flags=flags,
            confidence=float(confidence),
            model_version="v1.2.0"
        )
        
        # Save score to database
        await save_fraud_score(response)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@router.post("/score/batch")
async def score_transactions_batch(transactions: List[ScoreRequest]):
    """
    Score multiple transactions in batch for efficiency
    """
    try:
        results = []
        
        for transaction in transactions:
            # Process each transaction
            features = ml_engine.extract_features(transaction)
            risk_score = ml_engine.predict_fraud_probability(features)
            
            # Determine risk level
            if risk_score >= 0.8:
                risk_level = RiskLevel.HIGH
            elif risk_score >= 0.5:
                risk_level = RiskLevel.MEDIUM
            else:
                risk_level = RiskLevel.LOW
            
            flags = ml_engine.generate_flags(transaction, risk_score)
            confidence = ml_engine.get_prediction_confidence(features)
            
            result = ScoreResponse(
                transaction_id=transaction.transaction_id,
                risk_score=float(risk_score),
                risk_level=risk_level,
                flags=flags,
                confidence=float(confidence),
                model_version="v1.2.0"
            )
            
            results.append(result)
        
        # Save all scores to database
        for result in results:
            await save_fraud_score(result)
        
        return {"results": results, "total_processed": len(results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch scoring failed: {str(e)}")

@router.get("/score/model-info")
async def get_model_info():
    """
    Get information about the current ML model
    """
    return {
        "model_version": "v1.2.0",
        "model_type": "XGBoost Classifier",
        "features_count": 15,
        "training_date": "2024-01-10",
        "accuracy": 0.94,
        "precision": 0.91,
        "recall": 0.89,
        "f1_score": 0.90
    }