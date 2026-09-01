import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from ml_models import WeatherPredictionModel, RouteRiskClassifier, TravelTimePredictor


def generate_sample_weather_data(n_samples: int = 500) -> tuple:
    """
    Generate sample weather data for training (or use real dataset).
    
    Real datasets to use:
    - OpenWeatherMap Historical API
    - Kaggle Weather Datasets
    - NOAA Weather Data
    - Weather Underground API
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (X, y) - features and targets
    """
    print(f"📊 Generating {n_samples} sample weather records...")
    
    np.random.seed(42)
    
    # Features: [temperature, precipitation, wind_speed, visibility]
    temperatures = np.random.uniform(-10, 40, n_samples)  # °C
    precipitation = np.random.exponential(2, n_samples)   # mm
    wind_speeds = np.random.gamma(2, 2, n_samples)       # km/h
    visibility = np.random.uniform(1, 15, n_samples)      # km
    
    X = np.column_stack([temperatures, precipitation, wind_speeds, visibility])
    
    # Target: Safety score (0-100) - higher is safer
    # Calculate based on conditions
    safety_score = 100 - (
        (np.abs(temperatures - 20) / 40) * 15 +  # Comfort temperature ~20°C
        (precipitation / 20) * 25 +               # Heavy rain reduces safety
        (wind_speeds / 20) * 20 +                 # High winds reduce safety
        ((15 - visibility) / 15) * 25             # Low visibility reduces safety
    )
    
    # Add some noise
    safety_score += np.random.normal(0, 5, n_samples)
    safety_score = np.clip(safety_score, 0, 100)
    
    y = safety_score
    
    print(f"✅ Generated features shape: {X.shape}, targets shape: {y.shape}")
    return X, y


def generate_sample_route_data(n_samples: int = 400) -> tuple:
    """
    Generate sample route risk data for training.
    
    Real datasets to use:
    - Google Maps API (historical traffic)
    - TomTom Traffic Data
    - HERE Real-Time Traffic
    - NHTSA Accident Data
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (X, y) - features and targets
    """
    print(f"📊 Generating {n_samples} sample route risk records...")
    
    np.random.seed(42)
    
    # Features: [congestion_level, weather_severity, accident_proximity, road_condition]
    congestion = np.random.uniform(0, 100, n_samples)     # 0-100%
    weather_severity = np.random.uniform(0, 10, n_samples) # 0-10
    accident_proximity = np.random.exponential(5, n_samples) # km
    road_condition = np.random.uniform(0, 100, n_samples)  # 0-100% (higher = better)
    
    X = np.column_stack([congestion, weather_severity, accident_proximity, road_condition])
    
    # Target: Risk level (0=low, 1=medium, 2=high)
    risk_score = (
        (congestion / 100) * 0.4 +
        (weather_severity / 10) * 0.3 +
        (1 - accident_proximity / 30) * 0.2 +
        (1 - road_condition / 100) * 0.1
    )
    
    # Classify into risk levels
    y = np.digitize(risk_score, bins=[0.33, 0.67]) 
    
    print(f"✅ Generated features shape: {X.shape}, targets shape: {y.shape}")
    return X, y


def generate_sample_travel_time_data(n_samples: int = 600) -> tuple:
    """
    Generate sample travel time data for training.
    
    Real datasets to use:
    - Google Maps API (historical travel times)
    - TomTom Historical Traffic
    - Waze Routing Data
    - OpenStreetMap Route Data
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (X, y) - features and targets
    """
    print(f"📊 Generating {n_samples} sample travel time records...")
    
    np.random.seed(42)
    
    # Features: [distance, congestion, weather_impact, time_of_day]
    distances = np.random.gamma(20, 1.5, n_samples)        # km
    congestion = np.random.uniform(0, 100, n_samples)      # 0-100%
    weather_impact = np.random.exponential(1, n_samples)   # 0-5
    time_of_day = np.random.uniform(0, 24, n_samples)      # 0-24 hours
    
    X = np.column_stack([distances, congestion, weather_impact, time_of_day])
    
    # Target: Travel time (minutes)
    base_time = distances / 50  # Base speed ~50 km/h
    congestion_factor = 1 + (congestion / 100) * 1.5  # Up to 2.5x slower
    weather_factor = 1 + (weather_impact / 5) * 0.5  # Up to 1.5x slower
    
    # Rush hour factor (8-10am, 5-7pm)
    rush_hour_factor = np.where(
        ((time_of_day >= 8) & (time_of_day <= 10)) | 
        ((time_of_day >= 17) & (time_of_day <= 19)),
        1.3,
        1.0
    )
    
    y = base_time * congestion_factor * weather_factor * rush_hour_factor
    y += np.random.normal(0, 2, n_samples)  # Add noise
    y = np.maximum(y, base_time)  # Minimum is base time
    
    print(f"✅ Generated features shape: {X.shape}, targets shape: {y.shape}")
    return X, y


def train_all_models():
    """Train all ML models and save them."""
    print("=" * 70)
    print("🚀 TRAINING ALL ML MODELS FOR CHATBOT")
    print("=" * 70)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # ==================== Train Weather Prediction Model ====================
    print("\n" + "🌤️ " * 20)
    print("1. WEATHER PREDICTION MODEL")
    print("🌤️ " * 20)
    
    X_weather, y_weather = generate_sample_weather_data(n_samples=500)
    X_train_w, X_test_w, y_train_w, y_test_w = train_test_split(
        X_weather, y_weather, test_size=0.2, random_state=42
    )
    
    weather_model = WeatherPredictionModel()
    weather_model.train(X_train_w, y_train_w)
    
    # Evaluate
    train_score_w = weather_model.model.score(
        weather_model.scaler.transform(X_train_w), y_train_w
    )
    test_score_w = weather_model.model.score(
        weather_model.scaler.transform(X_test_w), y_test_w
    )
    
    print(f"Training R² Score: {train_score_w:.4f}")
    print(f"Testing R² Score: {test_score_w:.4f}")
    print(f"Feature Importance: {weather_model.get_feature_importance()}")
    
    # ==================== Train Route Risk Classifier ====================
    print("\n" + "🛣️ " * 20)
    print("2. ROUTE RISK CLASSIFIER")
    print("🛣️ " * 20)
    
    X_route, y_route = generate_sample_route_data(n_samples=400)
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_route, y_route, test_size=0.2, random_state=42
    )
    
    route_model = RouteRiskClassifier()
    route_model.train(X_train_r, y_train_r)
    
    # Evaluate
    train_score_r = route_model.model.score(
        route_model.scaler.transform(X_train_r), y_train_r
    )
    test_score_r = route_model.model.score(
        route_model.scaler.transform(X_test_r), y_test_r
    )
    
    print(f"Training Accuracy: {train_score_r:.4f}")
    print(f"Testing Accuracy: {test_score_r:.4f}")
    
    # ==================== Train Travel Time Predictor ====================
    print("\n" + "⏱️ " * 20)
    print("3. TRAVEL TIME PREDICTOR")
    print("⏱️ " * 20)
    
    X_time, y_time = generate_sample_travel_time_data(n_samples=600)
    X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(
        X_time, y_time, test_size=0.2, random_state=42
    )
    
    time_model = TravelTimePredictor()
    time_model.train(X_train_t, y_train_t)
    
    # Evaluate
    train_score_t = time_model.model.score(
        time_model.scaler.transform(X_train_t), y_train_t
    )
    test_score_t = time_model.model.score(
        time_model.scaler.transform(X_test_t), y_test_t
    )
    
    print(f"Training R² Score: {train_score_t:.4f}")
    print(f"Testing R² Score: {test_score_t:.4f}")
    
    # ==================== Summary ====================
    print("\n" + "=" * 70)
    print("✅ ALL MODELS TRAINED AND SAVED!")
    print("=" * 70)
    print(f"Models saved in: models/")
    print(f"  - weather_predictor.pkl")
    print(f"  - route_risk_classifier.pkl")
    print(f"  - travel_time_predictor.pkl")
    print("\nNext: Use these models in tools.py as agent tools!")


def load_real_dataset(filepath: str, dataset_type: str = "weather"):
    """
    Load real dataset from CSV file.
    
    Dataset sources:
    - Kaggle: https://www.kaggle.com/datasets
    - OpenWeatherMap: https://openweathermap.org/
    - NHTSA: https://www.nhtsa.gov/data
    - UCI ML: https://archive.ics.uci.edu
    
    Args:
        filepath: Path to CSV file
        dataset_type: Type of dataset (weather, route, time)
        
    Returns:
        Tuple of (X, y)
    """
    print(f"📂 Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    
    if dataset_type == "weather":
        X = df[['temperature', 'precipitation', 'wind_speed', 'visibility']].values
        y = df['safety_score'].values
    
    elif dataset_type == "route":
        X = df[['congestion_level', 'weather_severity', 'accident_proximity', 'road_condition']].values
        y = df['risk_level'].values
    
    elif dataset_type == "time":
        X = df[['distance', 'congestion', 'weather_impact', 'time_of_day']].values
        y = df['travel_time'].values
    
    print(f"✅ Loaded {len(df)} records")
    return X, y


if __name__ == "__main__":
    # Train all models with sample data
    train_all_models()
    
    # To use real data instead:
    # X_weather, y_weather = load_real_dataset("datasets/weather_data.csv", "weather")
    # weather_model = WeatherPredictionModel()
    # weather_model.train(X_weather, y_weather)
