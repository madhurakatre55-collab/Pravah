import os
import json
from dotenv import load_dotenv
try:
    from crewai.tools import tool
    from crewai.tools.base_tool import Tool
    Tool.__call__ = lambda self, *args, **kwargs: self.run(*args, **kwargs)
except ImportError:
    try:
        from crewai_tools import tool
    except ImportError:
        pass
from ml_models import WeatherPredictionModel
from datetime import datetime

load_dotenv()

# Weather ML model
weather_ml_model = WeatherPredictionModel()


# Tool 1
@tool("Get Weather Data")
def get_weather_data(location: str) -> dict:
    """Fetch weather data."""
    return {
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


# Tool 2
@tool("Predict Weather Safety Score")
def predict_route_safety_score(temperature: float, precipitation: float, 
                               wind_speed: float, visibility: float) -> dict:
    """Predict route safety score."""
    weather_features = [temperature, precipitation, wind_speed, visibility]
    
    try:
        # Model prediction
        safety_score = weather_ml_model.predict(weather_features)
        safety_score = max(0, min(100, safety_score))
        
        # Risk classification
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
            "model": "RandomForestRegressor",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Model prediction failed"
        }


# Tool 3
@tool("Get Road Status")
def get_road_status(location: str, route_name: str = None) -> dict:
    """Fetch road status."""
    return {
        "location": location,
        "route": route_name,
        "status": "open",
        "accessibility": True,
        "traffic_level": "light",
        "congestion_percent": 15,
        "disruptions": [],
        "construction_zones": [],
        "estimated_delay_minutes": 0,
        "last_updated": datetime.now().isoformat(),
        "data_source": "mock_data"
    }


# Tool 4
@tool("Get Community Feedback")
def get_community_feedback(location: str, time_period_hours: int = 24) -> dict:
    """Fetch community feedback."""
    return {
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


# Tool 5
@tool("Translate Response")
def translate_response(text: str, target_language: str = "hindi") -> dict:
    """Translate response text."""
    supported_languages = {
        "english": "English",
        "hindi": "हिंदी",
        "assamese": "অসমীয়া",
        "bengali": "বাংলা",
        "manipuri": "মৈতৈলোন্ (Manipuri)",
        "mizo": "Mizo",
        "nagamese": "Nagamese",
        "khasi": "Khasi"
    }
    
    target = target_language.lower().strip()
    if target not in supported_languages:
        target = "english"
        
    if target == "english":
        return {
            "original_text": text,
            "target_language": "English",
            "language_code": "english",
            "translated_text": text,
            "timestamp": datetime.now().isoformat()
        }

    # Load translations
    trans_file = os.path.join(os.path.dirname(__file__), "translations.json")
    translations = {}
    if os.path.exists(trans_file):
        try:
            with open(trans_file, "r", encoding="utf-8") as f:
                translations = json.load(f)
        except Exception:
            pass

    translated_text = text
    lang_dict = translations.get(target, {})
    for eng_phrase, target_phrase in lang_dict.items():
        translated_text = translated_text.replace(eng_phrase, target_phrase)

    return {
        "original_text": text,
        "target_language": supported_languages.get(target, target),
        "language_code": target,
        "translated_text": translated_text,
        "timestamp": datetime.now().isoformat()
    }


# Detect query intent
def detect_query_intent(query: str) -> dict:
    """Detect query intent."""
    query_lower = query.lower()
    
    # Keyword detection
    weather_keywords = [
        'weather', 'temperature', 'rain', 'rainfall', 'monsoon', 'storm', 'cyclone',
        'climate', 'wind', 'fog', 'visibility', 'sunny', 'cloudy'
    ]
    route_keywords = [
        'route', 'road', 'highway', 'direction', 'path', 'way', 'drive', 'driving',
        'travel', 'sohra', 'nh-6', 'nh6', 'nh-27', 'nh27', 'blocked', 'blockage',
        'landslide', 'mudslide', 'navigate', 'navigation', 'truck', 'trucks',
        'dispatch', 'cargo', 'freight', 'convoy', 'convoys', 'transport', 'transportation',
        'transit', 'logistics', 'corridor', 'reach', 'trip', 'journey', 'destination'
    ]
    alert_keywords = [
        'alert', 'accident', 'incident', 'danger', 'hazard', 'warning', 'emergency',
        'risk', 'disruption', 'closure', 'flood', 'flooding', 'sinkhole', 'evacuation'
    ]
    
    wants_weather = any(keyword in query_lower for keyword in weather_keywords)
    wants_route = any(keyword in query_lower for keyword in route_keywords)
    wants_alerts = any(keyword in query_lower for keyword in alert_keywords)
    
    # Check corridor pattern
    if ' to ' in query_lower or ' from ' in query_lower:
        wants_route = True

    # Check dispatch words
    safety_transport_words = ['safe', 'safety', 'dispatch', 'send', 'travel', 'drive', 'supply', 'supplies']
    if any(w in query_lower for w in safety_transport_words):
        wants_weather = True
        wants_route = True
        
    # Default fallback intent
    if not (wants_weather or wants_route or wants_alerts):
        wants_weather = True
        wants_route = True
    
    return {
        "original_query": query,
        "wants_weather": wants_weather,
        "wants_route": wants_route,
        "wants_alerts": wants_alerts,
        "agents_needed": {
            "weather_agent": wants_weather,
            "accessibility_agent": wants_route,
            "alert_agent": wants_alerts or (wants_weather and wants_route)
        }
    }
