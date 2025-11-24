import streamlit as st
from openai import OpenAI
import os

# Try to load from Streamlit secrets (for cloud)
try:
    api_key_from_config = st.secrets["OPENAI_API_KEY"]
except:
    # Fall back to .env file (for local development)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key_from_config = os.getenv("OPENAI_API_KEY")
    except:
        api_key_from_config = None

# Function to enhance the prompt
def enhance_prompt(api_key, role, context, task):
    instruction = (
        "Given the following Role, Context, and Task, generate an enhanced, structured prompt. "
        "The prompt must: "
        "1. Improve clarity and completeness. "
        "2. Request GPT to clarify assumptions before responding. "
        "3. Specify an expected output format (e.g., bullet points, JSON, structured text)."
    )

    user_input = f"Role: {role}\nContext: {context}\nTask: {task}"
    final_prompt = f"{instruction}\n\n{user_input}"

    try:
        # Initialize client with the API key
        client = OpenAI(api_key=api_key)
        
        # Create a chat completion with the updated API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": final_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
def main():
    st.title("AI Prompt Enhancer")
    st.write("Improve and structure your prompts for better AI responses.")
    
    # Sidebar for API key input
    st.sidebar.header("Settings")
    
    # Use configured key if available, otherwise ask for input
    if api_key_from_config:
        api_key = api_key_from_config
        st.sidebar.success("✅ API Key loaded automatically")
    else:
        api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
        if not api_key:
            st.sidebar.warning("⚠️ Please enter your API key")
    
    role = st.text_input("Role", placeholder="e.g., You are a helpful assistant")
    context = st.text_area("Context", placeholder="e.g., The user needs help with...")
    task = st.text_area("Task", placeholder="e.g., Create a summary of...")

    if st.button("Enhance Prompt"):
        if not api_key:
            st.warning("Please enter your OpenAI API key in the sidebar.")
        elif role and context and task:
            with st.spinner("Enhancing your prompt..."):
                enhanced_prompt = enhance_prompt(api_key, role, context, task)
            
            if enhanced_prompt.startswith("Error:"):
                st.error(enhanced_prompt)
            else:
                st.subheader("Enhanced Prompt:")
                st.code(enhanced_prompt, language="markdown")
        else:
            st.warning("Please fill in all fields before generating.")

if __name__ == "__main__":
    main()