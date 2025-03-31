import streamlit as st
from agents import google_calendar

st.title("TITAN")

# Sidebar to select an agent
agent_list = {
    "Google Calendar": google_calendar.get_agent,
}

selected_agent_name = st.sidebar.selectbox("Select an agent:", list(agent_list.keys()))

user_input = st.text_input("Enter a request:")

if user_input:
    agent = agent_list[selected_agent_name]()
    response = agent.run(user_input)
    
    st.write(response.content)
