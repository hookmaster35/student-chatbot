import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="Student Helper Bot", page_icon="🎓")

# 2. Sidebar for API Key (Secure way)
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# 3. Main Title
st.title("Student Assistant Chatbot")
st.write("Ask me about assignments, study tips, or campus info!")

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle User Input
if prompt := st.chat_input("What's on your mind?"):
    if not api_key:
        st.info("Please add your API key in the sidebar to continue.")
        st.stop()
    
    # Configure Gemini
    genai.configure(api_key=st.secrets)
    model = genai.GenerativeModel('gemini-3-flash-preview')

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Simple context for the bot
            system_instruction = "You are a helpful university student assistant. Keep answers concise and friendly."
            response = model.generate_content(system_instruction + "\nUser: " + prompt)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})