import streamlit as st
from openai import OpenAI
import base64
import os
import datetime
from io import BytesIO
from PIL import Image
from location_weather import get_location_and_weather
from streamlit_js_eval import get_geolocation

@st.dialog("Get Location")
def locat():
    if st.checkbox("Get my location"):
        get_coords()


@st.dialog("Take a Photo")
def cam():
    
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    preprocess(picture)

@st.dialog("upload a file")
def upl():
    uploaded_file = st.file_uploader("Upload a photo", type=("jpg", "png"))
    preprocess(uploaded_file)

def get_coords():
    loc = get_geolocation()
    if loc:
        st.session_state.latitude = loc['coords']['latitude']
        st.session_state.longitude = loc['coords']['longitude']
        st.rerun()


def preprocess(picture):

    if picture:
        st.session_state.show_img = picture
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"image_{timestamp}.png"

        with open(file_path, "wb") as file:
            file.write(picture.getbuffer())

        with open(file_path, "rb") as image_file:
             st.session_state.img = base64.b64encode(image_file.read()).decode('utf-8')
        
        st.rerun()

def weather_location():
    get_location_and_weather(st.session_state.latitude, st.session_state.longitude)

if "latitude" not in st.session_state:
    locat()

else:

    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

    if "location" not in st.session_state:
        st.session_state.weather, st.session_state.location = get_location_and_weather(st.session_state.latitude, st.session_state.longitude, st.session_state.client, st.secrets['weather_key'])

    if "messages" not in st.session_state:


        system_message = '''
        You are a travel companion bot that takes in user input in audio format and answer in audio as well

        Your default language is english, but if the user asks question in another language answer in that language only 

        If the user asks you to work as a interpreter the start translating 

        Stop being the interpretr when the user asks you to stop translating
        '''
        st.session_state["messages"] = \
        [{"role": "system", "content": system_message},
        {"role": "assistant", "content": "How can I help you?"}]

    st.sidebar.header(st.session_state.location)

    if st.sidebar.button("Camera 📷"):
        cam()

    if st.sidebar.button("Upload files ⬆️"):
        upl()

    if "show_img" in st.session_state:
        st.sidebar.image(st.session_state.show_img)
        if st.sidebar.button("Clear ❌"):
            del st.session_state["img"]
            del st.session_state["show_img"]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            if isinstance(msg["content"], list) and len(msg["content"]) > 1:
                if msg["content"][1].get("type") == "image_url":
                    col1, col2 = st.columns([1, 3])
                    img_data = base64.b64decode(msg["content"][1]["image_url"]["url"].split(",")[1])
                    col1.image(img_data)
                    chat_msg = st.chat_message(msg["role"]) 
                    chat_msg.write(msg["content"][0].get("text"))
            else:
                chat_msg = st.chat_message(msg["role"]) 
                chat_msg.write(msg["content"])

    if audio_value :=  st.audio_input("What is up?"):
        st.session_state.audio_value = audio_value


    if "last_audio" not in st.session_state:
        st.session_state.last_audio = True

    if audio_value and st.session_state.last_audio != st.session_state.audio_value:
        
        st.session_state.last_audio = audio_value

        prompt = st.session_state.client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_value,
        response_format="text"
        )

        if "img" in st.session_state:
            col1, col2 = st.columns([1, 3])
            img_data = base64.b64decode(st.session_state.img)
            col1.image(img_data)
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content":[
            {"type": "text", "text": prompt},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{st.session_state.img}",
            },
            },
        ]})
            del st.session_state["img"]
            del st.session_state["show_img"]
            

        else:
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
        st.session_state.messages.append({"role": "assistant", "content": stream.choices[0].message.content})
        del st.session_state["audio_value"]