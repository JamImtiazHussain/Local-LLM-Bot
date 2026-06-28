import streamlit as st
import requests

st.title("Local LLM Chatbot")

# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("Ask something:")

# Send button
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a question")
    else:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": user_input,
                    "stream": False   # 🔥 important fix
                }
            )

            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "No response from AI")
            else:
                answer = f"Error: {response.status_code}"

        except Exception as e:
            answer = f"Connection error: {e}"

        # Save chat
        st.session_state.history.append((user_input, answer))

# Display chat history
for q, a in st.session_state.history:
    st.write("You:", q)
    st.write("AI:", a)
    st.write("---")

# Reset button
if st.button("Reset"):
    st.session_state.history = []