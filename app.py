# app.py - KrishiMitra (Bilingual Version)
import requests
from dotenv import load_dotenv
import os
import json
import re
import streamlit as st
import spacy
from googletrans import Translator
import time
# --- IMPORT THE REAL DIAGNOSIS FUNCTION ---
from model.pest_detector import diagnose_plant_disease

# --- 1. TEXT & LOCALIZATION ---
TEXT = {
    # ... (all your text content remains the same) ...
    "page_title": {"en": "KrishiMitra", "hi": "कृषि मित्र"},
    "page_icon": "🌿",
    "sidebar_title": {"en": "🌿 KrishiMitra", "hi": "🌿 कृषि मित्र"},
    "sidebar_welcome": {"en": "Welcome to KrishiMitra, your AI-powered farming assistant.", "hi": "कृषि मित्र में आपका स्वागत है, यह आपका AI-संचालित खेती सहायक है।"},
    "sidebar_what_i_do": {"en": "**What can I do?**", "hi": "**मैं क्या कर सकता हूँ?**"},
    "sidebar_feature_1": {"en": "- 📈 Provide current market prices.", "hi": "- 📈 फसलों के बाजार भाव प्रदान करना।"},
    "sidebar_feature_2": {"en": "- 🌦️ Give you a weather forecast.", "hi": "- 🌦️ मौसम का पूर्वानुमान देना।"},
    "sidebar_feature_3": {"en": "- 🔬 Diagnose plant diseases from a photo.", "hi": "- 🔬 तस्वीर से पौधों की बीमारियों का पता लगाना।"},
    "app_title": {"en": "🤖 KrishiMitra Assistant", "hi": "🤖 कृषि मित्र सहायक"},
    "app_intro": {"en": "Ask me about crop prices, weather, or upload a photo of a sick plant!", "hi": "मुझसे फसल की कीमतों, मौसम के बारे में पूछें, या किसी बीमार पौधे की तस्वीर अपलोड करें!"},
    "welcome_message": {"en": "Hello, farmer! How can I help you today?", "hi": "नमस्ते किसान! मैं आपकी कैसे मदद कर सकता हूँ?"},
    "chat_placeholder": {"en": "What do you need help with?", "hi": "आप क्या मदद चाहते हैं?"},
    "spinner_thinking": {"en": "Thinking...", "hi": "सोच रहा हूँ..."},
    "spinner_analyzing": {"en": "Analyzing the image...", "hi": "तस्वीर का विश्लेषण हो रहा है..."},
    "upload_prompt": {"en": "Choose a plant leaf image...", "hi": "पौधे की पत्ती की एक तस्वीर चुनें..."},
    "upload_caption": {"en": "Uploaded Image.", "hi": "अपलोड की गई तस्वीर।"},
    "trigger_disease": {"en": "It sounds like you have a sick plant. **Please upload a photo of the affected leaf below.**", "hi": "लगता है आपके पौधे में कोई बीमारी है। **कृपया नीचे प्रभावित पत्ती की तस्वीर अपलोड करें।**"},
    "trigger_upload_check": {"en": "upload a photo", "hi": "तस्वीर अपलोड करें"},
    "post_diagnosis_message": {"en": "Here is the diagnosis for your plant.", "hi": "आपके पौधे की जांच की रिपोर्ट यहाँ है।"},
    "fallback_message": {"en": "I'm sorry, I can only help with market prices, weather, and plant diseases. Please try asking one of those.", "hi": "माफ़ कीजिए, मैं केवल बाजार भाव, मौसम, और पौधों की बीमारियों में मदद कर सकता हूँ। कृपया इनमें से कोई एक प्रश्न पूछें।"}
}

# Translation function
def simple_translate_to_hindi(text_to_translate):
    translator = Translator()
    translation = translator.translate(text_to_translate, dest='hi')
    return translation.text

# --- 2. BILINGUAL AGENT FUNCTIONS ---

def get_market_price(crop_name, lang='en'):
    # ... (this function remains the same) ...
    prices = {
        "soybean": {"en": "The current market price for Soybean in Indore is ₹4,500 per quintal.", "hi": "इंदौर में सोयाबीन का मौजूदा बाजार भाव ₹4,500 प्रति क्विंटल है।"},
        "wheat": {"en": "The current market price for Wheat in Dewas is ₹2,100 per quintal.", "hi": "देवास में गेहूं का मौजूदा बाजार भाव ₹2,100 प्रति क्विंटल है।"}
    }
    fallback = {"en": f"Sorry, I don't have the price for {crop_name}. I only have data for Soybean and Wheat.", "hi": f"माफ़ कीजिए, मेरे पास {crop_name} का भाव नहीं है। मेरे पास केवल सोयाबीन और गेहूं की जानकारी है।"}
    
    if "soybean" in crop_name.lower() or "सोयाबीन" in crop_name.lower():
        return prices["soybean"][lang]
    elif "wheat" in crop_name.lower() or "गेहूं" in crop_name.lower():
        return prices["wheat"][lang]
    else:
        return fallback[lang]
nlp = spacy.load("en_core_web_sm")
json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data.json')
INDIAN_CITIES = []
try:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            # Store a list of lowercase city names for easy matching
            INDIAN_CITIES = [city.lower() for city in data]
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"Error loading cities file: {e}")
def extract_location(text):
    words = re.findall(r'\w+', text.lower())
    for city in INDIAN_CITIES:
        for word in words:
            if word == city:
                return city
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None
def get_weather_forecast(location, lang='en'):
    load_dotenv()
    """Returns weather forecast in the selected language."""

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found. Please set it in the .env file."
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    completeUrl = f"{base_url}q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(completeUrl)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            weatherDescription = data['weather'][0]['description']
            hindidescription = simple_translate_to_hindi(weatherDescription)
            humidity = data['main']['humidity']
            if "rain" in weatherDescription:
                # Use a more natural phrase for rain
                localized_description_en = "chance of light rain in the evening"
                localized_description_hi = "शाम को हल्की बारिश की संभावना है।"
            elif "clear sky" in weatherDescription:
                localized_description_en = "clear skies"
                localized_description_hi = "आसमान साफ रहेगा।"
            elif "clouds" in weatherDescription:
                localized_description_en = "cloudy skies"
                localized_description_hi = "आसमान में बादल छाए रहेंगे।"
            elif "mist" in weatherDescription or "fog" in weatherDescription:
                localized_description_en = "misty conditions"
                localized_description_hi = "हल्की धुंध रहेगी।"
            else:
                # Fallback to a simple translation if we don't have a specific phrase
                localized_description_en = weatherDescription
                localized_description_hi = "मौसम का हाल है: " + hindidescription
            # --- Build the Final Response Message ---
            if lang == 'hi':
                message = f"{location} के लिए मौसम का हाल है: {temperature}°C, {localized_description_hi} और {humidity}% आर्द्रता।"
            else:
                message = f"The weather forecast for {location} is: {temperature}°C, with {localized_description_en} and {humidity}% humidity."

            return message
        else:
            return {"en": f"Error: Could not retrieve weather data for {location}.", "hi": f"त्रुटि: {location} के लिए मौसम डेटा प्राप्त नहीं किया जा सका।"}[lang]
    except requests.exceptions.RequestException as e:
        return f"A network error occurred: {e}"

# NOTE: The mocked diagnose_plant_disease function has been removed.

def route_query(query, lang='en'):
    """Router that directs query to the correct agent based on language."""
    query = query.lower()
    location = extract_location(query)
    # print(location)
    # --- EXPANDED KEYWORDS FOR BETTER DETECTION ---
    keywords = {
        "price": {"en": ["price", "rate", "cost", "mandi"], "hi": ["भाव", "दाम", "कीमत", "मंडी"]},
        "weather": {"en": ["weather", "forecast", "temperature"], "hi": ["मौसम", "तापमान"]},
        "disease": {
            "en": ["disease", "sick", "pest", "leaf", "plant", "infection", "spots", "ill"],
            "hi": ["बीमारी", "रोग", "पत्ती", "पौधा", "संक्रमण", "धब्बे", "बीमार"]
        }
    }

    # --- ROUTING LOGIC (REMAINS THE SAME) ---
    if any(word in query for word in keywords["price"]["en"] + keywords["price"]["hi"]):
        return get_market_price(query, lang)
    elif any(word in query for word in keywords["weather"]["en"] + keywords["weather"]["hi"]):
        return get_weather_forecast(location, lang)
    elif any(word in query for word in keywords["disease"]["en"] + keywords["disease"]["hi"]):
        return TEXT["trigger_disease"][lang]
    else:
        return TEXT["fallback_message"][lang]

# --- 3. STREAMLIT APP ---

# --- Page Config ---
st.set_page_config(page_title=TEXT["page_title"]["en"], page_icon=TEXT["page_icon"], layout="centered")

# --- Language Selection ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'en'
lang_choice = st.radio(
    "Choose Language / भाषा चुनें:",
    ('English', 'हिंदी (Hindi)'),
    horizontal=True,
    key='lang_selector'
)
st.session_state.language = 'hi' if lang_choice == 'हिंदी (Hindi)' else 'en'
lang = st.session_state.language

# --- Sidebar ---
with st.sidebar:
    st.title(TEXT["sidebar_title"][lang])
    st.markdown(TEXT["sidebar_welcome"][lang])
    st.markdown(TEXT["sidebar_what_i_do"][lang])
    st.markdown(TEXT["sidebar_feature_1"][lang])
    st.markdown(TEXT["sidebar_feature_2"][lang])
    st.markdown(TEXT["sidebar_feature_3"][lang])

# --- Main App ---
st.title(TEXT["app_title"][lang])
st.write(TEXT["app_intro"][lang])

# --- NEW: Initialize Dual Chat History ---
if "messages_en" not in st.session_state:
    st.session_state.messages_en = [{"role": "assistant", "content": TEXT["welcome_message"]["en"]}]
    st.session_state.messages_hi = [{"role": "assistant", "content": TEXT["welcome_message"]["hi"]}]

# --- Display the Correct Chat History ---
display_messages = st.session_state.messages_hi if lang == 'hi' else st.session_state.messages_en
for message in display_messages:
    avatar = "🧑‍🌾" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- User Input & Agent Logic ---
if prompt := st.chat_input(TEXT["chat_placeholder"][lang]):
    # A. Append the user prompt to both histories with immediate translation
    prompt_hi = simple_translate_to_hindi(prompt) if lang == 'en' else prompt
    prompt_en = prompt if lang == 'en' else simple_translate_to_hindi(prompt)
    st.session_state.messages_en.append({"role": "user", "content": prompt_en})
    st.session_state.messages_hi.append({"role": "user", "content": prompt_hi})

    # B. Display the user message
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.markdown(prompt)

    # C. Get the assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(TEXT["spinner_thinking"][lang]):
            response_text = route_query(prompt, lang)
            st.markdown(response_text)
    
    # D. Append the assistant's response to both histories
    response_en = response_text if lang == 'en' else simple_translate_to_hindi(response_text)
    response_hi = response_text if lang == 'hi' else simple_translate_to_hindi(response_text)
    st.session_state.messages_en.append({"role": "assistant", "content": response_en})
    st.session_state.messages_hi.append({"role": "assistant", "content": response_hi})
    st.rerun()

# --- Conditional File Uploader ---
# --- Conditional File Uploader ---
# Get the last message from the correct history list
last_message_list = st.session_state.messages_hi if lang == 'hi' else st.session_state.messages_en
if last_message_list and last_message_list[-1]["role"] == "assistant" and TEXT["trigger_upload_check"][lang] in last_message_list[-1]["content"]:
    
    uploaded_file = st.file_uploader(TEXT["upload_prompt"][lang], type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.chat_message("user", avatar="🧑‍🌾"):
            st.image(uploaded_file, caption=TEXT["upload_caption"][lang], width=150)
        
        # Append the image uploaded message to both histories
        image_uploaded_en = "[Image Uploaded]"
        image_uploaded_hi = "[तस्वीर अपलोड की गई]"
        st.session_state.messages_en.append({"role": "user", "content": image_uploaded_en})
        st.session_state.messages_hi.append({"role": "user", "content": image_uploaded_hi})

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner(TEXT["spinner_analyzing"][lang]):
                # Get the diagnosis in English from your model
                diagnosis_en = diagnose_plant_disease("temp_image.jpg")
                # Translate it to Hindi
                diagnosis_hi = simple_translate_to_hindi(diagnosis_en)

                if lang == 'hi':
                    st.markdown(diagnosis_hi)
                else:
                    st.markdown(diagnosis_en)
        
        # Append the diagnosis to both histories
        st.session_state.messages_en.append({"role": "assistant", "content": diagnosis_en})
        st.session_state.messages_hi.append({"role": "assistant", "content": diagnosis_hi})
        
        # We also need to add the post-diagnosis message
        post_diag_en = TEXT["post_diagnosis_message"]["en"]
        post_diag_hi = TEXT["post_diagnosis_message"]["hi"]
        st.session_state.messages_en.append({"role": "assistant", "content": post_diag_en})
        st.session_state.messages_hi.append({"role": "assistant", "content": post_diag_hi})

        # --- IMPORTANT: Rerun the app to update the chat history ---
        st.rerun()