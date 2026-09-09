import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List


class WeatherPredictionModel:
    """Weather safety prediction model."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(base_dir, "models")
        self.model_path = os.path.join(self.model_dir, "weather_safety_model.pkl")
        self.scaler_path = os.path.join(self.model_dir, "weather_scaler.pkl")
        self.feature_names = ['temperature', 'precipitation', 'wind_speed', 'visibility']
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train weather model."""
        print("[INFO] Training Weather Safety Prediction Model...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("[INFO] Weather safety model trained and saved to models/")
    
    def predict(self, weather_data: List[float]) -> float:
        """Predict safety score."""
        if self.model is None:
            if not self.load():
                # Rule-based fallback
                temp, precip, wind, vis = weather_data
                fallback_score = 100 - (precip * 0.5 + wind * 0.8 + (15 - vis) * 3)
                return float(max(0, min(100, fallback_score)))
        
        # Scale and predict
        features_scaled = self.scaler.transform([weather_data])
        prediction = self.model.predict(features_scaled)[0]
        
        # Clamp bounds
        return float(max(0, min(100, prediction)))
    
    def load(self) -> bool:
        """Load model files."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.scaler_path):
            print("[WARN] Weather model not found at:", self.model_path)
            return False
        
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        print("[INFO] Weather safety model loaded successfully")
        return True
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importances."""
        if self.model is None:
            self.load()
        
        if self.model is None:
            return {}
            
        importance_dict = {}
        for name, importance in zip(self.feature_names, self.model.feature_importances_):
            importance_dict[name] = float(importance)
        return importance_dict
    
    def get_model_info(self) -> dict:
        """Get model metadata."""
        if self.model is None:
            self.load()
        
        return {
            "model_type": "RandomForestRegressor",
            "n_estimators": self.model.n_estimators if self.model else 100,
            "max_depth": self.model.max_depth if self.model else 10,
            "feature_names": self.feature_names,
            "feature_count": len(self.feature_names),
            "model_path": self.model_path,
            "scaler_path": self.scaler_path,
            "status": "Loaded" if self.model is not None else "Not loaded"
        }
