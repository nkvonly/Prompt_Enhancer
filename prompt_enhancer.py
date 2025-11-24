import streamlit as st
from openai import OpenAI

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
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    role = st.text_input("Role", "")
    context = st.text_area("Context", "")
    task = st.text_area("Task", "")

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