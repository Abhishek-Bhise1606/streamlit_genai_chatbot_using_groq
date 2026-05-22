import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Generative AI ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

/* Headers */
h1, h2, h3, h4, h5, h6, p {
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Chat Message Styling */
.stChatMessage {
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
    background-color: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
}

/* User Message */
[data-testid="chatAvatarIcon-user"] {
    background-color: #2563eb;
}

/* Assistant Message */
[data-testid="chatAvatarIcon-assistant"] {
    background-color: #06b6d4;
}

/* Chat Input */
.stChatInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(to right, #06b6d4, #3b82f6);
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #0891b2, #2563eb);
}

/* Select Box */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b;
    border-radius: 10px;
    color: white;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("---")

    st.subheader("⚙️ Settings")

    # Model Selection
    selected_model = st.selectbox(
        "Choose AI Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ]
    )

    # Temperature Slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1
    )

    st.markdown("---")

    st.subheader("✨ Features")
    st.write("✅ Chat Memory")
    st.write("✅ Streaming Response")
    st.write("✅ Multiple AI Models")
    st.write("✅ Modern UI")
    st.write("✅ Fast Responses")

    st.markdown("---")

    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ==============================
# MAIN HEADER
# ==============================
st.markdown(
    """
    <h1 style='text-align:center;'>
        ✨ Generative AI ChatBot
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; font-size:18px;'>
        Powered by Groq + LangChain 🚀
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==============================
# DISPLAY OLD CHAT
# ==============================
for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================
# INITIALIZE LLM
# ==============================
llm = ChatGroq(
    model=selected_model,
    temperature=temperature
)

# ==============================
# USER INPUT
# ==============================
user_prompt = st.chat_input("💬 Ask anything...")

# ==============================
# CHATBOT LOGIC
# ==============================
if user_prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save User Message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    # Assistant Message Container
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        # Streaming Response
        with st.spinner("🤖 Thinking..."):

            stream = llm.stream(
                [
                    {
                        "role": "system",
                        "content": "You are a smart and helpful AI assistant."
                    },
                    *st.session_state.chat_history
                ]
            )

            for chunk in stream:

                if chunk.content:
                    full_response += chunk.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

    # Save Assistant Response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response
    })

# ==============================
# FOOTER
# ==============================
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:lightgray;'>
        Made with ❤️ using Streamlit + LangChain + Groq
    </div>
    """,
    unsafe_allow_html=True
)
