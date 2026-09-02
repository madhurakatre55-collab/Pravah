import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import Dict, List, Tuple


class WeatherPredictionMode cl: 
        self.model = None
        self.scaler = StandardScaler()    
        self.model_path = "models/weather_predictor.pkl"
        self.scaler_path = "models/weather_scaler.pkl"
        self.feature_names = ['temperature', 'precipitation', 'wind_speed', 'visibility']
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the model with historical weather data.
        
        Args:
            X_train: Features array (temperature, precipitation, wind_speed, visibility)
            y_train: Target array (safety scores 0-100)
        """
        print(" Training Weather Prediction Model...")
        X_scaled = self.scaler.fit_transform(X_train)
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model and scaler
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print(" Weather prediction model trained and saved")
    
    def predict(self, weather_data: List[float]) -> float:
        """
        Predict route safety from weather conditions.
        
        Args:
            weather_data: List of [temperature, precipitation, wind_speed, visibility]
            
        Returns:
            float: Safety score (0-100)
        """
        if self.model is None:
            self.load()
        
        features_scaled = self.scaler.transform([weather_data])
        prediction = self.model.predict(features_scaled)
        return prediction[0]
    
    def load(self):
        """Load trained model and scaler"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print(" Weather model loaded")
        else:
            print(" Model not found. Train model first using train_models.py")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if self.model is None:
            self.load()
        
        importance = {}
        for name, score in zip(self.feature_names, self.model.feature_importances_):
            importance[name] = float(score)
        
        return importance


class RouteRiskClassifier:
    """ML model for classifying route risk levels"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/route_risk_classifier.pkl"
        self.scaler_path = "models/route_scaler.pkl"
        self.feature_names = ['congestion_level', 'weather_severity', 'accident_proximity', 'road_condition']
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the model with historical route risk data.
        
        Args:
            X_train: Features array (congestion, weather, accidents, road condition)
            y_train: Target array (0=low, 1=medium, 2=high risk)
        """
        print(" Training Route Risk Classifier...")
        X_scaled = self.scaler.fit_transform(X_train)
        
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model and scaler
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print(" Route risk classifier trained and saved")
    
    def predict(self, route_data: List[float]) -> Tuple[str, float]:
        """
        Predict route risk level.
        
        Args:
            route_data: List of [congestion, weather, accidents, road_condition]
            
        Returns:
            Tuple of (risk_level, probability)
        """
        if self.model is None:
            self.load()
        
        features_scaled = self.scaler.transform([route_data])
        prediction = self.model.predict(features_scaled)[0]
        probability = np.max(self.model.predict_proba(features_scaled))
        
        risk_levels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        return risk_levels[prediction], float(probability)
    
    def load(self):
        """Load trained model and scaler"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print(" Route risk classifier loaded")
        else:
            print(" Model not found. Train model first using train_models.py")


class TravelTimePredictor:
    """ML model for predicting travel time"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/travel_time_predictor.pkl"
        self.scaler_path = "models/time_scaler.pkl"
        self.feature_names = ['distance', 'congestion', 'weather_impact', 'time_of_day']
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the model with historical travel time data.
        
        Args:
            X_train: Features array (distance, congestion, weather, time)
            y_train: Target array (travel time in minutes)
        """
        print(" Training Travel Time Predictor...")
        X_scaled = self.scaler.fit_transform(X_train)
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y_train)
        
        # Save model and scaler
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("  Travel time predictor trained and saved")
    
    def predict(self, route_data: List[float]) -> float:
        """
        Predict travel time.
        
        Args:
            route_data: List of [distance, congestion, weather_impact, time_of_day]
            
        Returns:
            float: Predicted travel time in minutes
        """
        if self.model is None:
            self.load()
        
        features_scaled = self.scaler.transform([route_data])
        prediction = self.model.predict(features_scaled)
        return max(0, prediction[0])  # Ensure non-negative time
    
    def load(self):
        """Load trained model and scaler"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print(" Travel time predictor loaded")
        else:
            print(" Model not found. Train model first using train_models.py")
