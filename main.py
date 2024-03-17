import streamlit as st
import google.generativeai as genai
import os
import dotenv
from chat import process_img, generate_response, init_prompt
dotenv.load_dotenv()

st.title("Skin Desease AI")

picture = st.camera_input("Take a picture")

if picture:
    with open('image.jpg', 'wb') as f:
        f.write(picture.read())
        f.flush()
        os.fsync(f.fileno())
    picture.seek(0)

    desease = process_img()

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": init_prompt(desease)}]

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    if prompt := st.chat_input(placeholder="Type a message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)


    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for text in response:
                    full_response += text
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)