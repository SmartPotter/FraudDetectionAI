from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models.schemas import ExplanationRequest, ExplanationResponse
from app.services.groq_client import GroqExplainer
from app.services.ml_engine import FraudMLEngine

router = APIRouter()

# Initialize services
groq_explainer = GroqExplainer()
ml_engine = FraudMLEngine()

@router.post("/explain", response_model=ExplanationResponse)
async def explain_fraud_decision(request: ExplanationRequest):
    """
    Generate AI-powered explanation for fraud detection decision
    """
    try:
        # Get SHAP values for feature importance
        shap_explanation = ml_engine.get_shap_explanation(request.transaction_data)
        
        # Generate human-readable explanation using Groq
        ai_explanation = await groq_explainer.generate_explanation(
            transaction_id=request.transaction_id,
            risk_score=request.risk_score,
            flags=request.flags,
            shap_values=shap_explanation,
            transaction_data=request.transaction_data
        )
        
        # Extract key factors from SHAP analysis
        key_factors = ml_engine.get_top_risk_factors(shap_explanation)
        
        # Generate recommendations
        recommendations = generate_recommendations(request.risk_score, request.flags)
        
        response = ExplanationResponse(
            transaction_id=request.transaction_id,
            explanation=ai_explanation,
            key_factors=key_factors,
            recommendations=recommendations,
            generated_at=datetime.now()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation generation failed: {str(e)}")

@router.get("/explain/templates")
async def get_explanation_templates():
    """
    Get available explanation templates for different fraud types
    """
    return {
        "high_amount": "This transaction was flagged due to an unusually high amount compared to the user's typical spending pattern.",
        "new_device": "The transaction originated from a device not previously associated with this user account.",
        "velocity": "Multiple transactions were detected in a short time period, indicating potential card testing or fraud.",
        "location_anomaly": "The transaction location is inconsistent with the user's typical geographic patterns.",
        "time_anomaly": "The transaction occurred at an unusual time for this user's typical activity.",
        "refund_pattern": "Suspicious refund activity detected that may indicate return fraud."
    }

def generate_recommendations(risk_score: float, flags: list) -> list:
    """
    Generate actionable recommendations based on risk factors
    """
    recommendations = []
    
    if risk_score >= 0.9:
        recommendations.append("Immediately block user and flag for manual review")
        recommendations.append("Contact user via verified phone number to confirm transaction")
    elif risk_score >= 0.7:
        recommendations.append("Require additional authentication before processing")
        recommendations.append("Monitor user activity closely for next 24 hours")
    elif risk_score >= 0.5:
        recommendations.append("Apply enhanced monitoring to user account")
        recommendations.append("Consider step-up authentication for large transactions")
    
    # Flag-specific recommendations
    if "unusual_amount" in flags:
        recommendations.append("Verify transaction with user via SMS or email")
    if "new_device" in flags:
        recommendations.append("Require device verification before processing")
    if "high_velocity" in flags:
        recommendations.append("Implement temporary transaction limits")
    
    return recommendations