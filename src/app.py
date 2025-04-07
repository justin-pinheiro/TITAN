import streamlit as st
from agents import hevy

agent_constructors = {
    "Hevy": hevy.get_agent,
}

@st.cache_resource
def get_agent(agent_name):
    return agent_constructors[agent_name]()
    

st.title("TITAN")

selected_agent_name = st.sidebar.selectbox("Select an agent:", list(agent_constructors.keys()))

# This will only initialize once per agent selection
agent = get_agent(selected_agent_name)

user_input = st.text_input("Enter a request:")

if user_input:
    response = agent.run(user_input)
    st.write(response.content)