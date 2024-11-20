import streamlit as st
from openai import OpenAI

system_message = '''
You are bot that will answer questions in the same language in which the question is asked

If the user asks you to do translations work as a interpreter 

'''

if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

if "messages" not in st.session_state:
    st.session_state["messages"] = \
    [{"role": "system", "content": system_message},
     {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] != "system":    
        chat_msg = st.chat_message(msg["role"])
        chat_msg.write(msg["content"])

if audio_value := st.audio_input("What is up?"):
    prompt = st.session_state.client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_value,
    response_format="text"
    )
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    stream = st.session_state.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    response = st.session_state.client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=stream.choices[0].message.content
    )

    with st.chat_message("assistant"):
        reply = st.write(stream.choices[0].message.content)

    st.audio(response.content, autoplay=True)
    st.write(stream.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": reply})