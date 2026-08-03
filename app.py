import streamlit as st
import os
from agents.agents_graph import run_food_advisor

# Configure Streamlit page
st.set_page_config(
    page_title="Sri Lankan Food Advisor",
    page_icon="🍛",
    layout="wide"
)

# --- Main App ---
st.title("Sri Lankan Food Advisor 🍛")
st.markdown("Welcome! I can help you find the perfect Sri Lankan food based on your taste preferences. Just tell me if you want something spicy, sweet, or ask a general question about Sri Lankan cuisine!")

st.header("Culinary Chat")
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Tell me what you are craving (e.g., 'I want a spicy dish with chicken' or 'recommend a sweet dessert')..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant thinking...
    with st.chat_message("assistant"):
        with st.spinner("Our culinary agents are thinking (Routing -> Searching Recipes -> Critic Review)..."):
            try:
                response = run_food_advisor(prompt)
                st.markdown(response)
                # Add assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Agent Orchestration Error: {str(e)}")
