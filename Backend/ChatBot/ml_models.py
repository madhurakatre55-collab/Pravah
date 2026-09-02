import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List


class WeatherPredictionModel:
    """
    ML Model for predicting weather-based route safety for NER logistics.
    
    Predicts safety score (0-100) based on:
    - Temperature (°C)
    - Precipitation (mm)
    - Wind Speed (km/h)
    - Visibility (km)
    
    Output: Safety Score 0-100 (higher = safer)
    """
    
    def __init__(self):
        """Initialize the model."""
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/weather_safety_model.pkl"
        self.scaler_path = "models/weather_scaler.pkl"
        self.feature_names = ['temperature', 'precipitation', 'wind_speed', 'visibility']
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the weather safety prediction model.
        
        Args:
            X_train: Training features (N, 4) - [temp, precip, wind, visibility]
            y_train: Training targets (N,) - safety scores 0-100
        """
        print("🔄 Training Weather Safety Prediction Model...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train RandomForest
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print("✅ Weather safety model trained and saved to models/")
        print(f"   Model path: {self.model_path}")
        print(f"   Scaler path: {self.scaler_path}")
    
    def predict(self, weather_data: List[float]) -> float:
        """
        Predict weather safety score for given conditions.
        
        Args:
            weather_data: List of [temperature, precipitation, wind_speed, visibility]
            
        Returns:
            float: Safety score (0-100)
        """
        if self.model is None:
            self.load()
        
        # Scale and predict
        features_scaled = self.scaler.transform([weather_data])
        prediction = self.model.predict(features_scaled)[0]
        
        # Ensure within valid range
        return max(0, min(100, prediction))
    
    def load(self):
        """Load trained model from disk."""
        if not os.path.exists(self.model_path):
            print("⚠️  Model not found at:", self.model_path)
            print("   Please train model first: python train_models.py")
            return False
        
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        print("✅ Weather safety model loaded")
        return True
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get importance scores for each feature.
        
        Returns:
            dict: Feature names mapped to importance scores
        """
        if self.model is None:
            self.load()
        
        importance_dict = {}
        for name, importance in zip(self.feature_names, self.model.feature_importances_):
            importance_dict[name] = float(importance)
        
        return importance_dict
    
    def get_model_info(self) -> dict:
        """Get model information and statistics."""
        if self.model is None:
            self.load()
        
        return {
            "model_type": "RandomForestRegressor",
            "n_estimators": self.model.n_estimators,
            "max_depth": self.model.max_depth,
            "feature_names": self.feature_names,
            "feature_count": len(self.feature_names),
            "model_path": self.model_path,
            "scaler_path": self.scaler_path,
            "status": "Loaded" if self.model is not None else "Not loaded"
        }
