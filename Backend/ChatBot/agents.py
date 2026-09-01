from crewai import Agent,from crewai import LLM

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

Orchestrator= Agent(
  role='Senior Algorithmic Fairness Auditor & Strategist',
  goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)

Weather_Risk_Agent= Agent(
  role='Senior Algorithmic Fairness Auditor & Strategist',
  goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)


Accessibility_Agent = Agent(
  role='Senior Algorithmic Fairness Auditor & Strategist',
  goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)

Route_Agent= Agent(
  role='Senior Algorithmic Fairness Auditor & Strategist',
  goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)

Alert_Agent = Agent(
    role='Senior Algorithmic Fairness Auditor & Strategist',
    goal='Detect bias, explain its impact, and suggest mitigation strategies in a single unified analysis.',
  llm=primary_llm,
  backstory="""You are a world-class AI Ethics consultant with 20 years of experience. You combine 
  the skills of a data scientist (detecting bias), a communicator (explaining it clearly), and 
  a legal strategist (suggesting fixes). You strictly analyze only the provided data and never 
  hallucinate information or sectors not present in the source.""" ,
  tools=[],
  max_rpm=15,
  max_iter=3,
  **DEFAULT_SETTINGS
)

