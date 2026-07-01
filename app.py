import os
import streamlit as st
from groq import Groq

st.title("LLM Chatbot")

# ---------------- GROQ CLIENT ----------------
# GROQ_API_KEY is read from the Space's secret (set in Settings -> Variables and secrets)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

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
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": user_input}],
            )
            answer = completion.choices[0].message.content

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
