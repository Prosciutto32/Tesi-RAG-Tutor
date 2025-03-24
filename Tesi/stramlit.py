import streamlit as st
from query_data import query_rag 
st.title("TUTORIAL - un TUTOR basato su Intelligienza ArtificiaLe")



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("fai la tua domanda"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    risposta = query_rag(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(risposta)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": risposta})



 #chiama query_data con il prompt
 # to do: fare un metodo che prende un PDF lo carica nel folder "data" e chiama populate_database per aggiornarlo
  #una volta finito manda mail ai professori che ci sei