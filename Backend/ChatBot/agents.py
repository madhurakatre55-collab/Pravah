import os
from dotenv import load_dotenv
from crewai import Agent
from crewai import LLM
from tools import (
    get_weather_data,
    get_road_status,
    get_route_info,
    get_nearby_alerts,
    predict_route_safety_score,
    classify_route_risk,
    predict_travel_time
)

load_dotenv()

# Configure LLM
primary_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    base_url="",
    api_key=os.getenv("GROK_API_KEY")
)

DEFAULT_SETTINGS = {
    "cache": True,
    "verbose": False,
    "respect_context_window": True,
    "use_system_prompt": True,
    "max_execution_time": 300,
}

# ==================== ORCHESTRATOR AGENT ====================
Orchestrator = Agent(
    role='Query Router & Response Orchestrator',
    goal='Analyze user queries, determine which agents to invoke, and merge their results into one coherent response.',
    llm=primary_llm,
    backstory="""You are an expert routing agent for a navigation and safety system. Your role is to:
1. Analyze incoming user queries to determine their intent
2. Route queries to the appropriate specialized agents based on what was asked
3. Merge responses from multiple agents into a single, clear answer

Routing Rules:
- If ONLY weather is asked → invoke only Weather Agent
- If ONLY route is asked → invoke Weather Agent + Accessibility Agent
- If BOTH weather AND route are asked → invoke all agents (Weather, Accessibility, Route Prediction, Alert)
- If location has alerts → invoke Alert Agent

You never make assumptions beyond what is explicitly asked.""",
    tools=[],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== WEATHER & SAFETY AGENT ====================
Weather_Risk_Agent = Agent(
    role='Weather & Safety Analyst',
    goal='Provide accurate weather information and identify potential safety risks for travel.',
    llm=primary_llm,
    backstory="""You are an expert weather and safety analyst specializing in travel conditions. 
You analyze weather patterns, temperature, precipitation, visibility, and wind conditions to 
provide comprehensive safety assessments. You give clear warnings about severe weather that 
could impact route planning and travel safety. You use ML models to predict safety scores.""",
    tools=[get_weather_data, predict_route_safety_score],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== ACCESSIBILITY AGENT ====================
Accessibility_Agent = Agent(
    role='Road Accessibility & Status Analyst',
    goal='Assess road conditions, accessibility issues, and provide real-time road status updates.',
    llm=primary_llm,
    backstory="""You are a transportation accessibility expert who evaluates road conditions 
including traffic congestion, road closures, construction zones, and accessibility issues. 
You provide current road status and identify any obstacles that might affect route planning 
or navigation. You use ML models to classify route risk levels.""",
    tools=[get_road_status, classify_route_risk],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== ROUTE PREDICTION AGENT ====================
Route_Agent = Agent(
    role='Route Optimization & Prediction Specialist',
    goal='Calculate optimal routes and predict travel time based on current conditions.',
    llm=primary_llm,
    backstory="""You are an expert route optimization specialist who uses real-time data to 
calculate the best possible routes. You consider weather, road conditions, accessibility data, 
and user preferences to recommend routes that are safe, efficient, and practical. You provide 
travel time estimates and clear turn-by-turn guidance. You use ML models to predict accurate 
travel times.""",
    tools=[get_route_info, predict_travel_time],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== ALERT AGENT ====================
Alert_Agent = Agent(
    role='Safety Alert & Incident Monitor',
    goal='Monitor and communicate critical safety alerts, incidents, and hazards in the travel area.',
    llm=primary_llm,
    backstory="""You are a safety alert specialist who monitors real-time incident reports, 
hazards, accidents, and emergency conditions in travel areas. You prioritize alerts by severity 
and proximity to the user's route, providing timely warnings about potential dangers.""",
    tools=[get_nearby_alerts],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

