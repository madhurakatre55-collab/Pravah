# ML Model Setup & Integration Guide

## Overview

The chatbot now includes **3 trained ML models** that enhance agent predictions:

1. **Weather Prediction Model** - Predicts route safety score based on weather
2. **Route Risk Classifier** - Classifies route risk level (LOW/MEDIUM/HIGH)
3. **Travel Time Predictor** - Predicts accurate travel times with conditions

---

## Installation

### Step 1: Install Dependencies

```bash
pip install -r Backend/ChatBot/requirnments.txt
```

**New ML libraries added:**
- `scikit-learn>=1.3.0` - Machine learning models
- `pandas>=2.0.0` - Data handling
- `numpy>=1.24.0` - Numerical computing
- `joblib>=1.3.0` - Model serialization

### Step 2: Verify Installation

```bash
python -c "import sklearn; print('✅ scikit-learn installed')"
python -c "import pandas; print('✅ pandas installed')"
python -c "import joblib; print('✅ joblib installed')"
```

---

## Training Models

### Quick Start (Generate Sample Data & Train)

```bash
cd Backend/ChatBot
python train_models.py
```

This will:
- Generate 500+ synthetic weather records
- Generate 400+ synthetic route records
- Generate 600+ synthetic travel time records
- Train all 3 ML models
- Save models to `models/` directory

**Expected Output:**
```
🚀 TRAINING ALL ML MODELS FOR CHATBOT
================================================================
🌤️ 1. WEATHER PREDICTION MODEL
📊 Generating 500 sample weather records...
✅ Model trained and saved
Training R² Score: 0.92
Testing R² Score: 0.89

🛣️ 2. ROUTE RISK CLASSIFIER
📊 Generating 400 sample route records...
✅ Model trained and saved
Training Accuracy: 0.95
Testing Accuracy: 0.92

⏱️ 3. TRAVEL TIME PREDICTOR
📊 Generating 600 sample travel time records...
✅ Model trained and saved
Training R² Score: 0.88
Testing R² Score: 0.85

✅ ALL MODELS TRAINED AND SAVED!
```

### Using Real Data

Download datasets from:

#### **Weather Data:**
- [OpenWeatherMap Historical API](https://openweathermap.org/api/weatherbit-historical-api)
- [Kaggle Weather Datasets](https://kaggle.com/datasets?search=weather)
- [NOAA Weather Data](https://www.noaa.gov/)

#### **Road/Route Data:**
- [Google Maps API](https://developers.google.com/maps)
- [TomTom Traffic Data](https://developer.tomtom.com/)
- [HERE Maps API](https://developer.here.com/)
- [Kaggle Traffic Datasets](https://kaggle.com/datasets?search=traffic)

#### **Accident/Safety Data:**
- [NHTSA Accident Data](https://www.nhtsa.gov/data)
- [Kaggle Accident Datasets](https://kaggle.com/datasets?search=accident)

**CSV Format Expected:**

**weather_data.csv:**
```csv
temperature,precipitation,wind_speed,visibility,safety_score
22,0,5,10,85
15,2.5,12,8,65
-5,5,25,2,25
```

**route_data.csv:**
```csv
congestion_level,weather_severity,accident_proximity,road_condition,risk_level
20,2,10,90,0
65,5,2,40,2
45,3,5,60,1
```

**travel_time.csv:**
```csv
distance,congestion,weather_impact,time_of_day,travel_time
25,20,1,9,35
25,60,2,8,45
25,80,4,18,65
```

**Train with Real Data:**

```python
from train_models import load_real_dataset
from ml_models import WeatherPredictionModel
from sklearn.model_selection import train_test_split

# Load real dataset
X, y = load_real_dataset("datasets/weather_data.csv", dataset_type="weather")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
weather_model = WeatherPredictionModel()
weather_model.train(X_train, y_train)

print(f"Model R² Score: {weather_model.model.score(weather_model.scaler.transform(X_test), y_test)}")
```

---

## Model Files & Structure

```
Backend/ChatBot/
├── ml_models.py                 # ML model classes
├── train_models.py              # Training script
├── models/                       # Trained model files
│   ├── weather_predictor.pkl    # Weather safety model
│   ├── weather_scaler.pkl       # Weather data scaler
│   ├── route_risk_classifier.pkl # Route risk model
│   ├── route_scaler.pkl          # Route data scaler
│   ├── travel_time_predictor.pkl # Travel time model
│   └── time_scaler.pkl           # Time data scaler
└── datasets/                     # (Optional) Real training data
    ├── weather_data.csv
    ├── route_data.csv
    └── travel_time.csv
```

---

## Using ML Models in Agents

The ML models are automatically integrated as **agent tools**:

### 1. Weather Safety Prediction

**Tool:** `predict_route_safety_score`

```python
# Called by Weather_Risk_Agent
result = predict_route_safety_score(
    temperature=22,
    precipitation=0,
    wind_speed=5,
    visibility=10
)

# Output:
{
    "safety_score": 85.5,
    "risk_level": "LOW",
    "warning": "Excellent weather conditions for travel",
    "weather_conditions": {...}
}
```

### 2. Route Risk Classification

**Tool:** `classify_route_risk`

```python
# Called by Accessibility_Agent
result = classify_route_risk(
    congestion_level=45,
    weather_severity=3,
    accident_proximity=5,
    road_condition=60
)

# Output:
{
    "risk_level": "MEDIUM",
    "confidence_score": 92.5,
    "recommendation": "Use caution. Monitor traffic and weather updates.",
    "action": "Monitor"
}
```

### 3. Travel Time Prediction

**Tool:** `predict_travel_time`

```python
# Called by Route_Agent
result = predict_travel_time(
    distance=25,
    congestion=45,
    weather_impact=2,
    time_of_day=9
)

# Output:
{
    "predicted_travel_time": {
        "minutes": 42.5,
        "formatted": "42m"
    },
    "estimated_arrival": "2026-09-02T10:45:00",
    "contributing_factors": ["High congestion (+8 min)"]
}
```

---

## Running the Complete Workflow

### Step 1: Install & Train

```bash
# Install dependencies
pip install -r Backend/ChatBot/requirnments.txt

# Train models
python Backend/ChatBot/train_models.py
```

### Step 2: Run the Chatbot

```bash
cd Backend/ChatBot
python mains.py
```

### Step 3: Test with Example Queries

```python
from mains import ChatbotOrchestrator

orchestrator = ChatbotOrchestrator()

# Weather + Route Query
result = orchestrator.process_query(
    query="Is it safe to drive to the beach today? Need weather and route info.",
    start_location="Home",
    end_location="Beach",
    location="Coastal Highway"
)

print(result['final_response'])
```

---

## Model Performance Metrics

### Weather Prediction Model
- **Type:** RandomForestRegressor
- **Features:** 4 (temperature, precipitation, wind_speed, visibility)
- **Target:** Safety score (0-100)
- **Expected R² Score:** 0.85-0.95

### Route Risk Classifier
- **Type:** GradientBoostingClassifier
- **Features:** 4 (congestion, weather, accidents, road condition)
- **Target:** Risk level (0=LOW, 1=MEDIUM, 2=HIGH)
- **Expected Accuracy:** 90-95%

### Travel Time Predictor
- **Type:** RandomForestRegressor
- **Features:** 4 (distance, congestion, weather, time_of_day)
- **Target:** Travel time (minutes)
- **Expected R² Score:** 0.80-0.90

---

## Troubleshooting

### Error: "Model not found"
**Solution:** Run `python train_models.py` first

### Error: "Import error for scikit-learn"
**Solution:** `pip install scikit-learn pandas numpy joblib`

### Poor Model Performance
**Solutions:**
1. Use more real data (1000+ records)
2. Tune hyperparameters in `ml_models.py`
3. Try different model algorithms
4. Ensure data preprocessing is correct

### Models Slow to Load
**Solution:** Models are lazy-loaded. First prediction may be slower.

---

## Advanced: Custom Model Training

```python
from ml_models import WeatherPredictionModel
from train_models import load_real_dataset
from sklearn.model_selection import train_test_split

# Load your custom dataset
X, y = load_real_dataset("my_weather_data.csv", "weather")

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = WeatherPredictionModel()
model.train(X_train, y_train)

# Evaluate
score = model.model.score(model.scaler.transform(X_test), y_test)
print(f"Model Score: {score:.4f}")

# Use
prediction = model.predict([22, 0, 5, 10])
print(f"Safety Score: {prediction}")
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Train models with sample data
3. ✅ Test the workflow
4. 📊 Replace with real datasets
5. 🚀 Deploy to production

---

## Integration with Real APIs

When ready for production, replace mock tools with real APIs:

### Weather Data
```python
import requests

def get_real_weather(location):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_KEY"
    )
    return response.json()
```

### Route Data
```python
from googlemaps import Client as GoogleMapsClient

gmaps = GoogleMapsClient(key='YOUR_KEY')
directions = gmaps.directions("New York", "Boston")
```

See [tools.py](tools.py) for placeholder comments where APIs should be integrated.

---

## Support

For issues or questions:
1. Check model files exist in `models/` directory
2. Verify data format matches CSV examples
3. Ensure all dependencies are installed
4. Review error messages in agent logs

Happy modeling! 🚀
