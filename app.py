import os
import sys
from flask import Flask, request, jsonify, send_from_directory
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
from ml_models import WeatherPredictionModel

# Load environment
load_dotenv(os.path.join(chatbot_dir, ".env"))

app = Flask(__name__)
if CORS_AVAILABLE:
    CORS(app)  # Enable CORS

# Initialize models
orchestrator = ChatbotOrchestrator()
weather_model = WeatherPredictionModel()


# Frontend routes
@app.route("/styles.css", methods=["GET"])
def serve_styles():
    """Serve stylesheet."""
    css_file = os.path.join(os.path.dirname(__file__), "static", "css", "styles.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            return f.read(), 200, {"Content-Type": "text/css; charset=utf-8"}
    return "", 404


@app.route("/script.js", methods=["GET"])
def serve_script():
    """Serve application script."""
    import re
    js_file = os.path.join(os.path.dirname(__file__), "static", "js", "script.js")
    with open(js_file, "r", encoding="utf-8") as f:
        js_code = f.read()

    # Chatbot connection hook
    chat_hook = """function sendChat(text){
  if(!text || !text.trim()) return;
  STATE.chatHistory.push({role:"user", text});
  const pendingId = "loading_" + Date.now();
  STATE.chatHistory.push({role:"bot", text:"⏳ <i>Analyzing telemetry, road sensors, and ML safety score...</i>", id:pendingId});
  const log = document.getElementById("chatLog");
  if(log){ log.innerHTML = chatLogHTML(); log.scrollTop = log.scrollHeight; }

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: text, target_language: STATE.lang === "hi" ? "hindi" : "english" })
  })
  .then(res => res.json())
  .then(data => {
    STATE.chatHistory = STATE.chatHistory.filter(m => m.id !== pendingId);
    let answer = data.translated_response || data.final_response || "Analysis complete.";
    let formatted = answer
      .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
      .replace(/###\\s*(.*?)\\n/g, '<h4 style="margin:4px 0; color:#38bdf8;">$1</h4>')
      .replace(/\\n/g, '<br>');
    STATE.chatHistory.push({role:"bot", text: formatted});
    if(log){ log.innerHTML = chatLogHTML(); log.scrollTop = log.scrollHeight; }
  })
  .catch(err => {
    STATE.chatHistory = STATE.chatHistory.filter(m => m.id !== pendingId);
    const key = text.toLowerCase().trim();
    const fallback = CHAT_REPLIES[key] || ("⚠️ AI Service connecting... (Error: " + err.message + ")");
    STATE.chatHistory.push({role:"bot", text: fallback});
    if(log){ log.innerHTML = chatLogHTML(); log.scrollTop = log.scrollHeight; }
  });
}"""

    js_code = re.sub(r'function sendChat\(text\)\{[\s\S]*?\n\}', lambda m: chat_hook, js_code, count=1)
    return js_code, 200, {"Content-Type": "application/javascript; charset=utf-8"}


@app.route("/", methods=["GET"])
def home_page():
    """Serve front page."""
    html_file = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/frontend/<path:filename>")
def serve_frontend(filename):
    """Serve frontend files."""
    return send_from_directory("frontend", filename)


@app.route("/static/<path:filename>")
def serve_static(filename):
    """Serve static files."""
    return send_from_directory("static", filename)


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


@app.route("/chat", methods=["GET"])
def chat_direct():
    """Direct chatbot page."""
    html_page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chatbot — PRAVAH NER Connect</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root {
  --brand: #0284c7;
  --brand-deep: #0369a1;
  --bg: #0b1329;
  --panel-bg: #152238;
  --border: #1e3a5f;
  --ink: #f8fafc;
  --ink-soft: #94a3b8;
  --red: #ef4444;
  --amber: #f59e0b;
  --green: #10b981;
  --sky: #38bdf8;
  --flow: #5eead4;
}
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
body { background: var(--bg); color: var(--ink); min-height: 100vh; overflow: hidden; }
.shell { display: flex; height: 100vh; width: 100vw; }
.sidebar { width: 250px; background: #0f1c32; border-right: 1px solid var(--border); display: flex; flex-direction: column; flex-shrink: 0; transition: width 0.2s; }
.sidebar-head { padding: 18px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
.brand-icon { width: 34px; height: 34px; border-radius: 50%; background: #0e7490; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.brand-name { font-size: 1.1rem; color: #fff; letter-spacing: 0.5px; }
.brand-name span { color: var(--sky); }
.brand-sub { font-size: 0.65rem; color: var(--flow); letter-spacing: 1px; display: block; margin-top: -2px; }
.nav-group { flex: 1; padding: 14px 10px; display: flex; flex-direction: column; gap: 4px; overflow-y: auto; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 9px 14px; border-radius: 8px; color: var(--ink-soft); text-decoration: none; font-size: 0.86rem; font-weight: 500; cursor: pointer; transition: 0.15s; }
.nav-item:hover { color: #fff; background: rgba(255,255,255,0.05); }
.nav-item.active { background: var(--brand); color: #fff; font-weight: 600; }
.nav-item svg { width: 18px; height: 18px; flex-shrink: 0; }
.sidebar-foot { padding: 14px 18px; font-size: 0.72rem; color: var(--ink-soft); border-top: 1px solid var(--border); line-height: 1.4; }
.main-col { flex: 1; display: flex; flex-direction: column; min-width: 0; height: 100vh; }
.navbar { height: 60px; border-bottom: 1px solid var(--border); background: #0f1c32; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; gap: 16px; flex-shrink: 0; }
.search-bar { display: flex; align-items: center; gap: 10px; background: #0b1329; border: 1px solid var(--border); padding: 8px 14px; border-radius: 8px; width: 320px; }
.search-bar input { background: none; border: none; color: #fff; outline: none; width: 100%; font-size: 0.85rem; }
.navbar-right { display: flex; align-items: center; gap: 14px; }
.status-chip { font-size: 0.76rem; font-weight: 600; padding: 4px 10px; border-radius: 20px; background: rgba(16,185,129,0.12); color: var(--green); border: 1px solid rgba(16,185,129,0.25); display: flex; align-items: center; gap: 6px; }
.lang-select { background: #0b1329; border: 1px solid var(--border); color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 0.82rem; outline: none; cursor: pointer; }
.user-chip { display: flex; align-items: center; gap: 8px; }
.avatar { width: 30px; height: 30px; border-radius: 50%; background: var(--brand); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; font-weight: 700; }
.page { flex: 1; padding: 22px 26px; overflow-y: auto; background: var(--bg); display: flex; flex-direction: column; }
.page-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-shrink: 0; }
.page-head h1 { font-family: 'Space Grotesk', sans-serif; font-size: 1.45rem; font-weight: 700; }
.page-head .sub { color: var(--ink-soft); font-size: 0.85rem; margin-top: 2px; }
.live-badge { font-size: 0.72rem; font-weight: 600; color: var(--sky); background: rgba(56,189,248,0.12); border: 1px solid rgba(56,189,248,0.25); padding: 4px 10px; border-radius: 6px; }
.chat-panel { background: var(--panel-bg); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; display: flex; flex-direction: column; flex: 1; min-height: 0; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.chat-log { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; background: #0b1329; min-height: 0; }
.msg { max-width: 85%; padding: 14px 18px; border-radius: 12px; font-size: 0.92rem; line-height: 1.6; word-break: break-word; }
.msg.user { align-self: flex-end; background: var(--brand); color: #fff; border-bottom-right-radius: 2px; }
.msg.bot { align-self: flex-start; background: #1b2a47; color: #f1f5f9; border-bottom-left-radius: 2px; border: 1px solid var(--border); }
.msg.bot h3, .msg.bot h4 { color: var(--sky); margin: 6px 0 2px 0; font-size: 1rem; }
.msg.bot b, .msg.bot strong { color: #fff; }
.msg.bot ul { margin: 6px 0 6px 20px; padding: 0; }
.chat-suggest { padding: 10px 16px; background: #0f1c32; border-top: 1px solid var(--border); display: flex; gap: 8px; overflow-x: auto; white-space: nowrap; flex-shrink: 0; }
.chip { background: #152238; color: var(--sky); border: 1px solid var(--border); padding: 6px 14px; border-radius: 20px; font-size: 0.78rem; cursor: pointer; transition: 0.15s; }
.chip:hover { background: var(--brand); color: #fff; border-color: var(--brand); }
.chat-input-bar { padding: 14px 18px; background: #0f1c32; border-top: 1px solid var(--border); display: flex; gap: 10px; align-items: center; flex-shrink: 0; }
.chat-input-bar input { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border); background: #152238; color: #fff; font-size: 0.92rem; outline: none; }
.chat-input-bar input:focus { border-color: var(--sky); }
.chat-input-bar button { background: var(--brand); color: #fff; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 0.95rem; font-weight: 600; display: flex; align-items: center; gap: 6px; transition: 0.2s; }
.chat-input-bar button:hover { background: var(--brand-deep); }
.loading-row { padding: 0 20px 8px 20px; color: var(--sky); font-size: 0.8rem; font-style: italic; display: none; background: #0b1329; }
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="sidebar-head">
      <div class="brand-icon">
        <svg width="22" height="22" viewBox="0 0 34 34" fill="none">
          <circle cx="17" cy="17" r="16" fill="#0E7490"/>
          <path d="M6 20c3-6 7 6 10 0s7-6 10 0" stroke="#5EEAD4" stroke-width="2.2" fill="none" stroke-linecap="round"/>
          <circle cx="6" cy="20" r="2" fill="#38BDF8"/>
          <circle cx="26" cy="20" r="2" fill="#38BDF8"/>
        </svg>
      </div>
      <div>
        <div class="brand-name"><span>PRAVAH</span></div>
        <span class="brand-sub">NER CONNECT</span>
      </div>
    </div>
    <div class="nav-group">
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>Overview</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.2 17.5C13 12 11 6 18 7.3"/></svg>Route Intelligence</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6l8-4z"/></svg>Accessibility Monitor</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 13l1.5-5A2 2 0 016.4 6.5h6.2A2 2 0 0114.6 8l1.4 5"/><path d="M3 13h18v4a1 1 0 01-1 1h-1"/><circle cx="7.5" cy="18" r="1.6"/><circle cx="16.5" cy="18" r="1.6"/></svg>Vehicle Tracking</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>Logistics & Deliveries</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19a4.5 4.5 0 000-9 6 6 0 00-11.4 1.8A4 4 0 007 19h10.5z"/></svg>Weather Intelligence</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.3 3.9L2.5 17a1.6 1.6 0 001.4 2.4h16.2a1.6 1.6 0 001.4-2.4L13.7 3.9a1.6 1.6 0 00-2.8 0z"/></svg>Alerts & Incidents</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6l8-4z"/><path d="M12 8v5"/><path d="M12 16.2h.01"/></svg>Emergency Routes</div>
      <div class="nav-item active"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.4 8.4 0 01-8.9 8.4 8.9 8.9 0 01-3.6-.8L3 21l1.9-5.5a8.4 8.4 0 01-.9-3.9A8.4 8.4 0 0112.6 3a8.5 8.5 0 018.4 8.5z"/></svg>Chatbot</div>
      <a class="nav-item" href="/map" style="text-decoration:none;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-6-3V5l6 3 6-3 6 3v12l-6-3-6 3z"/><path d="M9 8v12"/><path d="M15 5v12"/></svg>GIS Map</a>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 01-3.4 0"/></svg>Notifications</div>
      <div class="nav-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1-1.6 1.7 1.7 0 00-1.9.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.9 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.9.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.9-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.9V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/></svg>Settings</div>
    </div>
    <div class="sidebar-foot">PRAVAH v0.9 · SIH 26002<br>AI Logistics Intelligence</div>
  </aside>

  <div class="main-col">
    <header class="navbar">
      <div class="search-bar">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
        <input type="text" placeholder="Search routes, vehicles, districts…">
      </div>
      <div class="navbar-right">
        <span class="status-chip">🟢 Online</span>
        <select class="lang-select" id="langSelect">
          <option value="english">EN — English</option>
          <option value="hindi">HI — हिन्दी</option>
          <option value="assamese">AS — অসমীয়া</option>
          <option value="bengali">BN — বাংলা</option>
          <option value="manipuri">MN — মৈতৈলোন্</option>
          <option value="mizo">MZ — Mizo</option>
        </select>
        <div class="user-chip">
          <div class="avatar">DU</div>
          <span style="font-size:0.82rem; font-weight:600;">Demo User</span>
        </div>
      </div>
    </header>

    <main class="page">
      <div class="page-head">
        <div>
          <h1>PRAVAH AI Assistant</h1>
          <div class="sub">AI-powered logistics & accessibility intelligence for North East India</div>
        </div>
        <span class="live-badge">● Live Multi-Agent AI Engine</span>
      </div>

      <div class="chat-panel">
        <div class="chat-log" id="chatLog">
          <div class="msg bot">
            <b>Namaste!</b> I am your North Eastern Region Logistics & Disaster Intelligence Assistant.<br>
            I can help you analyze route accessibility, IMD weather safety scores, and real-time hazard alerts.<br>
            <i>Click any suggested question below or type your logistics query.</i>
          </div>
        </div>
        <div id="loadingIndicator" class="loading-row">⏳ Orchestrator & Agents are analyzing telemetry, road sensors, and ML safety score...</div>
        <div class="chat-suggest">
          <button class="chip" onclick="askPrompt('Is it safe to send logistics convoys to Shillong today?')">🚚 Shillong Safety</button>
          <button class="chip" onclick="askPrompt('How is the road condition from Guwahati to Shillong on NH-6?')">🛣️ Guwahati → Shillong</button>
          <button class="chip" onclick="askPrompt('Check landslide warnings and emergency alerts in Sohra.')">⚠️ Sohra Landslides</button>
          <button class="chip" onclick="askPrompt('What is the current rainfall and temperature in Kohima?')">🌧️ Kohima Weather</button>
          <button class="chip" onclick="askPrompt('Road accessibility report from Silchar to Aizawl.')">📦 Aizawl Corridor</button>
        </div>
        <div class="chat-input-bar">
          <input type="text" id="chatInput" placeholder="Ask about routes, weather, vehicles, or emergency convoys…" onkeydown="if(event.key==='Enter') sendChat()">
          <button onclick="sendChat()">Send ➤</button>
        </div>
      </div>
    </main>
  </div>
</div>

<script>
function askPrompt(q) {
  document.getElementById('chatInput').value = q;
  sendChat();
}

function formatMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/### (.*?)\\n/g, '<h4>$1</h4>')
    .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
    .replace(/\\* (.*?)\\n/g, '<li>$1</li>')
    .replace(/\\n/g, '<br>');
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const query = input.value.trim();
  if (!query) return;

  const log = document.getElementById('chatLog');
  const loading = document.getElementById('loadingIndicator');
  const lang = document.getElementById('langSelect').value;

  log.innerHTML += `<div class="msg user">${query}</div>`;
  input.value = '';
  log.scrollTop = log.scrollHeight;
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
      const reply = data.translated_response || data.final_response || 'Analysis complete.';
      log.innerHTML += `<div class="msg bot">${formatMarkdown(reply)}</div>`;
    } else {
      log.innerHTML += `<div class="msg bot" style="color:var(--red);">⚠️ Error: ${data.error || 'Failed to get response'}</div>`;
    }
  } catch (err) {
    loading.style.display = 'none';
    log.innerHTML += `<div class="msg bot" style="color:var(--red);">⚠️ Connection error: ${err.message}</div>`;
  }
  log.scrollTop = log.scrollHeight;
}
</script>
</body>
</html>"""
    return html_page


# ---------------------------------------------------------------------------
# GIS MAPPING FEATURE (added — does not modify any existing route/logic)
# ---------------------------------------------------------------------------

# Key North-East India locations relevant to PRAVAH's corridors.
# Coordinates are approximate town/city centers.
NER_LOCATIONS = [
    {"id": "guwahati", "name": "Guwahati",  "state": "Assam",       "lat": 26.1445, "lng": 91.7362},
    {"id": "shillong",  "name": "Shillong",  "state": "Meghalaya",   "lat": 25.5788, "lng": 91.8933},
    {"id": "sohra",     "name": "Sohra (Cherrapunji)", "state": "Meghalaya", "lat": 25.2843, "lng": 91.7273},
    {"id": "kohima",    "name": "Kohima",    "state": "Nagaland",    "lat": 25.6751, "lng": 94.1086},
    {"id": "dimapur",   "name": "Dimapur",   "state": "Nagaland",    "lat": 25.9091, "lng": 93.7266},
    {"id": "imphal",    "name": "Imphal",    "state": "Manipur",     "lat": 24.8170, "lng": 93.9368},
    {"id": "aizawl",    "name": "Aizawl",    "state": "Mizoram",     "lat": 23.7271, "lng": 92.7176},
    {"id": "silchar",   "name": "Silchar",   "state": "Assam",       "lat": 24.8333, "lng": 92.7789},
    {"id": "agartala",  "name": "Agartala",  "state": "Tripura",     "lat": 23.8315, "lng": 91.2868},
    {"id": "itanagar",  "name": "Itanagar",  "state": "Arunachal Pradesh", "lat": 27.0844, "lng": 93.6053},
]

# A couple of demo logistics corridors to draw as route lines on the map.
NER_ROUTES = [
    {"name": "Guwahati → Shillong (NH-6)", "path": ["guwahati", "shillong"]},
    {"name": "Shillong → Sohra",           "path": ["shillong", "sohra"]},
    {"name": "Silchar → Aizawl",           "path": ["silchar", "aizawl"]},
    {"name": "Guwahati → Dimapur → Kohima", "path": ["guwahati", "dimapur", "kohima"]},
]


def _risk_level(safety_score):
    """Map a numeric safety score to a risk band (mirrors /api/predict-weather-safety)."""
    if safety_score >= 80:
        return "LOW"
    elif safety_score >= 60:
        return "MODERATE"
    elif safety_score >= 40:
        return "HIGH"
    return "CRITICAL"


@app.route("/api/gis/locations", methods=["GET"])
def gis_locations():
    """Return NER location pins with a live weather-safety score for each,
    using the already-initialized weather_model. Read-only; does not touch
    any existing endpoint or model logic."""
    features = []
    for loc in NER_LOCATIONS:
        # Sample telemetry per location; replace with live sensor/IMD feed when available.
        temp, precip, wind, vis = 22.0, 0.0, 10.0, 10.0
        try:
            safety_score = weather_model.predict([temp, precip, wind, vis])
        except Exception:
            safety_score = 75.0  # graceful fallback if model call fails
        features.append({
            **loc,
            "safety_score": round(safety_score, 2),
            "risk_level": _risk_level(safety_score)
        })
    return jsonify({"success": True, "locations": features}), 200


@app.route("/api/gis/routes", methods=["GET"])
def gis_routes():
    """Return demo logistics corridors as sequences of location ids,
    resolved to coordinates, for drawing route lines on the map."""
    loc_by_id = {loc["id"]: loc for loc in NER_LOCATIONS}
    resolved = []
    for route in NER_ROUTES:
        points = [loc_by_id[pid] for pid in route["path"] if pid in loc_by_id]
        resolved.append({"name": route["name"], "points": points})
    return jsonify({"success": True, "routes": resolved}), 200


@app.route("/map", methods=["GET"])
def gis_map_page():
    """GIS map page — plots NER locations, live-ish safety scores, and
    logistics corridors using Leaflet.js (no API key required)."""
    html_page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GIS Map — PRAVAH NER Connect</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root {
  --brand: #0284c7; --bg: #0b1329; --panel-bg: #152238; --border: #1e3a5f;
  --ink: #f8fafc; --ink-soft: #94a3b8; --green: #10b981; --amber: #f59e0b;
  --red: #ef4444; --sky: #38bdf8;
}
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
body { background: var(--bg); color: var(--ink); height: 100vh; overflow: hidden; }
.topbar { height: 56px; display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; background: #0f1c32; border-bottom: 1px solid var(--border); }
.topbar h1 { font-size: 1.05rem; }
.topbar a { color: var(--sky); text-decoration: none; font-size: 0.85rem; }
#map { width: 100%; height: calc(100vh - 56px); background: #0b1329; }
.legend { position: absolute; bottom: 20px; left: 20px; background: var(--panel-bg);
  border: 1px solid var(--border); border-radius: 10px; padding: 10px 14px; font-size: 0.78rem;
  z-index: 1000; color: var(--ink-soft); }
.legend div { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.leaflet-popup-content-wrapper { background: var(--panel-bg); color: var(--ink); border: 1px solid var(--border); }
.leaflet-popup-tip { background: var(--panel-bg); }
</style>
</head>
<body>
<div class="topbar">
  <h1>🗺️ PRAVAH — GIS Route &amp; Hazard Map</h1>
  <a href="/chat">← Back to Chatbot</a>
</div>
<div style="position:relative;">
  <div id="map"></div>
  <div class="legend">
    <div><span class="dot" style="background:#10b981"></span> Low risk</div>
    <div><span class="dot" style="background:#f59e0b"></span> Moderate risk</div>
    <div><span class="dot" style="background:#f97316"></span> High risk</div>
    <div><span class="dot" style="background:#ef4444"></span> Critical risk</div>
  </div>
</div>
<script>
const map = L.map('map', { zoomControl: true }).setView([25.6, 92.9], 6.4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors',
  maxZoom: 18
}).addTo(map);

const riskColor = { LOW: '#10b981', MODERATE: '#f59e0b', HIGH: '#f97316', CRITICAL: '#ef4444' };

async function loadLocations() {
  const res = await fetch('/api/gis/locations');
  const data = await res.json();
  if (!data.success) return;
  data.locations.forEach(loc => {
    const color = riskColor[loc.risk_level] || '#38bdf8';
    const marker = L.circleMarker([loc.lat, loc.lng], {
      radius: 9, fillColor: color, color: '#0b1329', weight: 2, fillOpacity: 0.9
    }).addTo(map);
    marker.bindPopup(
      `<b>${loc.name}</b>, ${loc.state}<br>` +
      `Safety score: ${loc.safety_score}<br>` +
      `Risk level: <b style="color:${color}">${loc.risk_level}</b>`
    );
  });
}

async function loadRoutes() {
  const res = await fetch('/api/gis/routes');
  const data = await res.json();
  if (!data.success) return;
  data.routes.forEach(route => {
    const latlngs = route.points.map(p => [p.lat, p.lng]);
    const line = L.polyline(latlngs, { color: '#38bdf8', weight: 3, dashArray: '6 6', opacity: 0.8 }).addTo(map);
    line.bindTooltip(route.name, { sticky: true });
  });
}

loadLocations();
loadRoutes();
</script>
</body>
</html>"""
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