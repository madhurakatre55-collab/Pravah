import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
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


class RouteRiskClassifier:
    """Route risk classifier."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(base_dir, "models")
        self.model_path = os.path.join(self.model_dir, "route_risk_classifier.pkl")
        self.scaler_path = os.path.join(self.model_dir, "route_scaler.pkl")
        self.feature_names = ['congestion_percent', 'weather_severity', 'hazard_proximity_km', 'road_condition_rating']
        self.risk_labels = {0: "LOW", 1: "MODERATE", 2: "HIGH", 3: "CRITICAL"}
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train classifier."""
        print("[INFO] Training Route Risk Classifier...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("[INFO] Route risk classifier trained and saved to models/")
    
    def predict(self, route_data: List[float]) -> dict:
        """Predict risk level."""
        if self.model is None:
            if not self.load():
                # Fallback estimation
                congestion, weather_sev, hazard_prox, road_cond = route_data
                if hazard_prox < 2.0 or weather_sev > 8:
                    return {"risk_code": 3, "risk_label": "CRITICAL", "confidence": 0.90}
                elif hazard_prox < 10.0 or weather_sev > 5:
                    return {"risk_code": 2, "risk_label": "HIGH", "confidence": 0.85}
                elif congestion > 60 or road_cond < 40:
                    return {"risk_code": 1, "risk_label": "MODERATE", "confidence": 0.80}
                else:
                    return {"risk_code": 0, "risk_label": "LOW", "confidence": 0.95}
        
        # Scale and predict
        X_scaled = self.scaler.transform([route_data])
        risk_code = int(self.model.predict(X_scaled)[0])
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = float(np.max(probabilities))
        
        return {
            "risk_code": risk_code,
            "risk_label": self.risk_labels.get(risk_code, "UNKNOWN"),
            "confidence": round(confidence, 4),
            "feature_inputs": {
                "congestion_percent": route_data[0],
                "weather_severity": route_data[1],
                "hazard_proximity_km": route_data[2],
                "road_condition_rating": route_data[3]
            }
        }
    
    def load(self) -> bool:
        """Load classifier files."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.scaler_path):
            print("[WARN] Route risk classifier not found at:", self.model_path)
            return False
        
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        print("[INFO] Route risk classifier loaded successfully")
        return True
