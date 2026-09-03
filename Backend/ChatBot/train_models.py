import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from ml_models import WeatherPredictionModel, RouteRiskClassifier

# Set stdout encoding for Windows compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def generate_sample_weather_data(n_samples: int = 1000) -> tuple:
    """
    Generate sample NER weather training data.
    
    In production, use IMD/Kaggle historical data:
    - IMD: https://mausam.imd.gov.in/
    - Kaggle: https://kaggle.com/datasets?search=india+weather
    """
    print(f"[DATA] Generating {n_samples} sample NER weather records...")
    
    np.random.seed(42)
    temperatures = np.random.uniform(5, 35, n_samples)          # 5-35°C (NER range)
    precipitation = np.random.exponential(8, n_samples)         # 0-100+ mm (monsoon region)
    wind_speeds = np.random.gamma(2, 2.5, n_samples)            # 0-40 km/h
    visibility = np.random.uniform(0.5, 15, n_samples)          # 0.5-15 km
    
    X = np.column_stack([temperatures, precipitation, wind_speeds, visibility])
    
    # Calculate safety score (0-100)
    safety_score = 100 - (
        (np.abs(temperatures - 22) / 35) * 10 +
        (precipitation / 120) * 40 +
        (wind_speeds / 40) * 20 +
        ((15 - visibility) / 15) * 30
    )
    
    safety_score += np.random.normal(0, 5, n_samples)
    safety_score = np.clip(safety_score, 0, 100)
    
    return X, safety_score


def generate_sample_route_risk_data(n_samples: int = 1000) -> tuple:
    """
    Generate sample NER route risk classification training data.
    Features: [congestion_percent, weather_severity, hazard_proximity_km, road_condition_rating]
    Targets: 0 (LOW), 1 (MODERATE), 2 (HIGH), 3 (CRITICAL)
    """
    print(f"[DATA] Generating {n_samples} sample NER route risk records...")
    
    np.random.seed(100)
    congestion = np.random.uniform(5, 95, n_samples)            # 5-95%
    weather_severity = np.random.uniform(0, 10, n_samples)      # 0-10 index
    hazard_proximity = np.random.exponential(15, n_samples)     # distance in km
    road_condition = np.random.uniform(10, 100, n_samples)      # 10-100 rating
    
    X = np.column_stack([congestion, weather_severity, hazard_proximity, road_condition])
    
    y = []
    for c, w, h, r in X:
        if h < 2.0 or w > 8.0:
            y.append(3) # CRITICAL
        elif h < 8.0 or w > 5.5 or r < 30:
            y.append(2) # HIGH
        elif c > 50 or r < 60:
            y.append(1) # MODERATE
        else:
            y.append(0) # LOW
            
    return X, np.array(y)


def train_all_models():
    """
    Main training routine for Chatbot ML models.
    """
    print("=" * 70)
    print("TRAINING CHATBOT ML MODELS (SIH 2026)")
    print("=" * 70)
    print()
    
    # 1. WEATHER PREDICTION MODEL
    print("STEP 1: Training Weather Safety Prediction Model")
    print("-" * 70)
    X_w, y_w = generate_sample_weather_data(n_samples=1000)
    X_w_train, X_w_test, y_w_train, y_w_test = train_test_split(X_w, y_w, test_size=0.2, random_state=42)
    
    weather_model = WeatherPredictionModel()
    weather_model.train(X_w_train, y_w_train)
    
    r2_score = weather_model.model.score(weather_model.scaler.transform(X_w_test), y_w_test)
    print(f"[SUCCESS] Weather Safety Model Test R^2 Score: {r2_score:.4f}\n")
    
    # 2. ROUTE RISK CLASSIFIER
    print("STEP 2: Training Route Risk Classifier")
    print("-" * 70)
    X_r, y_r = generate_sample_route_risk_data(n_samples=1000)
    X_r_train, X_r_test, y_r_train, y_r_test = train_test_split(X_r, y_r, test_size=0.2, random_state=42)
    
    route_model = RouteRiskClassifier()
    route_model.train(X_r_train, y_r_train)
    
    acc_score = route_model.model.score(route_model.scaler.transform(X_r_test), y_r_test)
    print(f"[SUCCESS] Route Risk Classifier Test Accuracy: {acc_score * 100:.2f}%\n")
    
    print("=" * 70)
    print("ALL MODELS TRAINED AND SAVED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    train_all_models()
