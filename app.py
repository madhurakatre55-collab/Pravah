import os
import sys
from flask import Flask, request, jsonify
from dotenv import load_dotenv

try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

# Setup path
chatbot_dir = os.path.join(os.path.dirname(__file__), "Backend", "ChatBot")
if chatbot_dir not in sys.path:
    sys.path.append(chatbot_dir)

from mains import ChatbotOrchestrator
from ml_models import WeatherPredictionModel, RouteRiskClassifier

# Load environment
load_dotenv(os.path.join(chatbot_dir, ".env"))

app = Flask(__name__)
if CORS_AVAILABLE:
    CORS(app)  # Enable CORS

# Initialize models
orchestrator = ChatbotOrchestrator()
weather_model = WeatherPredictionModel()
risk_classifier = RouteRiskClassifier()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check."""
    weather_info = weather_model.get_model_info()
    return jsonify({
        "status": "online",
        "service": "NER Disaster & Accessibility Chatbot API (SIH 2026)",
        "weather_ml_model": weather_info.get("status", "Unknown"),
        "groq_api_configured": bool(os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY"))
    }), 200


@app.route("/", methods=["GET"])
def chat_ui():
    """Web chat interface."""
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pravah - NER Disaster & Logistics Intelligence Chatbot</title>
        <style>
            * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { background: #0b1329; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; min-height: 100vh; }
            .chat-container { width: 100%; max-width: 900px; background: #152238; border: 1px solid #1e3a5f; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); overflow: hidden; display: flex; flex-direction: column; height: 92vh; }
            .chat-header { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #38bdf8; }
            .chat-header h2 { margin: 0; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px; }
            .badge-container { display: flex; gap: 8px; align-items: center; }
            .badge { background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 9999px; font-size: 0.78rem; font-weight: 600; }
            .pills { display: flex; gap: 8px; padding: 12px 20px; background: #0f1c32; border-bottom: 1px solid #1e3a5f; overflow-x: auto; white-space: nowrap; }
            .pill { background: #1e3a5f; color: #38bdf8; border: 1px solid #0284c7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
            .pill:hover { background: #0284c7; color: #ffffff; }
            .messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; background: #0b1329; }
            .msg { max-width: 85%; padding: 14px 18px; border-radius: 12px; line-height: 1.6; word-break: break-word; }
            .user-msg { align-self: flex-end; background: #0284c7; color: #fff; border-bottom-right-radius: 2px; }
            .bot-msg { align-self: flex-start; background: #1b2a47; color: #f1f5f9; border-bottom-left-radius: 2px; border: 1px solid #23385d; }
            .bot-msg h3, .bot-msg h4 { margin: 8px 0 4px 0; color: #38bdf8; }
            .bot-msg ul { margin: 4px 0 8px 18px; padding: 0; }
            .bot-msg strong { color: #f8fafc; font-weight: 700; }
            .controls { padding: 16px 20px; background: #0f1c32; border-top: 1px solid #1e3a5f; display: flex; gap: 10px; align-items: center; }
            input[type="text"] { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid #334e77; background: #152238; color: #fff; font-size: 0.95rem; outline: none; transition: border 0.2s; }
            input[type="text"]:focus { border-color: #38bdf8; }
            select { padding: 12px; border-radius: 8px; border: 1px solid #334e77; background: #152238; color: #fff; outline: none; cursor: pointer; }
            button { background: #0284c7; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
            button:hover { background: #0369a1; }
            .loading { color: #38bdf8; font-size: 0.85rem; font-style: italic; display: none; padding: 0 20px 8px 20px; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h2>🛰️ Pravah Intelligence Chatbot</h2>
                <div class="badge-container">
                    <span class="badge">Multi-Agent Flow</span>
                    <span class="badge">IMD Trained ML</span>
                </div>
            </div>
            <div class="pills">
                <span class="pill" onclick="fillQuery('Is it safe to send logistics convoys to Shillong today?')">🚚 Shillong Safety</span>
                <span class="pill" onclick="fillQuery('How is the road condition from Guwahati to Shillong on NH-6?')">🛣️ Guwahati → Shillong</span>
                <span class="pill" onclick="fillQuery('Check landslide warnings and emergency alerts in Sohra.')">⚠️ Sohra Landslides</span>
                <span class="pill" onclick="fillQuery('What is the current rainfall and temperature in Kohima?')">🌧️ Kohima Weather</span>
                <span class="pill" onclick="fillQuery('Road accessibility report from Silchar to Aizawl.')">📦 Aizawl Corridor</span>
            </div>
            <div class="messages" id="chatBox">
                <div class="msg bot-msg">
                    <strong>Namaste!</strong> I am your North Eastern Region Logistics & Disaster Intelligence Assistant.<br>
                    Ask me any question about:
                    <ul>
                        <li><b>Weather Safety & ML Predictions</b> (0-100 safety score)</li>
                        <li><b>Road Accessibility & Highway Closures</b> (NH-6, NH-27, landslides)</li>
                        <li><b>Emergency Disaster Alerts & Detours</b></li>
                    </ul>
                    <i>Click any quick prompt above or type your question below!</i>
                </div>
            </div>
            <span id="loadingIndicator" class="loading">🤖 Orchestrator & Agents are analyzing weather telemetry, ML safety score, and road sensors...</span>
            <div class="controls">
                <input type="text" id="userInput" placeholder="Ask about route safety, weather, or alerts..." onkeydown="if(event.key==='Enter') sendQuery()" />
                <select id="langSelect">
                    <option value="english">English</option>
                    <option value="hindi">Hindi (हिंदी)</option>
                    <option value="assamese">Assamese (অসমীয়া)</option>
                    <option value="bengali">Bengali (বাংলা)</option>
                    <option value="manipuri">Manipuri (মৈতৈলোন্)</option>
                    <option value="mizo">Mizo</option>
                </select>
                <button onclick="sendQuery()">Send</button>
            </div>
        </div>
        <script>
            function fillQuery(text) {
                document.getElementById('userInput').value = text;
                sendQuery();
            }

            function formatMarkdown(text) {
                if (!text) return '';
                let formatted = text
                    .replace(/### (.*?)\\n/g, '<h3>$1</h3>')
                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\* (.*?)\\n/g, '<li>$1</li>')
                    .replace(/\\n/g, '<br>');
                return formatted;
            }

            async function sendQuery() {
                const input = document.getElementById('userInput');
                const lang = document.getElementById('langSelect').value;
                const query = input.value.trim();
                if (!query) return;

                const chatBox = document.getElementById('chatBox');
                const loading = document.getElementById('loadingIndicator');

                chatBox.innerHTML += `<div class="msg user-msg">${query}</div>`;
                input.value = '';
                chatBox.scrollTop = chatBox.scrollHeight;
                loading.style.display = 'block';

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: query, target_language: lang })
                    });
                    const data = await res.json();
                    loading.style.display = 'none';

                    if (data.success) {
                        const rawReply = data.translated_response || data.final_response || JSON.stringify(data.agent_results, null, 2);
                        chatBox.innerHTML += `<div class="msg bot-msg">${formatMarkdown(rawReply)}</div>`;
                    } else {
                        chatBox.innerHTML += `<div class="msg bot-msg" style="color:#ef4444;">Error: ${data.error || 'Failed to get response'}</div>`;
                    }
                } catch (err) {
                    loading.style.display = 'none';
                    chatBox.innerHTML += `<div class="msg bot-msg" style="color:#ef4444;">Connection error: ${err.message}</div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return html_page



@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat API."""
    data = request.get_json() or {}
    query = data.get("query")
    
    if not query:
        return jsonify({
            "error": "Missing required field 'query' in request JSON body."
        }), 400
        
    location = data.get("location")
    start_location = data.get("start_location")
    end_location = data.get("end_location")
    target_language = data.get("target_language", "english")
    
    try:
        # Execute workflow
        result = orchestrator.process_query(
            query=query,
            location=location,
            start_location=start_location,
            end_location=end_location
        )
        
        # Translate response
        if target_language and target_language.lower() != "english":
            translated_res = orchestrator.execute_translation(
                text=result['final_response'],
                target_language=target_language
            )
            result['translated_response'] = translated_res
            
        return jsonify({
            "success": True,
            "query": query,
            "intent": result.get("intent"),
            "routing_decision": result.get("routing_decision"),
            "agent_results": result.get("agent_results"),
            "final_response": result.get("final_response"),
            "translated_response": result.get("translated_response")
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "An error occurred during agent workflow execution."
        }), 500


@app.route("/api/predict-weather-safety", methods=["POST"])
def predict_weather_safety():
    """ML prediction endpoint."""
    data = request.get_json() or {}
    temp = float(data.get("temperature", 22.0))
    precip = float(data.get("precipitation", 0.0))
    wind = float(data.get("wind_speed", 10.0))
    vis = float(data.get("visibility", 10.0))
    
    safety_score = weather_model.predict([temp, precip, wind, vis])
    if safety_score >= 80:
        risk_level = "LOW"
    elif safety_score >= 60:
        risk_level = "MODERATE"
    elif safety_score >= 40:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return jsonify({
        "success": True,
        "safety_score": round(safety_score, 2),
        "risk_level": risk_level,
        "temperature_celsius": temp,
        "precipitation_mm": precip,
        "wind_speed_kmh": wind,
        "visibility_km": vis
    }), 200


if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[START] Starting NER Chatbot API Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
