import os
from crewai import Task
from agents import (
    Orchestrator,
    Weather_Agent,
    Route_Accessibility_Agent,
    Alert_Agent,
    Translator_Agent
)

os.makedirs("task_output", exist_ok=True)

# Task factories

def get_weather_task(location: str) -> Task:
    """Weather analysis task."""
    return Task(
        description=f"""Analyze weather conditions for {location} and provide safety assessment.
Provide current weather conditions, ML safety score, and warnings.""",
        expected_output="""Weather analysis summary with ML safety score and recommendations.""",
        agent=Weather_Agent,
        async_execution=False
    )


def get_accessibility_task(route: str) -> Task:
    """Road accessibility task."""
    return Task(
        description=f"""Analyze road conditions and accessibility for {route}.
Provide road status, community reports, and detour recommendations.""",
        expected_output="""Road status analysis with accessibility reports and travel advice.""",
        agent=Route_Accessibility_Agent,
        async_execution=False
    )


def get_alert_task(location: str, radius: float = 5.0) -> Task:
    """Alert monitoring task."""
    return Task(
        description=f"""Monitor and evaluate safety alerts for {location} (search radius: {radius}km).
Provide identified hazards, risk severity, and emergency actions.""",
        expected_output="""Safety alert report with risk severity and recommended actions.""",
        agent=Alert_Agent,
        async_execution=False
    )


def get_translation_task(response_text: str, target_language: str) -> Task:
    """Regional translation task."""
    return Task(
        description=f"""Translate the final response into {target_language}.
Text: {response_text}""",
        expected_output=f"""Translation of the final response in {target_language}.""",
        agent=Translator_Agent,
        async_execution=False
    )


def get_response_merge_task(weather_result: str, road_result: str, alert_result: str) -> Task:
    """Response merge task."""
    return Task(
        description=f"""Merge agent findings into one unified response.
Findings:
- Weather: {weather_result}
- Road: {road_result}
- Alerts: {alert_result}""",
        expected_output="""Unified final answer for the user.""",
        agent=Orchestrator,
        async_execution=False
    )
