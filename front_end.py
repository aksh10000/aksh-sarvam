import streamlit as st
import requests
import json
import base64
from dotenv import load_dotenv
import os

load_dotenv()
sarvam_api = os.getenv("SARVAM_API_KEY")
def get_audio(text):
    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [text[:500]],
        "target_language_code": "en-IN",
        "speaker": "meera",
        "pitch": 1,
        "pace": 1,
        "loudness": 1,
        "speech_sample_rate": 16000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    headers = {
        "api-subscription-key": sarvam_api,
        "Content-Type": "application/json"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    
    print(response.text)
    # Assume 'response' contains the JSON string from the API
    response_data = json.loads(response.text)
    # Get the Base64 encoded audio data
    # st.warning(response_data)
    # print(response_data)
    audio_base64 = response_data['audios'][0]
    # Decode the Base64 string
    audio_data = base64.b64decode(audio_base64)
    # Write the binary audio data to a WAV file
    file_name = 'output.wav'
    with open(file_name, 'wb') as audio_file:
        audio_file.write(audio_data)
    return file_name

def main():
    st.set_page_config(page_title="AI CHAT AGENT")
    st.header("Agentic router with tool-calling support and RAG")
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    
    if st.session_state.session_id:
        user_input = st.chat_input("User query")
        if user_input:
            # The URL of the API endpoint
            url = "http://127.0.0.1:8001/"

            # Send a POST request
            response = requests.post(url, json={"query": user_input, "session_id": st.session_state.session_id})

            # Check if the request was successful
            if response.status_code == 200:
                # Request was successful
                data = response.json()  # If the response is in JSON format
                api_response = data['response']
            else:
                # Request failed
                api_response = f"Request failed with status code: {response.status_code}"

            st.markdown(f"**User**: {user_input}")
            st.markdown(f"**Assistant**: {api_response}")
            file_name = get_audio(api_response)
            audio_file = open(file_name, 'rb')
            st.audio(audio_file)

            

            
    else:
        session_id = st.text_input("Enter your session id")
        if session_id:
            st.session_state.session_id = session_id
            st.rerun()

if __name__ == '__main__':
    main()
