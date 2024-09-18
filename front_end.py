import streamlit as st
import requests

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
    else:
        session_id = st.text_input("Enter your session id")
        if session_id:
            st.session_state.session_id = session_id
            st.rerun()

if __name__ == '__main__':
    main()