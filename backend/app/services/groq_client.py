import os
from groq import Groq
from typing import Dict, List, Any
import json

class GroqExplainer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("Warning: GROQ_API_KEY not found. Using mock explanations.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
    
    async def generate_explanation(
        self,
        transaction_id: str,
        risk_score: float,
        flags: List[str],
        shap_values: Dict[str, float],
        transaction_data: Dict[str, Any]
    ) -> str:
        """Generate AI-powered explanation for fraud detection"""
        
        if not self.client:
            return self._generate_mock_explanation(risk_score, flags)
        
        try:
            # Prepare context for Groq
            context = self._prepare_context(
                transaction_id, risk_score, flags, shap_values, transaction_data
            )
            
            # Create prompt for Groq
            prompt = self._create_explanation_prompt(context)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert fraud analyst AI assistant. Provide clear, concise explanations for fraud detection decisions. Keep explanations under 100 words and focus on the most important risk factors."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            explanation = response.choices[0].message.content.strip()
            return explanation
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return self._generate_mock_explanation(risk_score, flags)
    
    def _prepare_context(
        self,
        transaction_id: str,
        risk_score: float,
        flags: List[str],
        shap_values: Dict[str, float],
        transaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare context data for explanation generation"""
        
        # Get top contributing factors from SHAP values
        top_factors = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        
        context = {
            "transaction_id": transaction_id,
            "risk_score": risk_score,
            "risk_level": "HIGH" if risk_score >= 0.8 else "MEDIUM" if risk_score >= 0.5 else "LOW",
            "flags": flags,
            "top_factors": top_factors,
            "amount": transaction_data.get("amount", 0),
            "user_id": transaction_data.get("user_id", "unknown"),
            "location": transaction_data.get("location", "unknown"),
            "timestamp": transaction_data.get("timestamp", "unknown")
        }
        
        return context
    
    def _create_explanation_prompt(self, context: Dict[str, Any]) -> str:
        """Create prompt for Groq explanation generation"""
        
        prompt = f"""
Analyze this transaction for fraud risk:

Transaction ID: {context['transaction_id']}
Risk Score: {context['risk_score']:.2f} ({context['risk_level']} RISK)
Amount: ${context['amount']}
Location: {context['location']}

Risk Flags:
{chr(10).join(f"- {flag}" for flag in context['flags'])}

Top Risk Factors (from ML model):
{chr(10).join(f"- {factor}: {value:.3f}" for factor, value in context['top_factors'])}

Provide a clear, concise explanation (1-2 sentences) of why this transaction was flagged for fraud. Focus on the most significant risk factors and what they indicate about potential fraudulent activity.
"""
        
        return prompt
    
    def _generate_mock_explanation(self, risk_score: float, flags: List[str]) -> str:
        """Generate mock explanation when Groq API is not available"""
        
        if risk_score >= 0.9:
            base_explanation = "This transaction shows extremely high fraud risk due to multiple suspicious indicators."
        elif risk_score >= 0.7:
            base_explanation = "This transaction exhibits several concerning patterns that suggest potential fraud."
        elif risk_score >= 0.5:
            base_explanation = "This transaction shows moderate risk factors that warrant additional scrutiny."
        else:
            base_explanation = "This transaction appears normal with minimal risk indicators."
        
        # Add specific flag explanations
        flag_explanations = {
            "Large transaction amount": "The transaction amount significantly exceeds typical spending patterns",
            "Unusual amount for user": "This amount is highly unusual compared to the user's historical behavior",
            "High transaction velocity": "Multiple transactions in a short timeframe suggest potential card testing",
            "New device detected": "The transaction originated from an unrecognized device",
            "Unusual location": "The transaction location is inconsistent with normal user patterns",
            "Unusual transaction time": "The transaction occurred outside normal business hours",
            "Weekend transaction": "Weekend activity may indicate higher risk depending on user patterns"
        }
        
        relevant_explanations = [flag_explanations.get(flag, flag) for flag in flags[:2]]
        
        if relevant_explanations:
            detailed_explanation = f"{base_explanation} {' '.join(relevant_explanations[:2])}."
        else:
            detailed_explanation = base_explanation
        
        return detailed_explanation

    async def generate_analyst_response(self, question: str, context: Dict[str, Any]) -> str:
        """Generate response for analyst Q&A"""
        
        if not self.client:
            return "I'm sorry, but the AI explanation service is currently unavailable. Please check your Groq API configuration."
        
        try:
            prompt = f"""
You are an expert fraud analyst AI assistant helping with fraud investigation.

Context:
- Current fraud detection system data
- Recent transaction patterns
- Risk assessment models

Question: {question}

Provide a helpful, accurate response based on fraud detection best practices. Keep responses concise and actionable.
"""
            
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert fraud analyst AI assistant. Provide helpful, accurate information about fraud detection, risk assessment, and investigation techniques."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating analyst response: {e}")
            return "I apologize, but I'm unable to process your question at the moment. Please try again later."