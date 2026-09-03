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

# Patch cache breakpoint
try:
    import crewai.llms.cache
    crewai.llms.cache.mark_cache_breakpoint = lambda message: {k: v for k, v in message.items() if k != "cache_breakpoint"}
except Exception:
    pass

# Configure LLM
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")

primary_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    base_url="",
    api_key=api_key
)

DEFAULT_SETTINGS = {
    "cache": False,
    "verbose": False,
    "respect_context_window": True,
    "use_system_prompt": True,
    "max_execution_time": 300,
}

# Orchestrator Agent
Orchestrator = Agent(
    role='Query Router & Response Orchestrator',
    goal='Analyze user queries, route to appropriate agents, and merge results into one coherent response.',
    llm=primary_llm,
    backstory="""You are an expert routing agent for NER Logistics & Accessibility Intelligence Platform.
Your responsibilities:
1. Analyze user queries to understand intent (weather, route, or both)
2. Route queries to specialized agents based on needs
3. Merge all agent responses into one clear, actionable answer
4. Identify if alerts need to be triggered based on severity""",
    tools=[],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# Weather Agent
Weather_Agent = Agent(
    role='Weather Intelligence Analyst',
    goal='Provide accurate weather data and ML-based safety predictions for NER region.',
    llm=primary_llm,
    backstory="""You are an expert weather analyst for the North Eastern Region.
Your responsibilities:
1. Fetch live weather data (temperature, rainfall, wind, visibility, humidity)
2. Use ML model to predict weather safety score (0-100)
3. Identify weather-based risks (heavy rain, low visibility, strong winds)
4. Provide clear recommendations based on safety score""",
    tools=[get_weather_data, predict_route_safety_score],
    max_rpm=15,
    max_iter=3, 
    **DEFAULT_SETTINGS
)

# Accessibility Agent
Route_Accessibility_Agent = Agent(
    role='Road Accessibility & Status Analyst',
    goal='Assess road conditions and provide real-time accessibility information for NER.',
    llm=primary_llm,
    backstory="""You are a road accessibility expert for the North Eastern Region.
Your responsibilities:
1. Check road status (open, blocked, under construction)
2. Get community feedback about road conditions
3. Assess accessibility for logistics and emergency routes
4. Identify disruption factors (landslides, floods, accidents)""",
    tools=[get_road_status, get_community_feedback],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# Translator Agent
Translator_Agent = Agent(
    role='Multilingual Response Translator',
    goal='Translate responses to regional NER languages for accessibility.',
    llm=primary_llm,
    backstory="""You are a multilingual translator for the North Eastern Region.
Your responsibilities:
1. Translate chatbot responses to regional languages (Hindi, Assamese, Bengali, Manipuri, Mizo)
2. Maintain alert severity in all translations
3. Preserve critical safety information""",
    tools=[translate_response],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)

# Alert Agent
Alert_Agent = Agent(
    role='Safety & Alert Notification Specialist',
    goal='Analyze weather safety score, road disruptions, evaluate severity, and trigger alert notifications.',
    llm=primary_llm,
    backstory="""You are the emergency safety & alert monitoring agent for the North Eastern Region.
Your responsibilities:
1. Analyze weather safety scores and road accessibility reports
2. Check severe disruptions (landslides, flash floods, highway blockages)
3. Evaluate overall risk severity (LOW, MODERATE, HIGH, CRITICAL)""",
    tools=[],
    max_rpm=15,
    max_iter=3,
    **DEFAULT_SETTINGS
)
