import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import shap

from app.models.schemas import ScoreRequest

class FraudMLEngine:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'amount', 'hour', 'day_of_week', 'is_weekend',
            'amount_zscore', 'velocity_1h', 'velocity_24h',
            'new_device', 'location_risk', 'merchant_risk',
            'user_age_days', 'avg_transaction_amount',
            'transaction_frequency', 'refund_ratio', 'failed_attempts'
        ]
        self.load_model()
        
    def load_model(self):
        """Load pre-trained fraud detection model"""
        model_path = "models/fraud_model.pkl"
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            # Create and train a dummy model for demo
            self.model = self._create_dummy_model()
            # Save the dummy model
            os.makedirs("models", exist_ok=True)
            joblib.dump(self.model, model_path)
    
    def _create_dummy_model(self):
        """Create a dummy model for demonstration"""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 10000
        
        # Create features
        X = np.random.randn(n_samples, len(self.feature_names))
        
        # Create labels with some logic
        y = np.zeros(n_samples)
        
        # High amounts are more likely to be fraud
        y[X[:, 0] > 2] = 1
        
        # Weekend transactions are slightly more risky
        y[X[:, 3] > 0.5] = np.random.choice([0, 1], size=np.sum(X[:, 3] > 0.5), p=[0.8, 0.2])
        
        # High velocity is risky
        y[X[:, 5] > 1.5] = 1
        y[X[:, 6] > 1.5] = 1
        
        # New devices are risky
        y[X[:, 7] > 0.5] = np.random.choice([0, 1], size=np.sum(X[:, 7] > 0.5), p=[0.7, 0.3])
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        return model
    
    def extract_features(self, request: ScoreRequest) -> np.ndarray:
        """Extract features from transaction request"""
        timestamp = request.timestamp or datetime.now()
        
        features = {
            'amount': request.amount,
            'hour': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'is_weekend': 1 if timestamp.weekday() >= 5 else 0,
            'amount_zscore': self._calculate_amount_zscore(request.user_id, request.amount),
            'velocity_1h': self._calculate_velocity(request.user_id, hours=1),
            'velocity_24h': self._calculate_velocity(request.user_id, hours=24),
            'new_device': 1 if self._is_new_device(request.user_id, request.device_id) else 0,
            'location_risk': self._calculate_location_risk(request.user_id, request.location),
            'merchant_risk': self._calculate_merchant_risk(request.location),
            'user_age_days': self._get_user_age_days(request.user_id),
            'avg_transaction_amount': self._get_avg_transaction_amount(request.user_id),
            'transaction_frequency': self._get_transaction_frequency(request.user_id),
            'refund_ratio': self._get_refund_ratio(request.user_id),
            'failed_attempts': self._get_failed_attempts(request.user_id)
        }
        
        # Convert to numpy array in correct order
        feature_array = np.array([features[name] for name in self.feature_names]).reshape(1, -1)
        
        return feature_array
    
    def predict_fraud_probability(self, features: np.ndarray) -> float:
        """Predict fraud probability for given features"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Get probability of fraud (class 1)
        prob = self.model.predict_proba(features)[0, 1]
        return float(prob)
    
    def get_prediction_confidence(self, features: np.ndarray) -> float:
        """Get confidence score for prediction"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Use the maximum probability as confidence
        probs = self.model.predict_proba(features)[0]
        confidence = float(np.max(probs))
        return confidence
    
    def generate_flags(self, request: ScoreRequest, risk_score: float) -> List[str]:
        """Generate human-readable flags based on features and risk score"""
        flags = []
        
        # Amount-based flags
        if request.amount > 1000:
            flags.append("Large transaction amount")
        
        amount_zscore = self._calculate_amount_zscore(request.user_id, request.amount)
        if amount_zscore > 2:
            flags.append("Unusual amount for user")
        
        # Velocity flags
        velocity_1h = self._calculate_velocity(request.user_id, hours=1)
        if velocity_1h > 3:
            flags.append("High transaction velocity")
        
        # Device flags
        if self._is_new_device(request.user_id, request.device_id):
            flags.append("New device detected")
        
        # Location flags
        location_risk = self._calculate_location_risk(request.user_id, request.location)
        if location_risk > 0.7:
            flags.append("Unusual location")
        
        # Time-based flags
        timestamp = request.timestamp or datetime.now()
        if timestamp.hour < 6 or timestamp.hour > 23:
            flags.append("Unusual transaction time")
        
        if timestamp.weekday() >= 5:  # Weekend
            flags.append("Weekend transaction")
        
        return flags
    
    def get_shap_explanation(self, transaction_data: Dict[str, Any]) -> Dict[str, float]:
        """Get SHAP explanation for feature importance"""
        # For demo purposes, return mock SHAP values
        # In production, you would use actual SHAP explainer
        mock_shap_values = {
            'amount': np.random.uniform(-0.1, 0.3),
            'hour': np.random.uniform(-0.05, 0.05),
            'day_of_week': np.random.uniform(-0.02, 0.02),
            'is_weekend': np.random.uniform(-0.03, 0.03),
            'amount_zscore': np.random.uniform(-0.1, 0.4),
            'velocity_1h': np.random.uniform(-0.05, 0.2),
            'velocity_24h': np.random.uniform(-0.05, 0.15),
            'new_device': np.random.uniform(-0.02, 0.1),
            'location_risk': np.random.uniform(-0.05, 0.2),
            'merchant_risk': np.random.uniform(-0.03, 0.1)
        }
        
        return mock_shap_values
    
    def get_top_risk_factors(self, shap_values: Dict[str, float], top_k: int = 5) -> List[str]:
        """Get top risk factors from SHAP values"""
        # Sort by absolute SHAP value
        sorted_factors = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)
        
        # Convert to human-readable descriptions
        factor_descriptions = {
            'amount': 'Transaction amount',
            'amount_zscore': 'Amount compared to user history',
            'velocity_1h': 'Recent transaction frequency',
            'velocity_24h': 'Daily transaction frequency',
            'new_device': 'Device recognition',
            'location_risk': 'Location analysis',
            'merchant_risk': 'Merchant risk profile',
            'hour': 'Time of transaction',
            'is_weekend': 'Weekend activity',
            'day_of_week': 'Day of week pattern'
        }
        
        top_factors = []
        for factor, value in sorted_factors[:top_k]:
            description = factor_descriptions.get(factor, factor)
            impact = "increases" if value > 0 else "decreases"
            top_factors.append(f"{description} {impact} risk")
        
        return top_factors
    
    # Helper methods for feature calculation (mock implementations)
    def _calculate_amount_zscore(self, user_id: str, amount: float) -> float:
        """Calculate z-score for transaction amount"""
        # Mock implementation - in production, query user's transaction history
        user_avg = 150.0  # Mock average
        user_std = 75.0   # Mock standard deviation
        return (amount - user_avg) / user_std if user_std > 0 else 0
    
    def _calculate_velocity(self, user_id: str, hours: int) -> int:
        """Calculate transaction velocity"""
        # Mock implementation
        return np.random.randint(0, 5)
    
    def _is_new_device(self, user_id: str, device_id: str) -> bool:
        """Check if device is new for user"""
        # Mock implementation
        return np.random.choice([True, False], p=[0.2, 0.8])
    
    def _calculate_location_risk(self, user_id: str, location: str) -> float:
        """Calculate location risk score"""
        # Mock implementation
        return np.random.uniform(0, 1)
    
    def _calculate_merchant_risk(self, location: str) -> float:
        """Calculate merchant risk score"""
        # Mock implementation
        return np.random.uniform(0, 0.5)
    
    def _get_user_age_days(self, user_id: str) -> int:
        """Get user account age in days"""
        # Mock implementation
        return np.random.randint(1, 1000)
    
    def _get_avg_transaction_amount(self, user_id: str) -> float:
        """Get user's average transaction amount"""
        # Mock implementation
        return np.random.uniform(50, 300)
    
    def _get_transaction_frequency(self, user_id: str) -> float:
        """Get user's transaction frequency"""
        # Mock implementation
        return np.random.uniform(0.1, 5.0)
    
    def _get_refund_ratio(self, user_id: str) -> float:
        """Get user's refund ratio"""
        # Mock implementation
        return np.random.uniform(0, 0.2)
    
    def _get_failed_attempts(self, user_id: str) -> int:
        """Get recent failed payment attempts"""
        # Mock implementation
        return np.random.randint(0, 3)