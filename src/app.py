import os
import streamlit as st
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo

st.title("Ollama Chat with Streamlit")
user_input = st.text_input("Say something to Ollama:")

if user_input:
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    agent = Agent(
        name="Web Agent",
        model=Ollama(id="llama3.1:8b", host=ollama_host),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    response = agent.run(user_input)
    
    st.write("Ollama's response:")
    st.write(response.content)
