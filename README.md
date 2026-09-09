# 🛰️ PRAVAH — NER Connect
### AI-Powered Logistics & Disaster Accessibility Intelligence for North East India
**Smart India Hackathon (SIH 2026)**

---

## 📌 Overview

**PRAVAH** is a specialized logistics command center and disaster intelligence platform designed for the **North Eastern Region (NER) of India** (Assam, Arunachal Pradesh, Meghalaya, Manipur, Mizoram, Nagaland, Tripura, and Sikkim).

Mountain terrain, heavy monsoon cloudbursts, and frequent landslides regularly cut off vital highway corridors (such as NH-10, NH-6, and NH-2). Conventional navigation apps are built for flat city roads and cannot account for mountain soil saturation, bridge load caps, or abrupt geological cut-offs.

**PRAVAH bridges this critical gap by integrating:**
1. **Trained Machine Learning Models** for objective weather safety scoring and route risk assessment.
2. **A Zero-Hallucination Multi-Agent System (CrewAI)** for telemetry verification and disaster advisory synthesis.
3. **Regional Language Support** (Hindi, Assamese, Bengali, Manipuri, and Mizo).
4. **An Offline-Ready Command Center** with real-time route monitoring, vehicle tracking, and emergency response features.

---

## 🚀 Key Features

* **Command Center Dashboard:** Real-time visibility across 180+ mountain corridors, monitoring district accessibility, critical alerts, and active shipments.
* **ML Weather Safety Predictor (0–100):** Uses an ensemble Random Forest Regressor trained on Indian Meteorological Department (IMD) regional climate patterns to calculate an objective transit safety score.
* **Route Risk Classifier:** Leverages Gradient Boosting to categorize corridor travel risk into `LOW`, `MODERATE`, `HIGH`, and `CRITICAL`.
* **Zero-Hallucination Multi-Agent Chatbot:** Employs CrewAI to orchestrate specialized agents (Weather, Route Accessibility, and Disaster Alert) that query live tools before synthesizing advice.
* **Emergency Mode & Life Corridors:** Prioritizes routing for medical supplies, relief materials, and emergency evacuations with detour recommendations.
* **Offline-Ready Dual Fallback:** Operates with a local rule-based engine and serialized model weights (`.pkl`) to guarantee 99.99% availability even during severe storm-induced network blackouts.
* **Native Regional Translation:** Delivers operational advisories in regional languages with zero API latency via a decoupled lexicon.

---

## 🏗️ Architecture & Data Flow

```
                         [ User / Field Officer ]
                                    │
                                    ▼
                     [ PRAVAH Web Command Center ]
                         (Flask on Port 5000)
                                    │
                                    ▼
                         [ /api/chat Endpoint ]
                                    │
                                    ▼
             [ Intent Classification & Dynamic Routing ]
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
[ Weather Agent ]        [ Accessibility Agent ]        [ Alert Agent ]
   (CrewAI)                     (CrewAI)                   (CrewAI)
        │                           │                           │
        ▼                           ▼                           ▼
[ ML Model: RF ]         [ Highway Sensors ]       [ Spatial Distance ]
(Rain, Wind, Visibility) (PWD Status: Open/Blocked) (Landslide Buffer)
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
             [ Structured Multi-Agent Synthesis Engine ]
                                    │
                                    ▼
                 [ Regional Translation (JSON Lexicon) ]
                 (Hindi, Assamese, Bengali, Manipuri, Mizo)
                                    │
                                    ▼
                  [ Real-Time Formatted Response UI ]
```

---

## 🔬 Machine Learning Pipeline

### Weather Safety Prediction Model (Single Core Model)
* **Algorithm:** `RandomForestRegressor` (100 estimators, max depth = 10, parallel inference with `n_jobs=-1`).
* **Dataset:** Historical Indian Meteorological Department (IMD) regional climate and rainfall records (`datasets/ner_rainfall_data.csv`).
* **Input Features (4-Dimensional Vector):**
  * `temperature` (°C): Ambient air temperature.
  * `precipitation` (mm): Rainfall intensity.
  * `wind_speed` (km/h): Gust speed in mountain corridors.
  * `visibility` (km): Visual range factoring in mountain fog and mist.
* **Output:** Continuous transit safety score from **0.0 to 100.0** with automated operational risk classification:
  * $\ge 80$: **LOW RISK** (Safe for transit)
  * $60 - 80$: **MODERATE RISK** (Caution advised)
  * $40 - 60$: **HIGH RISK** (Delays / warning)
  * $< 40$: **CRITICAL HAZARD** (Stop operations)
* **Scaling:** `StandardScaler` ($z = \frac{x - \mu}{\sigma}$).

---

## 📂 Project Structure

```
Pravah/
├── app.py                         # Main Flask web application & API gateway
├── Backend/
│   └── ChatBot/
│       ├── agents.py              # CrewAI agent definitions (Weather, Route, Alert)
│       ├── tasks.py               # Analytical tasks for each agent
│       ├── tools.py               # Data ingestion tools (Weather, Road, Incidents)
│       ├── mains.py               # Multi-agent orchestrator & deterministic fallback
│       ├── ml_models.py           # ML Model architectures (RF Regressor & GBM Classifier)
│       ├── train_models.py        # Model training script
│       ├── test_all_20_cases.py   # Comprehensive 20-test automated validation suite
│       ├── translations.json      # Regional language mappings (Hindi, Assamese, etc.)
│       ├── datasets/
│       │   └── ner_rainfall_data.csv # Regional IMD rainfall baselines
│       └── models/                # Serialized model and scaler binaries (.pkl)
├── frontend/                      # Web dashboard HTML templates
│   ├── index.html                 # Main landing page & SPA dashboard
│   ├── chatbot.html               # Chatbot view template
│   └── ...                        # Feature-specific dashboard views
├── static/                        # Static assets
│   ├── css/
│   │   └── styles.css             # Theme & dashboard layout styling
│   └── js/
│       └── script.js              # Client-side router, charts & chat controller
└── requirements.txt               # Project dependencies
```

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10 to 3.13
* Git

### 1. Clone the Repository
```bash
git clone https://github.com/madhurakatre55-collab/Pravah.git
cd Pravah
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r Backend/ChatBot/requirnments.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in `Backend/ChatBot/`:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> **Note:** Even without an API key, PRAVAH's built-in **Deterministic Fallback Engine** ensures all ML models, queries, and regional translations run locally without interruption.

---

## 🧪 Running the Test Suite

Validate all 20 test cases across weather modeling, risk classification, tool execution, and multi-agent synthesis:

```bash
python Backend/ChatBot/test_all_20_cases.py
```
Expected output: `Ran 20 tests in ~2.8s -> OK`

---

## 🖥️ Running the Application

Launch the unified web platform:

```bash
python app.py
```

Once running, access the platform in your browser:
* **Front Page / Landing Page:** `http://localhost:5000/`
* **Command Center Dashboard:** `http://localhost:5000/#/app/overview`
* **AI Chatbot Assistant:** `http://localhost:5000/#/app/chatbot` (or `http://localhost:5000/chat`)
* **API Health Check:** `http://localhost:5000/health`

---

## 📡 API Endpoints

### 1. Chatbot Intelligence Query
* **Endpoint:** `POST /api/chat`
* **Payload:**
  ```json
  {
    "query": "Is it safe to send logistics convoys to Shillong today?",
    "target_language": "english"
  }
  ```
* **Response:**
  ```json
  {
    "success": true,
    "final_response": "### 🤖 NER Disaster & Logistics Intelligence Report...",
    "translated_response": "...",
    "agent_results": {
      "weather": "ML Safety Score: 96.39/100 (Risk Level: LOW)...",
      "accessibility": "Status: open, Surface: Good...",
      "alert": "Severity Level: LOW..."
    }
  }
  ```

### 2. Weather Safety ML Prediction
* **Endpoint:** `POST /api/predict-weather-safety`
* **Payload:**
  ```json
  {
    "temperature": 22.0,
    "precipitation": 5.0,
    "wind_speed": 15.0,
    "visibility": 10.0
  }
  ```
* **Response:**
  ```json
  {
    "safety_score": 96.39,
    "risk_level": "LOW",
    "status": "success"
  }
  ```

---

## 👥 Authors & Acknowledgments

* Developed for **Smart India Hackathon (SIH 2026)**.
* Built to solve terrain, climate, and logistics challenges across North East India.
