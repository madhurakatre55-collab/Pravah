import os
import sys
from typing import Dict
from crewai import Crew
from dotenv import load_dotenv

from agents import (
    Orchestrator,
    Weather_Agent,
    Route_Accessibility_Agent,
    Alert_Agent,
    Translator_Agent
)
from tasks import (
    get_weather_task,
    get_accessibility_task,
    get_alert_task,
    get_translation_task,
    get_response_merge_task
)
from tools import (
    detect_query_intent,
    get_weather_data,
    predict_route_safety_score,
    get_road_status,
    get_community_feedback,
    translate_response
)

# UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()


class ChatbotOrchestrator:
    """Chatbot query orchestrator."""
    
    def __init__(self):
        """Initialize orchestrator."""
        self.orchestrator_agent = Orchestrator
        self.weather_agent = Weather_Agent
        self.accessibility_agent = Route_Accessibility_Agent
        self.alert_agent = Alert_Agent
        self.translator_agent = Translator_Agent
        self.execution_results = {}
    
    def analyze_query_intent(self, query: str) -> Dict:
        """Analyze query intent."""
        print("\n[STEP 1] Analyzing Query Intent...")
        print(f"User Query: {query}")
        
        intent = detect_query_intent(query)
        print("Intent Detected:")
        print(f"  - Wants Weather: {intent['wants_weather']}")
        print(f"  - Wants Route: {intent['wants_route']}")
        print(f"  - Wants Alerts: {intent['wants_alerts']}")
        return intent
    
    def determine_agent_routing(self, intent: Dict) -> Dict:
        """Determine agent routing."""
        print("\n[STEP 2] Determining Agent Routing...")
        
        agents_to_invoke = []
        routing_reason = []
        
        if intent['wants_weather'] and not intent['wants_route']:
            agents_to_invoke = ['weather']
            routing_reason.append("Only weather information requested -> Weather Agent only")
        elif intent['wants_route'] and not intent['wants_weather']:
            agents_to_invoke = ['weather', 'accessibility']
            routing_reason.append("Route requested without weather -> Weather + Accessibility Agents")
        elif intent['wants_weather'] and intent['wants_route']:
            agents_to_invoke = ['weather', 'accessibility', 'alert']
            routing_reason.append("Both weather and route requested -> Weather, Accessibility, and Alert Agents")
        else:
            agents_to_invoke = ['weather', 'accessibility']
            routing_reason.append("General travel inquiry -> Weather and Accessibility Agents")
        
        if intent['wants_alerts'] and 'alert' not in agents_to_invoke:
            agents_to_invoke.append('alert')
            routing_reason.append("Alerts mentioned -> Alert Agent included")
        
        routing_decision = {
            'agents_to_invoke': agents_to_invoke,
            'routing_reason': routing_reason,
            'invoke_weather': 'weather' in agents_to_invoke,
            'invoke_accessibility': 'accessibility' in agents_to_invoke,
            'invoke_alert': 'alert' in agents_to_invoke
        }
        
        print(f"Routing Decision: {agents_to_invoke}")
        for reason in routing_reason:
            print(f"  - {reason}")
        return routing_decision
    
    def execute_weather_analysis(self, location: str) -> str:
        """Execute weather analysis."""
        print(f"\n[WEATHER] Executing Weather Analysis for {location}...")
        
        try:
            task = get_weather_task(location)
            crew = Crew(agents=[self.weather_agent], tasks=[task])
            result = str(crew.kickoff())
        except Exception as e:
            print(f"[WEATHER] LLM unavailable ({e}). Using deterministic ML model & weather data...")
            w_data = get_weather_data(location)
            score_data = predict_route_safety_score(
                temperature=float(w_data.get('temperature_celsius', 22)),
                precipitation=float(w_data.get('rainfall_mm', 5)),
                wind_speed=float(w_data.get('wind_speed_kmh', 15)),
                visibility=float(w_data.get('visibility_km', 10))
            )
            safety = score_data.get('safety_score', score_data.get('predicted_safety_score', 85.0))
            r_level = score_data.get('risk_level', 'LOW')
            recom = score_data.get('recommended_action', score_data.get('recommendation', 'Conditions are safe for logistics movement.'))
            result = (
                f"Weather Analysis for {location}:\n"
                f"- Conditions: {w_data.get('conditions', 'Partly Cloudy')}, Temperature: {w_data.get('temperature_celsius', 22)}°C\n"
                f"- Rainfall: {w_data.get('rainfall_mm', 5)} mm, Wind Speed: {w_data.get('wind_speed_kmh', 15)} km/h, Visibility: {w_data.get('visibility_km', 10)} km\n"
                f"- ML Safety Score: {safety}/100 (Risk Level: {r_level})\n"
                f"- Assessment: {recom}"
            )
        
        self.execution_results['weather'] = result
        print("[WEATHER] Analysis Complete")
        return result
    
    def execute_accessibility_analysis(self, route: str) -> str:
        """Execute road analysis."""
        print(f"\n[ROUTE] Executing Accessibility Analysis for {route}...")
        
        try:
            task = get_accessibility_task(route)
            crew = Crew(agents=[self.accessibility_agent], tasks=[task])
            result = str(crew.kickoff())
        except Exception as e:
            print(f"[ROUTE] LLM unavailable ({e}). Using live road sensors and ground feedback...")
            road_data = get_road_status(route)
            fb_data = get_community_feedback(route)
            disruptions = ", ".join(road_data.get('disruptions', [])) or "None reported"
            reports_list = [f"{r.get('type', 'Report')}: {r.get('description', '')} ({r.get('severity', 'LOW')})" for r in fb_data.get('recent_reports', [])]
            reports = "; ".join(reports_list) if reports_list else "No active community obstruction reports."
            result = (
                f"Road Accessibility Analysis for {route}:\n"
                f"- Status: {road_data.get('status', 'Open')}\n"
                f"- Surface Condition: {road_data.get('surface_condition', 'Good')}\n"
                f"- Disruptions / Closures: {disruptions}\n"
                f"- Community Reports: {reports}\n"
                f"- Travel Recommendation: Route is open and navigable. Standard mountain driving precautions apply."
            )
            
        self.execution_results['accessibility'] = result
        print("[ROUTE] Accessibility Analysis Complete")
        return result
    
    def execute_translation(self, text: str, target_language: str = "hindi") -> str:
        """Execute translation task."""
        print(f"\n[TRANSLATION] Executing Translation to {target_language}...")
        
        if not target_language or target_language.lower() in ["english", "en"]:
            return text
            
        try:
            task = get_translation_task(text, target_language)
            crew = Crew(agents=[self.translator_agent], tasks=[task])
            result = str(crew.kickoff())
        except Exception as e:
            print(f"[TRANSLATION] LLM unavailable ({e}). Using regional dictionary translator...")
            t_data = translate_response(text, target_language)
            result = t_data.get('translated_text', text)
            
        self.execution_results['translation'] = result
        print("[TRANSLATION] Complete")
        return result
    
    def execute_alert_monitoring(self, location: str, radius: float = 5.0) -> str:
        """Execute alert monitoring."""
        print(f"\n[ALERT] Executing Alert Monitoring for {location} (radius: {radius}km)...")
        
        try:
            task = get_alert_task(location, radius)
            crew = Crew(agents=[self.alert_agent], tasks=[task])
            result = str(crew.kickoff())
        except Exception as e:
            print(f"[ALERT] LLM unavailable ({e}). Using automated safety alert engine...")
            w_res = self.execution_results.get('weather', '')
            if 'CRITICAL' in w_res:
                severity = "CRITICAL"
                actions = "Stop all logistics operations immediately due to hazardous conditions."
            elif 'HIGH' in w_res or 'landslide' in location.lower():
                severity = "HIGH"
                actions = "Halt non-essential supply transport. Check alternate bypass route."
            elif 'MODERATE' in w_res:
                severity = "MODERATE"
                actions = "Caution advised - Monitor local weather updates and reduce speeds."
            else:
                severity = "LOW"
                actions = "Normal transit operations permitted. Maintain standard convoy monitoring."
                
            result = (
                f"Safety Alert Report for {location}:\n"
                f"- Severity Level: {severity}\n"
                f"- Active Warnings: Monsoon vigilance on hill slopes within {radius}km radius.\n"
                f"- Action Advised: {actions}"
            )
            
        self.execution_results['alert'] = result
        print("[ALERT] Alert Monitoring Complete")
        return result
    
    def merge_responses(self, routing_decision: Dict) -> str:
        """Merge agent responses."""
        print("\n[STEP 5] Merging Agent Responses...")
        
        weather_res = self.execution_results.get('weather', 'Not requested')
        road_res = self.execution_results.get('accessibility', 'Not requested')
        alert_res = self.execution_results.get('alert', 'Not requested')
        
        try:
            task = get_response_merge_task(weather_res, road_res, alert_res)
            crew = Crew(agents=[self.orchestrator_agent], tasks=[task])
            final_response = str(crew.kickoff())
        except Exception as e:
            print(f"[STEP 5] LLM unavailable ({e}). Generating structured multi-agent synthesis...")
            sections = ["### 🤖 NER Disaster & Logistics Intelligence Report"]
            if weather_res != 'Not requested':
                sections.append(f"**🌤️ Weather Assessment:**\n{weather_res}")
            if road_res != 'Not requested':
                sections.append(f"**🛣️ Road Accessibility & Route Disruption:**\n{road_res}")
            if alert_res != 'Not requested':
                sections.append(f"**⚠️ Active Disaster Alerts & Warnings:**\n{alert_res}")
            sections.append("**✅ Operational Recommendation:**\nProceed in accordance with the safety score and ground disruption alerts detailed above.")
            final_response = "\n\n".join(sections)
            
        print("[STEP 5] Response Merge Complete")
        return final_response
    
    def process_query(self, query: str, location: str = None, 
                     start_location: str = None, end_location: str = None,
                     target_language: str = "english") -> Dict:
        """Process user query."""
        print("=" * 70)
        print("CHATBOT QUERY PROCESSING WORKFLOW")
        print("=" * 70)
        
        # Reset results
        self.execution_results = {}
        
        # Infer location
        if not location:
            query_lower = query.lower()
            if "shillong" in query_lower:
                location = "Shillong"
            elif "guwahati" in query_lower:
                location = "Guwahati"
            elif "sohra" in query_lower or "cherrapunji" in query_lower:
                location = "Sohra"
            elif "kohima" in query_lower:
                location = "Kohima"
            elif "aizawl" in query_lower:
                location = "Aizawl"
            elif "gangtok" in query_lower:
                location = "Gangtok"
            elif "itanagar" in query_lower:
                location = "Itanagar"
            elif "agartala" in query_lower:
                location = "Agartala"
            else:
                location = "Northeast Region"
                
        # Step 1: Intent
        intent = self.analyze_query_intent(query)
        
        # Step 2: Routing
        routing_decision = self.determine_agent_routing(intent)
        
        # Step 3: Execute
        print("\n[STEP 3] Executing Designated Agents...")
        
        if routing_decision['invoke_weather']:
            self.execute_weather_analysis(location)
        
        if routing_decision['invoke_accessibility']:
            route = f"{start_location} to {end_location}" if (start_location and end_location) else None
            if not route:
                query_lower = query.lower()
                if "guwahati" in query_lower and "shillong" in query_lower:
                    route = "Guwahati to Shillong"
                elif "shillong" in query_lower and "sohra" in query_lower:
                    route = "Shillong to Sohra"
                elif "silchar" in query_lower and "aizawl" in query_lower:
                    route = "Silchar to Aizawl"
                elif "dimapur" in query_lower and "kohima" in query_lower:
                    route = "Dimapur to Kohima"
                else:
                    route = f"{location} Corridor"
            self.execute_accessibility_analysis(route)
        
        if routing_decision['invoke_alert']:
            self.execute_alert_monitoring(location)
        
        # Step 4: Results
        print("\n[STEP 4] Intermediate Results:")
        for agent_name, result in self.execution_results.items():
            print(f"\n--- {agent_name.upper()} ---")
            print(f"{result}")
        
        # Step 5: Merge
        final_response = self.merge_responses(routing_decision)
        
        # Step 6: Translate
        translated_response = final_response
        if target_language and target_language.lower() not in ["english", "en"]:
            translated_response = self.execute_translation(final_response, target_language)
        
        # Return workflow result
        workflow_result = {
            'query': query,
            'intent': intent,
            'routing_decision': routing_decision,
            'agent_results': self.execution_results,
            'final_response': final_response,
            'translated_response': translated_response,
            'target_language': target_language
        }
        
        print("\n" + "=" * 70)
        print("WORKFLOW COMPLETE")
        print("=" * 70)
        print(f"\nFINAL ANSWER:\n{translated_response}\n")
        
        return workflow_result


def main():
    """Terminal runner."""
    orchestrator = ChatbotOrchestrator()
    query = "Is it safe to send supplies to Shillong today? Please check weather and road landslides."
    orchestrator.process_query(query=query, location="Shillong")


if __name__ == "__main__":
    main()
