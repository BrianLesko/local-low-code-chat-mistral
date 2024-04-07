# Brian Lesko 
# 4/6/2024
# Use streamlit GUI to interact with Mistral 7B model running in a container

import streamlit as st
import customize_gui
import ollamaInterface
import textwrap
import ollama
from ollama import Client
import time
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

def setup_session_state():
    if "client" not in st.session_state:
        st.session_state.my_ollama = ollamaInterface.ollamaInterface()
        message = st.session_state.my_ollama.start_container()
        st.write(message)
        st.session_state.client = Client(host='http://localhost:11434')
        st.session_state.my_ollama.start()
        st.session_state.messages = []

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            col1, col2, col3 = st.columns([1,69,1])
            with col2:
                st.caption("You" if message['role'] == 'user' else "Mistral 7B")
                st.write(message['content'])
                if 'num_tokens' in message and message['role'] == 'user':
                    st.caption(f"Number of tokens: {message['num_tokens']}")
                if 'response_time' in message and message['role'] == 'assistant':
                    st.caption(f"Response time: {message['response_time']:.1f}s")

def process_stream(stream, begin_time, Time, placeholder):
    text = ""
    times = []
    for chunk in stream:
        with Time: 
            times.append(time.time()-begin_time)
            st.caption(f"Time: {times[-1]:.1f}s")
        text += chunk['message']['content']
        wrapped_text = textwrap.fill(text, width=80)
        placeholder.markdown(f'<p style="font-size:16px">{wrapped_text}</p>', unsafe_allow_html=True)
        if 'assistant' in st.session_state.messages[-1]['role']:
            st.session_state.messages[-1] = {
                'role': 'assistant', 
                'content': wrapped_text, 
                'response_time': times[-1]
            }
        else:
            st.session_state.messages.append({
                'role': 'assistant', 
                'content': wrapped_text, 
                'response_time': times[-1]
            })

def main():
    gui = customize_gui.gui()
    gui.setup(wide=True,text=" Query a local LLM running in a container, no data is shared to the internet")

    setup_session_state()

    st.title('Local AI Chat with Mistral 7b')
    st.write(" ")
    "---"
    st.write(" ")

    display_messages()

    Time = st.empty()
    content = st.chat_input("Write a message")
    if content: 
        num_tokens = len(tokenizer(content)['input_ids'])
        start_time = time.time()
        with st.chat_message("user"): 
            col1, col2, col3 = st.columns([1,69,1])
            with col2:
                st.session_state.messages.append({'role': 'user', 'content': content, 'num_tokens': len(tokenizer(content)['input_ids']), 'response_time': time.time() - start_time})
                st.caption(" You")
                st.write(content)
                st.caption(f"Number of tokens: {num_tokens}")
        with st.chat_message("assistant"):
            with st.spinner("Querying the model"):
                begin_time = time.time()
                stream = ollama.chat(model='mistral',messages=[{'role': 'user', 'content': content}],stream=True,)
                col1, col2, col3 = st.columns([1,69,1])
                with col2:
                    st.caption(f"Mistral 7B")
                    placeholder = st.empty()
                    Time = st.empty()

            process_stream(stream, begin_time, Time, placeholder)

main()