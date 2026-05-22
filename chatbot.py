import streamlit as st
from langchain_ollama import OllamaLLM

# Page configuration
st.set_page_config(
    page_title="Learning Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    model_name = st.selectbox(
        "Choose Model",
        ["gemma2:2b","llama-3.1-8b-instant", "mistral"]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main title
st.title("🤖 Learning AI Chatbot")

st.markdown("Ask anything about Python, AI, ML, or Coding.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display old chats
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Type your question here...")

# Process input
if user_prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Load model
    llm = OllamaLLM(
        model=model_name,
        temperature=temperature
    )

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = llm.invoke(user_prompt)

            st.markdown(response)

    # Save assistant response
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": response
        }
    )