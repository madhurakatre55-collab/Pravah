import os
from crewai_tools import tool
from dotenv import load_dotenv
from ml_models import WeatherPredictionModel

load_dotenv()

# ==================== INITIALIZE ML MODEL ====================
# ONE ML Model: Weather Safety Prediction
weather_ml_model = WeatherPredictionModel()


# ==================== ML-BASED PREDICTION TOOLS ====================
@tool("Predict Route Safety Score")
def predict_route_safety_score(temperature: float, precipitation: float, 
                               wind_speed: float, visibility: float) -> dict:
    """
    Uses trained ML model to predict route safety score based on weather conditions.
    Score: 0-100 (higher = safer)
    
    Args:
        temperature (float): Current temperature in Celsius
        precipitation (float): Precipitation amount in mm
        wind_speed (float): Wind speed in km/h
        visibility (float): Visibility in km
        
    Returns:
        dict: Safety score and detailed risk assessment
    """
    # Prepare features
    weather_features = [temperature, precipitation, wind_speed, visibility]
    
    try:
        # Get ML prediction
        safety_score = weather_ml_model.predict(weather_features)
        
        # Normalize to 0-100
        safety_score = max(0, min(100, safety_score))
        
        # Determine risk level
        if safety_score >= 80:
            risk_level = "LOW"
            warning = "Excellent weather conditions for travel"
        elif safety_score >= 60:
            risk_level = "MODERATE"
            warning = "Acceptable weather, use caution"
        elif safety_score >= 40:
            risk_level = "HIGH"
            warning = "Poor weather conditions, consider alternate plans"
        else:
            risk_level = "CRITICAL"
            warning = "Severe weather, travel not recommended"
        
        return {
            "safety_score": float(round(safety_score, 2)),
            "risk_level": risk_level,
            "warning": warning,
            "weather_conditions": {
                "temperature_celsius": temperature,
                "precipitation_mm": precipitation,
                "wind_speed_kmh": wind_speed,
                "visibility_km": visibility
            },
            "model_type": "RandomForestRegressor",
            "prediction_confidence": "High"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not predict safety score. Make sure to train models first using train_models.py"
        }


@tool("Classify Route Risk Level")
def classify_route_risk(congestion_level: float, weather_severity: float, 
                       accident_proximity: float, road_condition: float) -> dict:
    """
    Uses trained ML model to classify route risk level (LOW/MEDIUM/HIGH).
    
    Args:
        congestion_level (float): Traffic congestion 0-100%
        weather_severity (float): Weather severity 0-10 (0=clear, 10=severe)
        accident_proximity (float): Distance to nearest accident in km
        road_condition (float): Road condition score 0-100 (100=excellent)
        
    Returns:
        dict: Risk classification with probability score
    """
    route_features = [congestion_level, weather_severity, accident_proximity, road_condition]
    
    try:
        # Get ML prediction
        risk_level, probability = route_risk_model.predict(route_features)
        
        # Generate recommendation
        if risk_level == "LOW":
            recommendation = "Route is safe. Proceed with normal precautions."
        elif risk_level == "MEDIUM":
            recommendation = "Use caution. Monitor traffic and weather updates."
        else:  # HIGH
            recommendation = "High risk route. Consider alternative paths or delay travel."
        
        return {
            "risk_level": risk_level,
            "confidence_score": float(round(probability * 100, 2)),
            "recommendation": recommendation,
            "factors": {
                "congestion_level": congestion_level,
                "weather_severity": weather_severity,
                "accident_proximity_km": accident_proximity,
                "road_condition": road_condition
            },
            "model_type": "GradientBoostingClassifier",
            "action": "Avoid" if risk_level == "HIGH" else "Monitor" if risk_level == "MEDIUM" else "Proceed"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not classify route risk. Make sure to train models first using train_models.py"
        }


@tool("Predict Travel Time")
def predict_travel_time(distance: float, congestion: float, 
                       weather_impact: float, time_of_day: float) -> dict:
    """
    Uses trained ML model to predict travel time based on route and conditions.
    
    Args:
        distance (float): Route distance in km
        congestion (float): Traffic congestion level 0-100%
        weather_impact (float): Weather impact factor 0-5 (0=no impact, 5=severe)
        time_of_day (float): Time of day in 24-hour format (0-24)
        
    Returns:
        dict: Predicted travel time with breakdown
    """
    route_features = [distance, congestion, weather_impact, time_of_day]
    
    try:
        # Get ML prediction
        travel_time_minutes = travel_time_model.predict(route_features)
        
        # Convert to hours and minutes
        hours = int(travel_time_minutes // 60)
        minutes = int(travel_time_minutes % 60)
        
        # Estimate arrival time
        from datetime import datetime, timedelta
        departure_time = datetime.now()
        arrival_time = departure_time + timedelta(minutes=travel_time_minutes)
        
        # Analyze factors
        base_time = distance / 50  # Assume ~50km/h base speed
        time_overhead = travel_time_minutes - base_time
        
        factors_info = []
        if congestion > 50:
            factors_info.append(f"High congestion (+{int((congestion/100)*travel_time_minutes)} min)")
        if weather_impact > 2:
            factors_info.append(f"Severe weather (+{int((weather_impact/5)*travel_time_minutes)} min)")
        
        # Rush hour detection
        if (time_of_day >= 8 and time_of_day <= 10) or (time_of_day >= 17 and time_of_day <= 19):
            factors_info.append("Rush hour traffic detected")
        
        return {
            "predicted_travel_time": {
                "minutes": float(round(travel_time_minutes, 2)),
                "formatted": f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            },
            "departure_time": departure_time.isoformat(),
            "estimated_arrival": arrival_time.isoformat(),
            "route_details": {
                "distance_km": distance,
                "congestion_percent": congestion,
                "weather_impact_factor": weather_impact,
                "time_of_day_24h": time_of_day
            },
            "contributing_factors": factors_info if factors_info else ["Optimal conditions"],
            "base_travel_time_minutes": float(round(base_time, 2)),
            "model_type": "RandomForestRegressor",
            "prediction_confidence": "High"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Could not predict travel time. Make sure to train models first using train_models.py"
        }



# ==================== WEATHER TOOLS ====================
@tool("Get Weather Data")
def get_weather_data(location: str) -> dict:
    """
    Fetches current weather data for a specific location.
    Returns temperature, conditions, precipitation, visibility, and wind info.
    
    Args:
        location (str): The location to get weather data for
        
    Returns:
        dict: Weather information including temp, conditions, precipitation, etc.
    """
    # TODO: Integrate with real weather API (OpenWeatherMap, WeatherAPI, etc.)
    # For now, returning mock data structure
    weather_data = {
        "location": location,
        "temperature": 22,
        "conditions": "Partly Cloudy",
        "precipitation": 0,
        "visibility": 10,
        "wind_speed": 5,
        "wind_direction": "NE",
        "humidity": 65,
        "weather_alerts": [],
        "is_safe_for_travel": True
    }
    
    # Use ML model to get safety score
    safety_prediction = predict_route_safety_score(
        temperature=weather_data["temperature"],
        precipitation=weather_data["precipitation"],
        wind_speed=weather_data["wind_speed"],
        visibility=weather_data["visibility"]
    )
    
    weather_data["ml_safety_score"] = safety_prediction.get("safety_score", 0)
    weather_data["ml_risk_level"] = safety_prediction.get("risk_level", "UNKNOWN")
    
    return weather_data



# ==================== ROAD STATUS TOOLS ====================
@tool("Get Road Status")
def get_road_status(location: str, route: str = None) -> dict:
    """
    Fetches current road status and accessibility information.
    Returns traffic conditions, road closures, construction, and accessibility data.
    
    Args:
        location (str): The location to check road status for
        route (str, optional): Specific route to check
        
    Returns:
        dict: Road status including traffic, closures, construction, accessibility
    """
    # TODO: Integrate with real traffic/road status API (Google Maps, HERE, TomTom, etc.)
    # For now, returning mock data structure
    return {
        "location": location,
        "route": route,
        "traffic_level": "light",
        "congestion_percentage": 15,
        "road_closures": [],
        "construction_zones": [],
        "accessibility_issues": [],
        "estimated_delay": 0,
        "is_accessible": True,
        "last_updated": "2026-09-02T10:30:00Z"
    }


# ==================== ROUTE TOOLS ====================
@tool("Get Route Information")
def get_route_info(start_location: str, end_location: str, preferences: str = None) -> dict:
    """
    Calculates optimal routes between two locations.
    Considers weather, road conditions, and user preferences.
    
    Args:
        start_location (str): Starting point
        end_location (str): Destination
        preferences (str, optional): Route preferences (fastest, safest, most scenic, etc.)
        
    Returns:
        dict: Route information including paths, distances, travel times, and recommendations
    """
    # TODO: Integrate with routing API (Google Maps Directions, OSRM, GraphHopper, etc.)
    # For now, returning mock data structure
    return {
        "start": start_location,
        "end": end_location,
        "routes": [
            {
                "name": "Recommended Route",
                "distance": 25.5,
                "distance_unit": "km",
                "duration": "35 minutes",
                "traffic_affected": False,
                "polyline": "encoded_polyline_data",
                "safety_score": 9.2,
                "weather_impact": "low",
                "steps": []
            }
        ],
        "best_route_index": 0,
        "estimated_total_travel_time": "35 minutes",
        "departure_time": "2026-09-02T10:45:00Z",
        "arrival_time": "2026-09-02T11:20:00Z"
    }


# ==================== ALERT TOOLS ====================
@tool("Get Nearby Alerts")
def get_nearby_alerts(location: str, radius_km: float = 5.0) -> dict:
    """
    Retrieves safety alerts and incidents near a specific location.
    Returns accidents, hazards, incidents, and emergency situations.
    
    Args:
        location (str): The location to check for alerts
        radius_km (float): Search radius in kilometers (default: 5 km)
        
    Returns:
        dict: List of alerts including accidents, hazards, incidents, and their severity
    """
    # TODO: Integrate with real-time alert APIs (Waze, HERE, emergencies.gov, etc.)
    # For now, returning mock data structure
    return {
        "location": location,
        "search_radius_km": radius_km,
        "alerts": [
            {
                "type": "accident",
                "severity": "high",
                "description": "Multi-vehicle accident on Main Street",
                "distance_km": 2.3,
                "direction": "ahead",
                "latitude": 0.0,
                "longitude": 0.0,
                "reported_at": "2026-09-02T10:20:00Z",
                "impact": "High traffic congestion expected"
            }
        ],
        "alert_count": 1,
        "has_critical_alerts": True,
        "recommendation": "Consider alternate route"
    }


# ==================== UTILITY TOOLS ====================
@tool("Detect Query Intent")
def detect_query_intent(query: str) -> dict:
    """
    Analyzes user query to determine intent and required agent routing.
    
    Args:
        query (str): The user's question or request
        
    Returns:
        dict: Intent analysis with flags for weather, route, alerts, etc.
    """
    query_lower = query.lower()
    
    # Keyword detection for different intents
    weather_keywords = ['weather', 'temperature', 'rain', 'snow', 'storm', 'condition', 'climate', 'safe', 'safety']
    route_keywords = ['route', 'direction', 'path', 'way', 'drive', 'travel', 'how to get', 'navigate', 'go to', 'from']
    alert_keywords = ['alert', 'accident', 'incident', 'danger', 'hazard', 'warning', 'emergency', 'nearby']
    
    wants_weather = any(keyword in query_lower for keyword in weather_keywords)
    wants_route = any(keyword in query_lower for keyword in route_keywords)
    wants_alerts = any(keyword in query_lower for keyword in alert_keywords)
    
    return {
        "original_query": query,
        "wants_weather": wants_weather,
        "wants_route": wants_route,
        "wants_alerts": wants_alerts,
        "agents_needed": {
            "weather_agent": wants_weather,
            "accessibility_agent": wants_route or wants_weather,  # Accessibility needed for route queries
            "route_agent": wants_route,
            "alert_agent": wants_alerts or wants_route  # Alerts important for route safety
        }
    }
