import streamlit as st
from openai import OpenAI
import base64
import os
import datetime
from io import BytesIO
from PIL import Image
from location_weather import get_location_and_weather, get_weather
from streamlit_js_eval import get_geolocation
from datetime import datetime
import json
import folium
from streamlit_folium import folium_static

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



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country, e.g. San Francisco, US",
                    },
                },
                "required": ["location"],
            },
        }
    }]

if "latitude" not in st.session_state:
    locat()

else:

    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=st.secrets['openai_key'])

    if "location" not in st.session_state:
        st.session_state.weather, st.session_state.location = get_location_and_weather(st.session_state.latitude, st.session_state.longitude, st.session_state.client)

    if "messages" not in st.session_state:


        system_message = f'''
        You are a travel companion bot, you name is (Enten Nishiki) that takes in user input in audio format and answer in audio as well

        Your default language is english, user might ask questions in any other language, reply in english

        Until the user asks you to work as a interpreter then start transalting language to both ways ex: if the user asks you to be an interpreter for hindi to english then after that 
        translate any hindi input to english and any english input to hindi, ask user for the both the languagaes to interpret if not provided
        Only provide translated text and nothing else, Keep interpreting until the user asks you to stop translating

        The user is in {st.session_state.location} with {st.session_state.weather} weather, and date {datetime.now()},the user can be traveling in this city or to some other place, make sure you confirm this.
        And start the conversation with greeting the user, introducing yourself, tell the user in which city we are in asking the user if we are travelling to any other city or travelling the city the user is in to confirm the travelling location
        
        Once the travelling location is confirmed, Start the converstaion with confirming where we are travelling, get the weather of that location, make recommendations appropriate for that weather 
        ask user if they would like to know about Shopping Places, Tourist Attraction, Upcoming events, etc.
        
        '''


        stream = st.session_state.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}])


        st.session_state["messages"] = \
        [{"role": "system", "content": system_message},
        {"role": "assistant", "content": stream.choices[0].message.content}]

    st.sidebar.title(st.session_state.location)
    st.sidebar.image("https://openweathermap.org/img/wn/" + st.session_state.weather["weather"][0]["icon"] + "@2x.png")
    location = (st.session_state.latitude, st.session_state.longitude)
    m = folium.Map(location=location, zoom_start=13)
    folium.Marker(location, popup="Your Location").add_to(m)
    with st.sidebar:
        folium_static(m)

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

    if "first_message" not in st.session_state:
        st.session_state.first_message = stream.choices[0].message.content
        response = st.session_state.client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=stream.choices[0].message.content
        )
        st.audio(response.content, autoplay=True)


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
            messages=st.session_state.messages,
            tools= tools, 
        tool_choice="auto",
        )


        tool_calls = stream.choices[0].message.tool_calls

        if tool_calls:
            tool_call_id = tool_calls[0].id
            tool_function_name = tool_calls[0].function.name
            arguments = json.loads(tool_calls[0].function.arguments)

            if tool_function_name == 'get_weather':
                results = get_weather(arguments['location'])
                raw_data_prompt = f"""
                    Here is the raw weather data for {results}
                    
                    Please format this message as response for chatbot with user prompt {prompt}
                    """
                st.session_state.messages.append({"role": "system", "content": raw_data_prompt})
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