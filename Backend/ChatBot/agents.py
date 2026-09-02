import os
from dotenv import load_dotenv
from crewai import Agent
from crewai import LLM
from tools import (
    get_weather_data,
    get_road_status,
    predict_route_safety_score,
    get_community_feedback,
    translate_response
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
    goal='Analyze user queries, route to appropriate agents, and merge results into one coherent response.',
    llm=primary_llm,
    backstory="""You are an expert routing agent for NER Logistics & Accessibility Intelligence Platform.

Your responsibilities:
1. Analyze user queries to understand intent (weather, route, or both)
2. Route queries to specialized agents based on needs
3. Merge all agent responses into one clear, actionable answer
4. Identify if alerts need to be triggered based on severity

Routing Rules:
- Weather only → Weather Agent
- Route only → Route Accessibility Agent + Weather Agent (for context)
- Both → Weather Agent + Route Accessibility Agent
- High risk detected → Generate alert in response
- Multilingual → Route to Translator Agent

You provide intelligent routing without assumptions.""",
    tools=[],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== WEATHER INTELLIGENCE AGENT ====================
Weather_Agent = Agent(
    role='Weather Intelligence Analyst',
    goal='Provide accurate weather data and ML-based safety predictions for NER region.',
    llm=primary_llm,
    backstory="""You are an expert weather analyst for the North Eastern Region.

Your responsibilities:
1. Fetch live weather data (temperature, rainfall, wind, visibility, humidity)
2. Use ML model to predict weather safety score (0-100)
3. Identify weather-based risks (heavy rain, low visibility, strong winds)
4. Provide clear recommendations based on safety score
5. Generate warnings if safety score < 60

You analyze weather patterns and their impact on logistics and road accessibility.
You are precise, data-driven, and focus only on weather conditions.""",
    tools=[get_weather_data, predict_route_safety_score],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== ROUTE ACCESSIBILITY AGENT ====================
Route_Accessibility_Agent = Agent(
    role='Road Accessibility & Status Analyst',
    goal='Assess road conditions and provide real-time accessibility information for NER.',
    llm=primary_llm,
    backstory="""You are a road accessibility expert for the North Eastern Region.

Your responsibilities:
1. Check road status (open, blocked, under construction)
2. Get community feedback about road conditions (anonymized reports)
3. Assess accessibility for logistics and emergency routes
4. Identify disruption factors (landslides, floods, accidents)
5. Suggest alternate routes if main route is inaccessible

You read from community database (don't store data), analyze conditions, and provide
accessibility assessments. You focus on route viability, not GPS tracking.""",
    tools=[get_road_status, get_community_feedback],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# ==================== TRANSLATOR AGENT ====================
Translator_Agent = Agent(
    role='Multilingual Response Translator',
    goal='Translate responses to regional NER languages for accessibility.',
    llm=primary_llm,
    backstory="""You are a multilingual translator for the North Eastern Region.

Your responsibilities:
1. Translate chatbot responses to 8 regional languages:
   - English, Hindi, Assamese, Bengali, Manipuri, Mizo, Nagamese, Khasi
2. Maintain alert severity in all translations
3. Preserve critical safety information
4. Handle regional context and cultural nuances
5. Ensure clarity in translations (not word-for-word)

You provide multilingual support to reach all NER communities.
Priority: Safety and clarity over perfect grammar.""",
    tools=[translate_response],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

