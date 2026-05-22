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

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #000428, #004e92);
    color: white;
}
/* Title */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #4ade80;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

/* Chat Message */
.stChatMessage {
    background-color: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.08);

    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;
    white-space: pre-wrap;

    line-height: 1.7;
    font-size: 16px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #000428, #004e92);
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    height: 3em;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(to right, #16a34a, #15803d);
}

/* Input */
.stChatInput input {
    border-radius: 10px;
    padding: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #9CA3AF;
    margin-top: 30px;
    font-size: 15px;
}
/* Full Webpage Background */
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
.main,
.block-container {

    background: linear-gradient(
        135deg,
        #0f0c29,
        #302b63,
        #24243e
    ) !important;

    color: white !important;
}

/* Remove Black Header */
header {
    background: transparent !important;
}

/* Remove Top Bar Black Color */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Remove Toolbar Black */
[data-testid="stToolbar"] {
    background: transparent !important;
}

/* Remove Main Section Black */
section.main {
    background: transparent !important;
}

/* Remove Bottom Black Area */
footer {
    background: transparent !important;
}

/* Remove Default Streamlit Container */
[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

/* Remove Chat Area Black */
[data-testid="ScrollToBottomContainer"] {
    background: transparent !important;
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
            "llama-3.1-8b-instant"
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
# USER INPUT36

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
                        "content": """
            You are a smart AI learning assistant.

            Always answer in this format:

            📌 Topic Overview
            - Short explanation of the topic

            🧠 Step-by-Step Explanation
            1. Step one explanation
            2. Step two explanation
            3. Step three explanation

            💻 Example
            - Give simple code examples when needed

            ✅ Final Summary
            - Short conclusion

            Rules:
            - Explain like a teacher
            - Use simple beginner-friendly language
            - Use bullet points and emojis
            - Keep answers clean and structured
            """
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
