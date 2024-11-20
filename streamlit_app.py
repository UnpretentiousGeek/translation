import streamlit as st
from openai import OpenAI


if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

audio_value = st.audio_input("Record a voice message")

if audio_value:
    translation = st.session_state.client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_value,
    response_format="text"
    )
    st.write(translation.text)




