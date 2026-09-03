import sys
import os
import json
import unittest

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Windows encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from ml_models import WeatherPredictionModel, RouteRiskClassifier
from tools import (
    get_weather_data,
    predict_route_safety_score,
    get_road_status,
    get_community_feedback,
    translate_response,
    detect_query_intent
)
from mains import ChatbotOrchestrator
import app as flask_app_module


class TestPravahChatbotSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 75)
        print("  STARTING PRAVAH CHATBOT & ML INTELLIGENCE 20-TEST VALIDATION SUITE")
        print("=" * 75 + "\n")
        cls.orchestrator = ChatbotOrchestrator()
        cls.weather_model = WeatherPredictionModel()
        cls.risk_classifier = RouteRiskClassifier()
        flask_app_module.app.testing = True
        cls.client = flask_app_module.app.test_client()

    # Category A

    def test_01_weather_prediction_safe_conditions(self):
        """Test safe weather."""
        score = self.weather_model.predict([24.0, 0.0, 10.0, 15.0])
        print(f"[TEST 1] Safe Weather Score: {score:.2f}/100")
        self.assertGreaterEqual(score, 75.0)

    def test_02_weather_prediction_extreme_monsoon(self):
        """Test extreme monsoon."""
        score = self.weather_model.predict([18.0, 250.0, 45.0, 2.0])
        print(f"[TEST 2] Heavy Monsoon Score: {score:.2f}/100")
        self.assertLess(score, 55.0)

    def test_03_weather_prediction_high_wind_storm(self):
        """Test storm wind."""
        score_normal = self.weather_model.predict([20.0, 10.0, 15.0, 10.0])
        score_storm = self.weather_model.predict([20.0, 10.0, 75.0, 10.0])
        print(f"[TEST 3] Normal wind: {score_normal:.2f} vs High gale: {score_storm:.2f}")
        self.assertGreater(score_normal, score_storm)

    def test_04_weather_prediction_dense_mountain_fog(self):
        """Test mountain fog."""
        score_clear = self.weather_model.predict([15.0, 5.0, 10.0, 12.0])
        score_fog = self.weather_model.predict([15.0, 5.0, 10.0, 0.5])
        print(f"[TEST 4] Clear: {score_clear:.2f} vs Dense Fog: {score_fog:.2f}")
        self.assertGreater(score_clear, score_fog)

    def test_05_weather_prediction_bounds_clamping(self):
        """Test bounds clamping."""
        score_extreme_bad = self.weather_model.predict([-10.0, 600.0, 140.0, 0.0])
        score_extreme_good = self.weather_model.predict([25.0, 0.0, 2.0, 30.0])
        print(f"[TEST 5] Extreme Bad: {score_extreme_bad:.2f}, Extreme Good: {score_extreme_good:.2f}")
        self.assertGreaterEqual(score_extreme_bad, 0.0)
        self.assertLessEqual(score_extreme_bad, 100.0)
        self.assertGreaterEqual(score_extreme_good, 0.0)
        self.assertLessEqual(score_extreme_good, 100.0)

    # Category B

    def test_06_tool_get_weather_data_regional_hubs(self):
        """Test regional hubs."""
        hubs = ["Guwahati", "Shillong", "Aizawl", "Kohima", "Itanagar", "Agartala", "Gangtok"]
        for hub in hubs:
            res = get_weather_data(hub)
            self.assertEqual(res.get("location"), hub)
            self.assertIn("temperature_celsius", res)
            self.assertIn("rainfall_mm", res)
        print(f"[TEST 6] Successfully queried telemetry for all 7 NER hubs: {', '.join(hubs)}")

    def test_07_tool_predict_route_safety_score_callable(self):
        """Test route tool."""
        res = predict_route_safety_score(22.0, 10.0, 15.0, 10.0)
        self.assertIn("safety_score", res)
        self.assertIn("risk_level", res)
        self.assertIn("alert_message", res)
        print(f"[TEST 7] Tool predict_route_safety_score: Score={res['safety_score']}, Risk={res['risk_level']}")

    def test_08_tool_get_road_status_highways(self):
        """Test highway status."""
        res_nh6 = get_road_status("Guwahati to Shillong NH-6")
        self.assertIn("status", res_nh6)
        self.assertIn("route", res_nh6)
        print(f"[TEST 8] Road status for NH-6: {res_nh6['status']}")

    def test_09_tool_get_community_feedback(self):
        """Test community feedback."""
        res = get_community_feedback("Shillong to Sohra")
        self.assertIn("reports_summary", res)
        self.assertIn("total_reports", res)
        print(f"[TEST 9] Community feedback reports found: {res['total_reports']} reports")

    def test_10_tool_translate_response_regional_languages(self):
        """Test regional translation."""
        sample_text = "Route is safe for transport."
        for lang in ["hindi", "assamese", "bengali", "mizo"]:
            translated = translate_response(sample_text, lang)
            self.assertIn("translated_text", translated)
            self.assertEqual(translated.get("language_code"), lang)
        print("[TEST 10] Translation verified across 4 regional North Eastern languages")

    # Category C

    def test_11_route_risk_classifier_low_risk(self):
        """Test low risk."""
        pred = self.risk_classifier.predict([10.0, 1.0, 25.0, 90.0])
        print(f"[TEST 11] Optimal Route: Risk={pred['risk_label']}, Confidence={pred['confidence']:.2f}")
        self.assertIn(pred["risk_label"], ["LOW", "MODERATE"])

    def test_12_route_risk_classifier_critical_hazard(self):
        """Test critical hazard."""
        pred = self.risk_classifier.predict([85.0, 9.0, 0.5, 20.0])
        print(f"[TEST 12] Imminent Landslide Route: Risk={pred['risk_label']}, Confidence={pred['confidence']:.2f}")
        self.assertIn(pred["risk_label"], ["HIGH", "CRITICAL"])

    def test_13_orchestrator_accessibility_guwahati_to_shillong(self):
        """Test accessibility corridor."""
        output = self.orchestrator.execute_accessibility_analysis("Guwahati to Shillong")
        self.assertIn("Guwahati to Shillong", output)
        self.assertIn("Status", output)
        print("[TEST 13] Accessibility analysis for Guwahati -> Shillong verified")

    def test_14_orchestrator_alert_monitoring_sohra_landslides(self):
        """Test alert monitoring."""
        output = self.orchestrator.execute_alert_monitoring("Sohra Landslide Zone", radius=10.0)
        self.assertIn("Safety Alert Report", output)
        self.assertIn("Severity Level", output)
        print("[TEST 14] Alert monitoring triggered high-risk evaluation for Sohra")

    # Category D

    def test_15_intent_detection_weather_only(self):
        """Test weather intent."""
        intent = detect_query_intent("What is the current rainfall and temperature in Shillong?")
        routing = self.orchestrator.determine_agent_routing(intent)
        print(f"[TEST 15] Weather query routing: {routing['agents_to_invoke']}")
        self.assertTrue(routing['invoke_weather'])
        self.assertFalse(routing['invoke_alert'])

    def test_16_intent_detection_route_only(self):
        """Test route intent."""
        intent = detect_query_intent("How is the road condition from Guwahati to Kohima highway?")
        routing = self.orchestrator.determine_agent_routing(intent)
        print(f"[TEST 16] Route query routing: {routing['agents_to_invoke']}")
        self.assertTrue(routing['invoke_accessibility'])
        self.assertTrue(routing['invoke_weather'])

    def test_17_intent_detection_full_emergency_alerts(self):
        """Test emergency intent."""
        intent = detect_query_intent("Warning: Landslide danger and flood alerts on route to Aizawl. Is it safe to drive?")
        routing = self.orchestrator.determine_agent_routing(intent)
        print(f"[TEST 17] Emergency query routing: {routing['agents_to_invoke']}")
        self.assertTrue(routing['invoke_weather'])
        self.assertTrue(routing['invoke_accessibility'])
        self.assertTrue(routing['invoke_alert'])

    # Category E

    def test_18_flask_api_health_check(self):
        """Test health endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertEqual(payload.get("status"), "online")
        self.assertIn("weather_ml_model", payload)
        print(f"[TEST 18] Health Check Endpoint Response: {payload}")

    def test_19_flask_api_chat_full_pipeline(self):
        """Test chat pipeline."""
        req_body = {
            "query": "Is it safe to send logistics convoys to Shillong today?",
            "location": "Shillong",
            "target_language": "hindi"
        }
        response = self.client.post(
            "/api/chat",
            data=json.dumps(req_body),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertTrue(payload.get("success"))
        self.assertIn("final_response", payload)
        self.assertIn("translated_response", payload)
        print("\n[TEST 19] POST /api/chat Response Preview:")
        print(payload["translated_response"][:200] + "...")

    def test_20_flask_api_predict_weather_safety(self):
        """Test ML endpoint."""
        req_body = {
            "temperature": 21.5,
            "precipitation": 12.0,
            "wind_speed": 18.0,
            "visibility": 9.5
        }
        response = self.client.post(
            "/api/predict-weather-safety",
            data=json.dumps(req_body),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertTrue(payload.get("success"))
        self.assertIn("safety_score", payload)
        self.assertIn("risk_level", payload)
        print(f"[TEST 20] POST /api/predict-weather-safety: Score={payload['safety_score']}, Risk={payload['risk_level']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
