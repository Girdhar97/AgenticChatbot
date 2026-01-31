# GroqLLM class is responsible for initializing the ChatGroq model using the API key and model name provided by the user 
# through the Streamlit UI. It checks for the presence of the API key and raises an error if it's missing. 
# The get_llm_model method returns an instance of the ChatGroq model that can be used for generating responses in the 
# chatbot application.

# This file loads the Groq LLM model based on user input from the Streamlit UI.

import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_contols_input):
        self.user_controls_input=user_contols_input

    def get_llm_model(self):
        try:
            groq_api_key=self.user_controls_input["GROQ_API_KEY"]
            selected_groq_model=self.user_controls_input["selected_groq_model"]
            if groq_api_key=='' and os.environ["GROQ_API_KEY"] =='':
                st.error("Please Enter the Groq API KEY")

            llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error Ocuured With Exception : {e}")
        return llm