import os
from crewai_tools import tool
from dotenv import load_dotenv
from ml_models import WeatherPredictionModel
from datetime import datetime

load_dotenv()

# ==================== INITIALIZE ML MODEL ====================
# ONE ML Model: Weather Safety Prediction for NER
weather_ml_model = WeatherPredictionModel()


# ==================== TOOL 1: Get Weather Data ====================
@tool("Get Weather Data")
def get_weather_data(location: str) -> dict:
    """
    Fetches current weather data for a specific NER location.
    Provides real-time weather conditions for prediction.
    
    Args:
        location (str): NER city/district name (Guwahati, Shillong, etc.)
        
    Returns:
        dict: Weather data including temperature, rainfall, wind, visibility, humidity
    """
    # TODO: Replace with real OpenWeatherMap or IMD API
    # Current: Mock data for testing
    
    mock_weather = {
        "location": location,
        "timestamp": datetime.now().isoformat(),
        "temperature_celsius": 22,
        "rainfall_mm": 5,
        "wind_speed_kmh": 15,
        "visibility_km": 10,
        "humidity_percent": 70,
        "conditions": "Partly Cloudy",
        "data_source": "mock_data"
    }
    
    return mock_weather


# ==================== TOOL 2: Predict Weather Safety (ML Model) ====================
@tool("Predict Weather Safety Score")
def predict_route_safety_score(temperature: float, precipitation: float, 
                               wind_speed: float, visibility: float) -> dict:
    """
    Uses trained ML model to predict weather safety score for logistics.
    Safety Score: 0-100 (100 = Safe, 0 = Critical danger)
    
    Args:
        temperature (float): Current temperature in Celsius
        precipitation (float): Rainfall in millimeters
        wind_speed (float): Wind speed in km/h
        visibility (float): Visibility in kilometers
        
    Returns:
        dict: Safety score, risk level, and recommendations
    """
    weather_features = [temperature, precipitation, wind_speed, visibility]
    
    try:
        # ML Model Prediction
        safety_score = weather_ml_model.predict(weather_features)
        safety_score = max(0, min(100, safety_score))
        
        # Risk Classification
        if safety_score >= 80:
            risk_level = "LOW"
            alert = "✅ Excellent conditions - Safe to transport"
            action = "Proceed with standard precautions"
        elif safety_score >= 60:
            risk_level = "MODERATE"
            alert = "⚠️ Acceptable conditions - Use caution"
            action = "Proceed with careful monitoring"
        elif safety_score >= 40:
            risk_level = "HIGH"
            alert = "🔴 Poor conditions - Consider delay"
            action = "Recommend delay or alternate route"
        else:
            risk_level = "CRITICAL"
            alert = "🚨 Severe conditions - DO NOT TRANSPORT"
            action = "Stop all logistics operations"
        
        return {
            "safety_score": float(round(safety_score, 2)),
            "risk_level": risk_level,
            "alert_message": alert,
            "recommended_action": action,
            "weather_input": {
                "temperature_celsius": temperature,
                "precipitation_mm": precipitation,
                "wind_speed_kmh": wind_speed,
                "visibility_km": visibility
            },
            "model": "RandomForestRegressor (Trained on IMD data)",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not predict safety. Train model using: python train_models.py"
        }


# ==================== TOOL 3: Get Road Status ====================
@tool("Get Road Status")
def get_road_status(location: str, route_name: str = None) -> dict:
    """
    Fetches current road accessibility and status for NER locations.
    Provides info on open/blocked routes, disruptions, accessibility.
    
    Args:
        location (str): Location/city name
        route_name (str, optional): Specific route to check
        
    Returns:
        dict: Road status, accessibility, disruptions, estimated delays
    """
    # TODO: Replace with real API (Google Maps, NHAI Portal, State PWD APIs)
    # Current: Mock data for testing
    
    road_data = {
        "location": location,
        "route": route_name,
        "status": "open",
        "accessibility": True,
        "traffic_level": "light",  # light, moderate, heavy
        "congestion_percent": 15,
        "disruptions": [],
        "construction_zones": [],
        "estimated_delay_minutes": 0,
        "last_updated": datetime.now().isoformat(),
        "data_source": "mock_data"
    }
    
    return road_data


# ==================== TOOL 4: Get Community Feedback ====================
@tool("Get Community Feedback")
def get_community_feedback(location: str, time_period_hours: int = 24) -> dict:
    """
    Gets anonymized community reports about road conditions and disruptions.
    READ-ONLY from community database (anonymized, no identity stored).
    
    Args:
        location (str): Location to get feedback for
        time_period_hours (int): Last N hours of reports (default: 24)
        
    Returns:
        dict: Aggregated community feedback about conditions
    """
    # TODO: Connect to your community database (separate feature)
    # Current: Mock data for testing
    
    community_data = {
        "location": location,
        "time_period_hours": time_period_hours,
        "total_reports": 5,
        "reports_summary": [
            {
                "category": "road_status",
                "issue": "Road blocked due to landslide",
                "count": 3,
                "severity": "high",
                "last_reported": "2 hours ago"
            },
            {
                "category": "weather",
                "issue": "Heavy rainfall continuing",
                "count": 2,
                "severity": "medium",
                "last_reported": "30 minutes ago"
            }
        ],
        "overall_trust_level": "HIGH",
        "verified_count": 4,
        "data_source": "Anonymous community reports"
    }
    
    return community_data


# ==================== TOOL 5: Translate Response ====================
@tool("Translate Response")
def translate_response(text: str, target_language: str = "hindi") -> dict:
    """
    Translates chatbot responses to regional NER languages.
    Supports 8 languages for inclusive accessibility.
    
    Args:
        text (str): English text to translate
        target_language (str): Target language code
                              (hindi, assamese, bengali, manipuri, mizo, nagamese, khasi, english)
        
    Returns:
        dict: Translated text in target language
    """
    # TODO: Replace with Google Translate API or LangChain Translator
    # Current: Placeholder for testing
    
    supported_languages = {
        "english": "English",
        "hindi": "हिंदी",
        "assamese": "অসমীয়া",
        "bengali": "বাংলা",
        "manipuri": "Manipuri",
        "mizo": "Mizo",
        "nagamese": "Nagamese",
        "khasi": "Khasi"
    }
    
    if target_language not in supported_languages:
        return {
            "error": f"Language {target_language} not supported",
            "supported_languages": list(supported_languages.keys())
        }
    
    # Mock translation (replace with real API)
    translation = {
        "original_text": text,
        "target_language": supported_languages[target_language],
        "language_code": target_language,
        "translated_text": f"[{supported_languages[target_language]}] {text}",  # Placeholder
        "translation_service": "Google Translate API (To be integrated)",
        "timestamp": datetime.now().isoformat()
    }
    
    return translation
