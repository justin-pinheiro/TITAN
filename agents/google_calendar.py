from tools.googlecalendar import GoogleCalendarTools
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.workflow import Workflow, RunResponse, RunEvent
from datetime import datetime
import os
from dotenv import load_dotenv
from tzlocal import get_localzone_name

load_dotenv()

google_api_credentials_path = os.getenv("GOOGLE_API_CREDENTIALS_PATH")
ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")

print(google_api_credentials_path)

def get_agent()->Agent:
    return Agent(
        model=Ollama(id="qwen2.5:14b", host=ollama_host),
        tools=[GoogleCalendarTools(credentials_path=google_api_credentials_path)],
        description=
            f"""
            You are a scheduling assistant in charge of helping users with calendar related tasks. 
            """,
        task=
            f"""
            You will help users perform actions in their Google calendar:
                - get their scheduled events based on request
                - create new events based on provided details
            """,
        guidelines=[
            f"""
            When users ask something, always check their calendar events before replying.
            """],
        additional_context=
            f"""
            The users timezone is {get_localzone_name()}.
            Today's date is {datetime.now()}.
            Today's day is {datetime.today().strftime('%A')}.
            """,
        prevent_prompt_leakage=True,
        prevent_hallucinations=True,
        debug_mode=True
    )
