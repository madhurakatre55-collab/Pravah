import os
import json
from typing import Dict, List, Optional
from crewai import Crew
from dotenv import load_dotenv

from agents import (
    Orchestrator,
    Weather_Risk_Agent,
    Accessibility_Agent,
    Route_Agent,
    Alert_Agent
)
from tasks import (
    Orchestration_Task,
    Weather_Analysis_Task,
    Accessibility_Task,
    Route_Optimization_Task,
    Alert_Monitoring_Task,
    Response_Merge_Task
)
from tools import detect_query_intent

load_dotenv()


class ChatbotOrchestrator:
    """
    Main orchestrator for the chatbot query routing system.
    Manages agent execution flow based on user queries following the workflow:
    
    1. User asks a question
    2. Orchestrator analyzes intent and routes to appropriate agents
    3. Agents execute based on routing rules
    4. Results are merged into one clear answer
    """
    
    def __init__(self):
        """Initialize the orchestrator with all agents and routing rules."""
        self.orchestrator_agent = Orchestrator
        self.weather_agent = Weather_Risk_Agent
        self.accessibility_agent = Accessibility_Agent
        self.route_agent = Route_Agent
        self.alert_agent = Alert_Agent
        self.execution_results = {}
    
    def analyze_query_intent(self, query: str) -> Dict:
        """
        Step 1: Analyze the user query to determine intent.
        
        Args:
            query (str): The user's question
            
        Returns:
            dict: Intent analysis with routing flags
        """
        print(f"\n📋 Step 1: Analyzing Query Intent...")
        print(f"User Query: {query}")
        
        intent = detect_query_intent(query)
        print(f"Intent Detected:")
        print(f"  - Wants Weather: {intent['wants_weather']}")
        print(f"  - Wants Route: {intent['wants_route']}")
        print(f"  - Wants Alerts: {intent['wants_alerts']}")
        
        return intent
    
    def determine_agent_routing(self, intent: Dict) -> Dict:
        """
        Step 2: Determine which agents to invoke based on routing rules.
        
        Routing Rules:
        - If ONLY weather asked → invoke only Weather Agent
        - If ONLY route asked → invoke Weather + Accessibility Agents
        - If BOTH weather AND route asked → invoke all agents
        - If alerts mentioned → include Alert Agent
        
        Args:
            intent (dict): Intent analysis from Step 1
            
        Returns:
            dict: Routing decisions for agent execution
        """
        print(f"\n🔀 Step 2: Determining Agent Routing...")
        
        agents_to_invoke = []
        routing_reason = []
        
        if intent['wants_weather'] and not intent['wants_route']:
            # Rule 1: Only weather asked → only Weather Agent
            agents_to_invoke = ['weather']
            routing_reason.append("Only weather information requested → Weather Agent only")
        
        elif intent['wants_route'] and not intent['wants_weather']:
            # Rule 2: Only route asked → Weather + Accessibility
            agents_to_invoke = ['weather', 'accessibility']
            routing_reason.append("Route requested without weather → Weather + Accessibility Agents")
        
        elif intent['wants_weather'] and intent['wants_route']:
            # Rule 3: Both weather and route → All agents
            agents_to_invoke = ['weather', 'accessibility', 'route', 'alert']
            routing_reason.append("Both weather and route requested → All Agents (Weather, Accessibility, Route, Alert)")
        
        else:
            # Default: basic response only
            agents_to_invoke = []
            routing_reason.append("No specific query type detected → Orchestrator response only")
        
        # Add alert agent if alerts are mentioned
        if intent['wants_alerts'] and 'alert' not in agents_to_invoke:
            agents_to_invoke.append('alert')
            routing_reason.append("Alerts mentioned → Alert Agent included")
        
        routing_decision = {
            'agents_to_invoke': agents_to_invoke,
            'routing_reason': routing_reason,
            'invoke_weather': 'weather' in agents_to_invoke,
            'invoke_accessibility': 'accessibility' in agents_to_invoke,
            'invoke_route': 'route' in agents_to_invoke,
            'invoke_alert': 'alert' in agents_to_invoke
        }
        
        print(f"Routing Decision: {agents_to_invoke}")
        for reason in routing_reason:
            print(f"  - {reason}")
        
        return routing_decision
    
    def execute_weather_analysis(self, location: str) -> str:
        """
        Execute weather analysis task.
        
        Args:
            location (str): The location to analyze weather for
            
        Returns:
            str: Weather analysis result
        """
        print(f"\n🌤️  Executing Weather Analysis for {location}...")
        
        task = Weather_Analysis_Task.copy()
        task.description = task.description.format(location=location)
        
        crew = Crew(agents=[self.weather_agent], tasks=[task])
        result = crew.kickoff()
        
        self.execution_results['weather'] = result
        print(f"Weather Analysis Complete")
        return result
    
    def execute_accessibility_analysis(self, route: str) -> str:
        """
        Execute road accessibility analysis task.
        
        Args:
            route (str): The route to analyze
            
        Returns:
            str: Accessibility analysis result
        """
        print(f"\n🛣️  Executing Accessibility Analysis for {route}...")
        
        task = Accessibility_Task.copy()
        task.description = task.description.format(route=route)
        
        crew = Crew(agents=[self.accessibility_agent], tasks=[task])
        result = crew.kickoff()
        
        self.execution_results['accessibility'] = result
        print(f"Accessibility Analysis Complete")
        return result
    
    def execute_route_optimization(self, start: str, end: str, 
                                  weather_info: str = "", road_status: str = "") -> str:
        """
        Execute route optimization task.
        
        Args:
            start (str): Starting location
            end (str): Destination
            weather_info (str): Weather information to consider
            road_status (str): Road status information to consider
            
        Returns:
            str: Route optimization result
        """
        print(f"\n📍 Executing Route Optimization from {start} to {end}...")
        
        task = Route_Optimization_Task.copy()
        task.description = task.description.format(
            start_location=start,
            end_location=end,
            weather_info=weather_info or "Current weather data",
            road_status=road_status or "Current road conditions"
        )
        
        crew = Crew(agents=[self.route_agent], tasks=[task])
        result = crew.kickoff()
        
        self.execution_results['route'] = result
        print(f"Route Optimization Complete")
        return result
    
    def execute_alert_monitoring(self, location: str, radius: float = 5.0) -> str:
        """
        Execute alert monitoring task.
        
        Args:
            location (str): The location to monitor
            radius (float): Search radius in kilometers
            
        Returns:
            str: Alert monitoring result
        """
        print(f"\n🚨 Executing Alert Monitoring for {location} (radius: {radius}km)...")
        
        task = Alert_Monitoring_Task.copy()
        task.description = task.description.format(location=location, radius=radius)
        
        crew = Crew(agents=[self.alert_agent], tasks=[task])
        result = crew.kickoff()
        
        self.execution_results['alert'] = result
        print(f"Alert Monitoring Complete")
        return result
    
    def merge_responses(self, routing_decision: Dict) -> str:
        """
        Step 5: Merge all agent responses into one coherent answer.
        
        Args:
            routing_decision (dict): The routing decision made
            
        Returns:
            str: Merged final response
        """
        print(f"\n🔄 Step 5: Merging Agent Responses...")
        
        task = Response_Merge_Task.copy()
        task.description = task.description.format(
            weather_result=self.execution_results.get('weather', 'Not requested'),
            road_result=self.execution_results.get('accessibility', 'Not requested'),
            route_result=self.execution_results.get('route', 'Not requested'),
            alert_result=self.execution_results.get('alert', 'Not requested')
        )
        
        crew = Crew(agents=[self.orchestrator_agent], tasks=[task])
        final_response = crew.kickoff()
        
        print(f"Response Merge Complete")
        return final_response
    
    def process_query(self, query: str, location: str = None, 
                     start_location: str = None, end_location: str = None) -> Dict:
        """
        Main workflow: Process a user query through the complete agent workflow.
        
        Args:
            query (str): The user's question
            location (str, optional): Location for weather/alerts
            start_location (str, optional): Starting point for routes
            end_location (str, optional): Destination for routes
            
        Returns:
            dict: Complete workflow result including all agent outputs
        """
        print("=" * 70)
        print("🤖 CHATBOT QUERY PROCESSING WORKFLOW")
        print("=" * 70)
        
        # Step 1: Analyze Intent
        intent = self.analyze_query_intent(query)
        
        # Step 2: Determine Routing
        routing_decision = self.determine_agent_routing(intent)
        
        # Step 3: Execute Agents Based on Routing
        print(f"\n⚙️  Step 3: Executing Designated Agents...")
        
        if routing_decision['invoke_weather'] and location:
            self.execute_weather_analysis(location)
        
        if routing_decision['invoke_accessibility'] and (start_location or location):
            route = f"{start_location} to {end_location}" if start_location and end_location else location
            self.execute_accessibility_analysis(route)
        
        if routing_decision['invoke_route'] and start_location and end_location:
            weather_info = self.execution_results.get('weather', '')
            road_status = self.execution_results.get('accessibility', '')
            self.execute_route_optimization(start_location, end_location, weather_info, road_status)
        
        if routing_decision['invoke_alert'] and location:
            self.execute_alert_monitoring(location)
        
        # Step 4: Display Intermediate Results
        print(f"\n📊 Step 4: Intermediate Results...")
        for agent_name, result in self.execution_results.items():
            print(f"\n{agent_name.upper()} Result:")
            print(f"{result}\n")
        
        # Step 5: Merge Responses
        final_response = self.merge_responses(routing_decision)
        
        # Return complete workflow result
        workflow_result = {
            'query': query,
            'intent': intent,
            'routing_decision': routing_decision,
            'agent_results': self.execution_results,
            'final_response': final_response
        }
        
        print(f"\n" + "=" * 70)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 70)
        print(f"\n📝 FINAL ANSWER:\n{final_response}")
        
        return workflow_result


def main():
    """
    Example usage of the ChatbotOrchestrator.
    """
    orchestrator = ChatbotOrchestrator()
    
    # Example 1: Weather only query
    print("\n\n" + "🔷" * 35)
    print("EXAMPLE 1: Weather Only Query")
    print("🔷" * 35)
    result1 = orchestrator.process_query(
        query="What's the weather like tomorrow?",
        location="New York"
    )
    
    # Reset execution results
    orchestrator.execution_results = {}
    
    # Example 2: Route only query
    print("\n\n" + "🔶" * 35)
    print("EXAMPLE 2: Route Only Query")
    print("🔶" * 35)
    result2 = orchestrator.process_query(
        query="How do I get from Downtown to the Airport?",
        start_location="Downtown",
        end_location="Airport",
        location="City Center"
    )
    
    # Reset execution results
    orchestrator.execution_results = {}
    
    # Example 3: Weather + Route + Alert query
    print("\n\n" + "🔴" * 35)
    print("EXAMPLE 3: Weather + Route + Alert Query")
    print("🔴" * 35)
    result3 = orchestrator.process_query(
        query="Is it safe to drive to the coast today? Weather and route info needed.",
        start_location="Home",
        end_location="Beach",
        location="Coastal Highway"
    )


if __name__ == "__main__":
    main()
