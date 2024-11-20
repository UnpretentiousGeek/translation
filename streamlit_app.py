import streamlit as st
from openai import OpenAI


client = OpenAI(api_key=st.secrets["openai_key"])
audio_value = st.audio_input("Record a voice message")

if audio_value:

    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_value
    )
    st.write(transcription.text)