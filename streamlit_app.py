import streamlit as st
from openai import OpenAI


client = OpenAI(api_key=st.secrets['openai_key'])
if st.button("hi"):
        response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
    )
        st.audio(response['audio'])