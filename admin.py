import streamlit as st
import openai

# Load system prompt
def load_system_prompt():
    with open('data/system_prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Save system prompt
def save_system_prompt(prompt):
    with open('data/system_prompt.txt', 'w', encoding='utf-8') as file:
        file.write(prompt)

# Load welcome message
def load_welcome_message():
    with open('data/welcome_message.txt', 'r', encoding='utf-8') as file:
        return file.read()

# Save welcome message
def save_welcome_message(prompt):
    with open('data/welcome_message.txt', 'w', encoding='utf-8') as file:
        file.write(prompt)

# Streamlit app layout
st.sidebar.title("Centre d'administration")

# Edit system prompt
st.subheader("Modifier le prompt système et le message d'accueil")
system_prompt = load_system_prompt()
new_system_prompt = st.text_area("System Prompt:", system_prompt, height=300)
if st.button("Save system prompt"):
    save_system_prompt(new_system_prompt)
    st.success("System prompt saved successfully")

welcome_message = load_welcome_message()
new_welcome_message = st.text_area("Welcome message:", welcome_message, height=300)
if st.button("Save welcome message"):
    save_welcome_message(new_welcome_message)
    st.success("Welcome message saved successfully")