import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from ml_models import WeatherPredictionModel


def generate_sample_weather_data(n_samples: int = 1000) -> tuple:
    """
    Generate sample NER weather training data.
    
    In production, use IMD/Kaggle historical data:
    - IMD: https://mausam.imd.gov.in/
    - Kaggle: https://kaggle.com/datasets?search=india+weather
    
    Args:
        n_samples: Number of training samples to generate
        
    Returns:
        Tuple of (X, y) - features and safety score targets
    """
    print(f"📊 Generating {n_samples} sample NER weather records...\n")
    
    np.random.seed(42)
    
    # NER Weather Ranges (realistic for Northeast India)
    temperatures = np.random.uniform(5, 35, n_samples)          # 5-35°C (NER range)
    precipitation = np.random.exponential(8, n_samples)         # 0-100+ mm (monsoon region)
    wind_speeds = np.random.gamma(2, 2.5, n_samples)            # 0-40 km/h
    visibility = np.random.uniform(0.5, 15, n_samples)          # 0.5-15 km
    
    X = np.column_stack([temperatures, precipitation, wind_speeds, visibility])
    
    # Calculate safety score (0-100) based on conditions
    # Heavy rain + low visibility + high wind = Low safety
    safety_score = 100 - (
        (np.abs(temperatures - 22) / 35) * 10 +      # Comfort temp ~22°C
        (precipitation / 120) * 40 +                 # Heavy rain is major factor
        (wind_speeds / 40) * 20 +                    # High wind reduces safety
        ((15 - visibility) / 15) * 30                # Low visibility is critical
    )
    
    # Add realistic noise
    safety_score += np.random.normal(0, 5, n_samples)
    safety_score = np.clip(safety_score, 0, 100)
    
    y = safety_score
    
    print(f"✅ Generated {n_samples} weather samples")
    print(f"   Feature dimensions: {X.shape}")
    print(f"   Target range: {y.min():.1f} - {y.max():.1f}\n")
    
    return X, y


def load_real_weather_data(filepath: str) -> tuple:
    """
    Load real NER weather data from CSV.
    
    Expected CSV columns:
    - temperature_c
    - precipitation_mm
    - wind_speed_kmh
    - visibility_km
    - is_safe_for_transport (0 or 1, will be converted to 0-100 score)
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Tuple of (X, y) - features and targets
    """
    print(f"📂 Loading weather data from: {filepath}\n")
    
    df = pd.read_csv(filepath)
    
    # Extract features
    X = df[['temperature_c', 'precipitation_mm', 'wind_speed_kmh', 'visibility_km']].values
    
    # Extract target (safety score)
    if 'is_safe_for_transport' in df.columns:
        y = (df['is_safe_for_transport'].values * 100)  # 0->0, 1->100
    elif 'safety_score' in df.columns:
        y = df['safety_score'].values
    else:
        raise ValueError("CSV must have 'is_safe_for_transport' or 'safety_score' column")
    
    print(f"✅ Loaded {len(df)} records from CSV")
    print(f"   Feature shape: {X.shape}")
    print(f"   Target range: {y.min():.1f} - {y.max():.1f}\n")
    
    return X, y


def train_weather_model():
    """
    Main training function - trains ONLY weather safety prediction model.
    """
    print("=" * 70)
    print("🚀 TRAINING WEATHER SAFETY PREDICTION MODEL FOR NER")
    print("=" * 70)
    print()
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    print("📁 Models directory ready: ./models/\n")
    
    # ==================== Generate or Load Data ====================
    print("STEP 1: Preparing Training Data")
    print("-" * 70)
    
    # Option 1: Generate synthetic data (for testing)
    X, y = generate_sample_weather_data(n_samples=1000)
    
    # Option 2: Load real IMD data (uncomment when ready)
    # X, y = load_real_weather_data("datasets/weather_training_cleaned.csv")
    
    # ==================== Split Data ====================
    print("STEP 2: Splitting Training & Testing Data")
    print("-" * 70)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"✅ Training set: {X_train.shape[0]} samples")
    print(f"✅ Testing set: {X_test.shape[0]} samples\n")
    
    # ==================== Train Model ====================
    print("STEP 3: Training Weather Safety Model")
    print("-" * 70)
    print()
    
    weather_model = WeatherPredictionModel()
    weather_model.train(X_train, y_train)
    print()
    
    # ==================== Evaluate Model ====================
    print("STEP 4: Model Evaluation")
    print("-" * 70)
    
    train_score = weather_model.model.score(
        weather_model.scaler.transform(X_train), y_train
    )
    test_score = weather_model.model.score(
        weather_model.scaler.transform(X_test), y_test
    )
    
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Testing R² Score:  {test_score:.4f}\n")
    
    if test_score > 0.80:
        print("✅ Model performance: EXCELLENT")
    elif test_score > 0.70:
        print("✅ Model performance: GOOD")
    else:
        print("⚠️  Model performance: Fair (consider collecting more data)")
    
    print()
    
    # ==================== Feature Importance ====================
    print("STEP 5: Feature Importance Analysis")
    print("-" * 70)
    
    importance = weather_model.get_feature_importance()
    for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature:20s}: {score:.4f}")
    
    print()
    
    # ==================== Model Info ====================
    print("STEP 6: Model Information")
    print("-" * 70)
    
    info = weather_model.get_model_info()
    for key, value in info.items():
        print(f"  {key:20s}: {value}")
    
    print()
    print("=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print()
    print("📋 Summary:")
    print(f"   Model saved to: {weather_model.model_path}")
    print(f"   Scaler saved to: {weather_model.scaler_path}")
    print(f"   Test accuracy (R²): {test_score:.4f}")
    print()
    print("🚀 Next step: Run chatbot with 'python mains.py'")
    print()


def test_model_prediction():
    """
    Test the trained model with sample weather data.
    """
    print("\n" + "=" * 70)
    print("🧪 TESTING MODEL PREDICTIONS")
    print("=" * 70 + "\n")
    
    weather_model = WeatherPredictionModel()
    weather_model.load()
    
    # Test cases
    test_cases = [
        {"name": "Clear Day", "temp": 25, "rain": 0, "wind": 10, "vis": 15},
        {"name": "Light Rain", "temp": 22, "rain": 5, "wind": 12, "vis": 10},
        {"name": "Heavy Rain", "temp": 20, "rain": 50, "wind": 25, "vis": 3},
        {"name": "Severe Storm", "temp": 18, "rain": 100, "wind": 35, "vis": 1},
    ]
    
    print(f"{'Scenario':<20} {'Temp':<8} {'Rain':<8} {'Wind':<8} {'Vis':<8} {'Safety':<10} {'Risk':<10}")
    print("-" * 80)
    
    for test in test_cases:
        safety = weather_model.predict([test["temp"], test["rain"], test["wind"], test["vis"]])
        
        if safety >= 80:
            risk = "LOW"
        elif safety >= 60:
            risk = "MODERATE"
        elif safety >= 40:
            risk = "HIGH"
        else:
            risk = "CRITICAL"
        
        print(f"{test['name']:<20} {test['temp']:<8} {test['rain']:<8} {test['wind']:<8} {test['vis']:<8} {safety:<10.1f} {risk:<10}")
    
    print()


if __name__ == "__main__":
    # Train the weather model
    train_weather_model()
    
    # Test predictions
    test_model_prediction()
