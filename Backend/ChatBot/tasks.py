import os
from crewai import Task
from agents import (
    Orchestrator,
    Weather_Risk_Agent,
    Accessibility_Agent,
    Route_Agent,
    Alert_Agent
)

os.makedirs("task_output", exist_ok=True)

# ==================== ORCHESTRATION TASK ====================
Orchestration_Task = Task(
    description="""Analyze the user's query and determine which agents to invoke.
    
    Steps:
    1. Identify what the user is asking for (weather, route, alerts, combinations)
    2. Based on routing rules:
       - If ONLY weather asked → set flag to invoke only Weather Agent
       - If ONLY route asked → set flag to invoke Weather + Accessibility Agents
       - If BOTH weather AND route asked → set flag to invoke all agents
       - If alerts are mentioned → add Alert Agent to the routing
    3. Output clear routing decisions with rationale
    4. Wait for other agents' results to merge them
    
    User Query: {query}""",
    expected_output="""Clear routing decision with:
    - User intent identified
    - List of agents to invoke
    - Reasoning for the routing decision
    - Format ready for agent delegation""",
    agent=Orchestrator,
    async_execution=False
)

# ==================== WEATHER ANALYSIS TASK ====================
Weather_Analysis_Task = Task(
    description="""Analyze weather conditions for the given location and provide safety assessment.
    
    Location: {location}
    
    Provide:
    1. Current weather conditions (temperature, precipitation, visibility, wind)
    2. Safety assessment for travel (is it safe to travel?)
    3. Any weather-related warnings or alerts
    4. Recommendations based on current weather conditions
    
    Be concise but comprehensive in your analysis.""",
    expected_output="""Weather analysis including:
    - Current conditions summary
    - Safety assessment
    - Any warnings or alerts
    - Travel recommendations based on weather""",
    agent=Weather_Risk_Agent,
    async_execution=False
)

# ==================== ROAD ACCESSIBILITY TASK ====================
Accessibility_Task = Task(
    description="""Analyze road conditions and accessibility for the given route.
    
    Location/Route: {route}
    
    Provide:
    1. Current road status (open, closed, under construction)
    2. Traffic conditions and congestion levels
    3. Accessibility issues or obstacles
    4. Estimated delays or detours
    
    Be specific about any road conditions affecting travel.""",
    expected_output="""Road status analysis including:
    - Road accessibility status
    - Traffic and congestion information
    - Any closures or construction zones
    - Estimated delays
    - Accessibility recommendations""",
    agent=Accessibility_Agent,
    async_execution=False
)

# ==================== ROUTE OPTIMIZATION TASK ====================
Route_Optimization_Task = Task(
    description="""Calculate and recommend the best route based on all current conditions.
    
    From: {start_location}
    To: {end_location}
    Weather Info: {weather_info}
    Road Status: {road_status}
    
    Provide:
    1. Optimal route recommendation (considering weather and road conditions)
    2. Distance and estimated travel time
    3. Turn-by-turn guidance overview
    4. Alternative routes if applicable
    5. Safety score and conditions to watch for
    
    Integrate weather and road accessibility data into your route recommendation.""",
    expected_output="""Route recommendation including:
    - Recommended route with distance and time
    - Alternative routes if applicable
    - Safety considerations
    - Turn-by-turn guidance overview
    - Conditions to watch for during travel""",
    agent=Route_Agent,
    async_execution=False
)

# ==================== ALERT MONITORING TASK ====================
Alert_Monitoring_Task = Task(
    description="""Monitor and report safety alerts for the given location/route.
    
    Location/Route: {location}
    Search Radius: {radius}
    
    Provide:
    1. Critical alerts (accidents, hazards, emergencies)
    2. Alert severity and proximity
    3. Impact on travel plans
    4. Recommended actions or detours
    5. Real-time incident updates
    
    Prioritize alerts by severity and proximity to the user's route.""",
    expected_output="""Safety alert report including:
    - Critical alerts identified
    - Severity assessment
    - Impact on travel
    - Recommended actions
    - Alternative routes if needed due to alerts""",
    agent=Alert_Agent,
    async_execution=False
)

# ==================== RESPONSE MERGING TASK ====================
Response_Merge_Task = Task(
    description="""Merge all agent responses into one coherent, clear answer.
    
    Agent Responses to Merge:
    - Weather Analysis: {weather_result}
    - Road Status: {road_result}
    - Route Recommendation: {route_result}
    - Safety Alerts: {alert_result}
    
    Create a unified response that:
    1. Integrates all relevant information in logical order
    2. Prioritizes critical information (safety alerts, weather warnings)
    3. Provides clear, actionable recommendations
    4. Maintains consistency across all agent inputs
    5. Communicates in a single, unified voice
    
    Format the response for direct user presentation.""",
    expected_output="""Unified response that:
    - Addresses all aspects of the user's query
    - Prioritizes safety information
    - Provides clear, actionable advice
    - Is coherent and easy to understand
    - Ready for direct user presentation""",
    agent=Orchestrator,
    async_execution=False
)

