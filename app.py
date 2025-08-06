import streamlit as st
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
import re
import spacy
from googletrans import Translator
import time
from model.pest_detector import diagnose_plant_disease

# --- 1. SETUP & CACHED FUNCTIONS ---

st.set_page_config(page_title="KrishiMitra", page_icon="🌿", layout="centered")

@st.cache_resource
def load_spacy_model():
    """Loads the spaCy model and caches it."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("SpaCy model not found. Please run 'python -m spacy download en_core_web_sm'.")
        return None

@st.cache_data
def get_indian_cities():
    """Loads a list of Indian cities from a JSON file."""
    try:
        with open('static/data.json', 'r') as f:
            return [city.lower() for city in json.load(f)]
    except Exception as e:
        st.error(f"Error loading cities file: {e}")
        return []

nlp = load_spacy_model()
INDIAN_CITIES = get_indian_cities()
translator = Translator()

# --- 2. AGENT FUNCTIONS ---

# Your excellent get_market_price and get_weather_forecast functions go here.
# They are correct and don't need changes.
# I've omitted them for brevity, but they should be in your final file.

def extract_location(text):
    if not nlp: return "indore"
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE" and ent.text.lower() in INDIAN_CITIES:
            return ent.text.lower()
    return "indore"

def route_query(prompt, lang='en'):
    query = prompt.lower()
    location = extract_location(query)
    
    keywords = {
        "price": ["price", "rate", "cost", "mandi", "भाव", "दाम", "कीमत", "मंडी"],
        "weather": ["weather", "forecast", "temperature", "मौसम", "तापमान"],
        "disease": ["disease", "sick", "pest", "leaf", "plant", "infection", "ill", "बीमारी", "रोग", "पत्ती", "बीमार"]
    }

    if any(k in query for k in keywords["price"]):
        return get_market_price(query, location, lang)
    elif any(k in query for k in keywords["weather"]):
        return get_weather_forecast(location, lang)
    elif any(k in query for k in keywords["disease"]):
        st.session_state.show_uploader = True
        return "It sounds like you have a sick plant. Please upload a photo of the affected leaf below." if lang == 'en' else "लगता है आपके पौधे में कोई बीमारी है। कृपया नीचे प्रभावित पत्ती की तस्वीर अपलोड करें।"
    else:
        return "I'm sorry, I can only help with market prices, weather, and plant diseases." if lang == 'en' else "माफ़ कीजिए, मैं केवल बाजार भाव, मौसम, और पौधों की बीमारियों में मदद कर सकता हूँ।"

# --- 3. STREAMLIT APP LOGIC & UI ---

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "en"
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

# UI: Sidebar
with st.sidebar:
    st.title("🌿 KrishiMitra")
    # ... (Your sidebar content) ...

# UI: Header and Language Selector
st.title("🤖 KrishiMitra Assistant")
lang_choice = st.radio("Language", ["English", "हिंदी"], horizontal=True)
st.session_state.language = "hi" if lang_choice == "हिंदी" else "en"
lang = st.session_state.language

# --- Main Interaction Logic ---
def handle_prompt(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = route_query(prompt, lang)
    st.session_state.messages.append({"role": "assistant", "content": response})

# UI: Display initial cards if chat is empty
if not st.session_state.messages:
    # ... (Your card layout code is great and goes here) ...
    if st.button("🐛 " + ("Detect Crop Disease" if lang == 'en' else "फसल रोग का पता लगाएं")):
        handle_prompt("Detect Crop Disease")
        st.rerun()

# --- Display Chat History ---
# We store messages in one language and translate for display
for msg in st.session_state.messages:
    avatar = "🧑‍🌾" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        content = msg["content"]
        if lang == 'hi' and msg["role"] == 'assistant':
             # Simple check to avoid re-translating already-Hindi text
            if re.search("[\u0900-\u097F]+", content):
                 st.markdown(content)
            else:
                 st.markdown(translator.translate(content, dest='hi').text)
        else:
            st.markdown(content)

# --- Conditional File Uploader ---
if st.session_state.show_uploader:
    uploaded_file = st.file_uploader("Choose a plant leaf image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.messages.append({"role": "user", "content": "[Image Uploaded]"})
        diagnosis = diagnose_plant_disease("temp_image.jpg")
        st.session_state.messages.append({"role": "assistant", "content": diagnosis})
        
        st.session_state.show_uploader = False
        st.rerun()

# UI: Chat Input
if prompt := st.chat_input("Ask me anything..."):
    handle_prompt(prompt)
    st.rerun()
