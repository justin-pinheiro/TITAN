from phi.agent import Agent
from phi.model.ollama import Ollama
from tools import HevyTool
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

user_name = os.getenv("HEAVY_USER_NAME")
user_password = os.getenv("HEAVY_PASSWORD")

ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")

tool = HevyTool(user_name, user_password)

def get_agent()->Agent:
    
    return Agent(
        description="You are a hevy agent, your goal is to give access to workouts data of your owner and his friend",
        instructions= [
            "You have access to all more recents workouts from your owner, and all those he follows"
        ],
        context = {
            "owner": tool.owner,
            "current_date": datetime.now().strftime('%Y-%m-%d'),
        },
        model=Ollama(model=Ollama(id="qwen2.5:14b", host=ollama_host)),
        tools=[tool],
        markdown=True,
        show_tool_calls=False,
        debug_mode=True
    )
