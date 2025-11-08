import streamlit as st
from google import genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
def get_gemini_client():
    """Get or initialize the Gemini client"""
    if 'client' not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY not found in environment variables!")
            st.info("Please set the GEMINI_API_KEY environment variable with your API key from https://makersuite.google.com/app/apikey")
            st.stop()
        try:
            st.session_state.client = genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"Failed to initialize Gemini API: {str(e)}")
            st.stop()
    return st.session_state.client

# Page configuration
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and description
st.title("🤖 Gemini Chatbot")
st.markdown("### Powered by Google Gemini AI")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("This is a simple chatbot powered by Google's Gemini API. Ask me anything!")

    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 100, 2000, 1000, 100)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{message["content"]}</div>',
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>Gemini:</strong><br>{message["content"]}</div>',
                       unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.container():
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{user_input}</div>',
                   unsafe_allow_html=True)

    # Generate response
    with st.spinner("Thinking..."):
        try:
            # Get the client
            client = get_gemini_client()

            # Build context from chat history
            context = ""
            for msg in st.session_state.messages[:-1]:
                if msg["role"] == "user":
                    context += f"User: {msg['content']}\n"
                else:
                    context += f"Assistant: {msg['content']}\n"

            # Build full prompt with context
            full_prompt = context + f"User: {user_input}\nAssistant:"

            # Generate response using new API
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=full_prompt
            )

            bot_response = response.text

            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

            # Display bot response
            with st.container():
                st.markdown(f'<div class="chat-message bot-message"><strong>Gemini:</strong><br>{bot_response}</div>',
                           unsafe_allow_html=True)

            st.rerun()

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Footer
st.markdown("---")
st.caption("Built with Streamlit and Google Gemini API")
