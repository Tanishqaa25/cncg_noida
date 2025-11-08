import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Configure Gemini API
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in environment variables!")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Initialize the model
model = configure_gemini()

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
            # Create chat with history
            chat = model.start_chat(history=[])

            # Build context from previous messages
            context = ""
            for msg in st.session_state.messages[:-1]:
                if msg["role"] == "user":
                    context += f"User: {msg['content']}\n"
                else:
                    context += f"Assistant: {msg['content']}\n"

            # Generate response
            full_prompt = context + f"User: {user_input}\nAssistant:"
            response = chat.send_message(
                user_input,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
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
