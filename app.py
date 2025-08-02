# app.py - KrishiMitra (Bilingual Version)
import requests
from dotenv import load_dotenv
import os
import streamlit as st
import time
from model.pest_detector import diagnose_plant_disease

# --- 1. TEXT & LOCALIZATION ---
# A dictionary to hold all UI text for both languages
TEXT = {
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

# --- 2. BILINGUAL AGENT FUNCTIONS ---

def get_market_price(crop_name, lang='en'):
    """Returns market price in the selected language."""
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

def get_weather_forecast(location, lang='en'):
    load_dotenv()
    """Returns weather forecast in the selected language."""
    responses = {
        "en": f"The weather forecast for {location} is: 28°C, clear skies, with a slight chance of rain in the evening.",
        "hi": f"{location} के लिए मौसम का पूर्वानुमान है: 28°C, आसमान साफ रहेगा, शाम को हल्की बारिश की संभावना है।"
    }

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found. Please set it in the .env file."
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    completeUrl = f"{base_url}q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(completeUrl)
        if response.status_code == 200:
            data = response.json()
            print(data)
            temperature = data['main']['temp']
            weatherDescription = data['weather'][0]['description']
            humidity = data['main']['humidity']
            responses = {
        "en": f"The weather forecast for {location} is: {temperature}°C, and {weatherDescription} with {humidity}% Humidity",
        "hi": f"{location} के लिए मौसम का पूर्वानुमान है: {temperature}°C, आसमान साफ रहेगा, शाम को हल्की बारिश की संभावना है।"
    }
            return responses[lang]
        else:
            return f"response is not valid"
    except requests.exceptions.RequestException as e:
        return f"A network error occurred: {e}"

def diagnose_plant_disease(image_data, lang='en'):
    """Returns plant diagnosis in the selected language."""
    time.sleep(3) # Simulate model processing time
    responses = {
        "en": "Diagnosis complete. The plant appears to have **Late Blight**. Recommended action: Apply a copper-based fungicide immediately.",
        "hi": "जांच पूरी हुई। पौधे में **पिछेती झुलसा (Late Blight)** रोग लग रहा है। सुझाया गया उपाय: तुरंत तांबे पर आधारित फफूंदनाशक का छिड़काव करें।"
    }
    return responses[lang]

def route_query(query, lang='en'):
    """Router that directs query to the correct agent based on language."""
    query = query.lower()
    keywords = {
        "price": {"en": ["price", "rate", "cost", "mandi"], "hi": ["भाव", "दाम", "कीमत", "मंडी"]},
        "weather": {"en": ["weather", "forecast"], "hi": ["मौसम"]},
        "disease": {"en": ["disease", "sick", "pest", "leaf"], "hi": ["बीमारी", "रोग", "पत्ती"]}
    }

    if any(word in query for word in keywords["price"]["en"] + keywords["price"]["hi"]):
        return get_market_price(query, lang)
    elif any(word in query for word in keywords["weather"]["en"] + keywords["weather"]["hi"]):
        return get_weather_forecast("Indore", lang)
    elif any(word in query for word in keywords["disease"]["en"] + keywords["disease"]["hi"]):
        return TEXT["trigger_disease"][lang]
    else:
        return TEXT["fallback_message"][lang]

# --- 3. STREAMLIT APP ---

# --- Page Config ---
st.set_page_config(page_title=TEXT["page_title"]["en"], page_icon=TEXT["page_icon"], layout="centered")

# --- Language Selection ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'en'  # Default to English

# Place language selector at the top
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

# --- Chat History Management ---
if "messages" not in st.session_state:
    # Reset messages if language changes
    st.session_state.messages = [{"role": "assistant", "content": TEXT["welcome_message"][lang]}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input & Chat Logic ---
if prompt := st.chat_input(TEXT["chat_placeholder"][lang]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(TEXT["spinner_thinking"][lang]):
            response = route_query(prompt, lang)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Conditional File Uploader ---
if st.session_state.messages[-1]["role"] == "assistant" and TEXT["trigger_upload_check"][lang] in st.session_state.messages[-1]["content"]:
    
    uploaded_file = st.file_uploader(TEXT["upload_prompt"][lang], type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        with st.chat_message("user"):
            st.image(uploaded_file, caption=TEXT["upload_caption"][lang], width=150)
        
        st.session_state.messages.append({"role": "user", "content": "[Image Uploaded]"})

        with st.chat_message("assistant"):
            with st.spinner(TEXT["spinner_analyzing"][lang]):
                diagnosis = diagnose_plant_disease(uploaded_file, lang)
                st.markdown(diagnosis)
        
        st.session_state.messages.append({"role": "assistant", "content": diagnosis})
        
        st.session_state.messages[-3]["content"] = TEXT["post_diagnosis_message"][lang]
        st.experimental_rerun()