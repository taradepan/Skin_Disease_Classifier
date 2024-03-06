import streamlit as st
import os
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, gemini_pro_vision_response

working_directory=os.path.dirname(os.path.abspath(__file__))

#setting the page configuration
st.set_page_config(
    page_title="Gemini AI ",
    page_icon="🧠",
    layout="centered"
)

#function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

file = None
if file == None:
    file = st.file_uploader("Choose an image")
history = []
if file is not None:
    st.image(file)
    img_res = gemini_pro_vision_response(file)
    history.append(f"User: {img_res}")

model=load_gemini_pro_model()
# model.history = history  # Set history as an attribute of the model
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=history)

st.title("🤖Chatbot")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Get user input
user_input = st.text_input("Enter your message")

# If user input is provided, use it to generate a response
if user_input:
    # Generate a response from the model
    response = model.generate_content(user_input)
    
    # Append the user input and model response to the history
    history.append(f"User: {user_input}")
    history.append(f"Model: {response}")

    # Update the chat session history
    st.session_state.chat_session.history = history

    # Display the updated chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)