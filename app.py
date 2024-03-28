import streamlit as st
import customize_gui
gui = customize_gui.gui()
import ollamaInterface
import textwrap
import ollama
from ollama import Client

def main():
    gui.setup(wide=True,text=" Query a local LLM running in a container, no data is shared to the internet")

    # Start the container
    if "client" not in st.session_state:
        st.session_state.my_ollama = ollamaInterface.ollamaInterface()
        message = st.session_state.my_ollama.start_container()
        st.write(message)
        st.session_state.client = Client(host='http://localhost:11434')
        st.session_state.my_ollama.start()
        
    st.title('Local AI Chat with Mistral 7b')
    st.write(" ")
    "---"
    st.write(" ")
    
    # Display the existing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for role, message in st.session_state.messages:
        with st.chat_message(role):
            col1, col2, col3 = st.columns([1,69,.1])
            with col2:
                if role == 'user':
                    st.caption("You")
                else:
                    st.caption("Mistral 7B")
                st.write(message)
        
    content = st.chat_input("Write a message")

    if content: 
        with st.chat_message("user"): 
            col1, col2, col3 = st.columns([1,69,1])
            with col2:
                st.session_state.messages.append(('user', content))
                st.caption(" You")
                st.write(content)
        with st.spinner("Querying the model"):
            stream = ollama.chat(model='mistral',messages=[{'role': 'user', 'content': content}],stream=True,)

        with st.chat_message("assistant"):
            col1, col2, col3 = st.columns([1,69,1])
            with col2:
                st.caption("Mistral 7B")
                placeholder = st.empty()
            text = ""
            for chunk in stream:
                text += chunk['message']['content']
                wrapped_text = textwrap.fill(text, width=80)
                placeholder.markdown(f'<p style="font-size:16px">{wrapped_text}</p>', unsafe_allow_html=True)
                # Update the session state with the current message
                if 'assistant' in st.session_state.messages[-1]:
                    st.session_state.messages[-1] = ('assistant', wrapped_text)
                else:
                    st.session_state.messages.append(('assistant', wrapped_text))
main()

#if st.button("embeddings"):
#    with st.spinner("embedding"):
#       st.write(ollama.embeddings(model='mistral', prompt='They sky is blue because of rayleigh scattering'))