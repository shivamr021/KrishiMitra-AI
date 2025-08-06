import requests
from dotenv import load_dotenv
import os
import json
import re
import streamlit as st
import spacy
from googletrans import Translator
import time
from bs4 import BeautifulSoup
# --- IMPORT THE REAL DIAGNOSIS FUNCTION ---
from model.pest_detector import diagnose_plant_disease

# --- 1. TEXT & LOCALIZATION ---
TEXT = {
    "page_title": {"en": "KrishiMitra", "hi": "कृषि मित्र"},
    "page_icon": "🌿",
    "main_chat_placeholder": {"en": "Or ask me anything directly...", "hi": "या मुझसे सीधे कुछ भी पूछें..."},
    "welcome_message": {"en": "Hello, farmer! How can I help you today?", "hi": "नमस्ते किसान! मैं आपकी कैसे मदद कर सकता हूँ?"},
    "trigger_disease": {"en": "It sounds like you have a sick plant. *Please upload a photo of the affected leaf below.", "hi": "लगता है आपके पौधे में कोई बीमारी है। **कृपया नीचे प्रभावित पत्ती की तस्वीर अपलोड करें।*"},
    "trigger_upload_check": {"en": "upload a photo", "hi": "तस्वीर अपलोड करें"},
    "fallback_message": {"en": "I'm sorry, I can only help with market prices, weather, crop planning, and plant diseases.", "hi": "माफ़ कीजिए, मैं केवल बाजार भाव, मौसम, फसल योजना और पौधों की बीमारियों में मदद कर सकता हूँ।"},
    "crop_planner_title": {"en": "Crop Planner(Coming Soon)", "hi": "फसल योजनाकार(जल्द आ रहा है)"},
    "crop_planner_desc": {"en": "What should I grow?", "hi": "मुझे क्या उगाना चाहिए?"},
    "water_manage_title": {"en": "Weather Condition", "hi": "मौसम की स्थिति"},
    "water_manage_desc": {"en": "how's the Weather?", "hi": "मौसम कैसा है?"},
    "market_price_title": {"en": "Market Price", "hi": "बाजार मूल्य"},
    "market_price_desc": {"en": "Mandi rates", "hi": "मंडी रेट"},
    "pest_alert_title": {"en": "Pest Alert", "hi": "कीट चेतावनी"},
    "pest_alert_desc": {"en": "Detect crop disease", "hi": "फसल रोग का पता लगाएं"},
    "crop_agent_title": {"en": "Crop Agent", "hi": "फसल एजेंट"},
    "crop_agent_desc": {"en": "Best crop this month", "hi": "इस महीने की सबसे अच्छी फसल"},
    "best_crop_suggestion": {"en": f"Considering it's August in Indore, moong (मूंग) or maize (मक्का) are good options.", "hi": f"इंदौर में अगस्त को देखते हुए, मूंग या मक्का अच्छे विकल्प हैं।"},
    "sidebar_title": {"en": "🌿 KrishiMitra", "hi": "🌿 कृषि मित्र"},
    "sidebar_welcome": {"en": "Welcome to KrishiMitra, your AI-powered farming assistant.", "hi": "कृषि मित्र में आपका स्वागत है, यह आपका AI-संचालित खेती सहायक है।"},
    "sidebar_what_i_do": {"en": "*What can I do?", "hi": "मैं क्या कर सकता हूँ?*"},
    "sidebar_feature_1": {"en": "- 🌱 Plan your crops.", "hi": "- 🌱 अपनी फसलों की योजना बनाना।"},
    "sidebar_feature_2": {"en": "- 💧 Provide weather & water info.", "hi": "- 💧 मौसम और पानी की जानकारी देना।"},
    "sidebar_feature_3": {"en": "- 📈 Give current market prices.", "hi": "- 📈 फसलों के बाजार भाव प्रदान करना।"},
    "sidebar_feature_4": {"en": "- 🔬 Diagnose plant diseases.", "hi": "- 🔬 पौधों की बीमारियों का पता लगाना।"},
    "app_title": {"en": "🤖 KrishiMitra Assistant", "hi": "🤖 कृषि मित्र सहायक"},
    "app_intro": {"en": "Ask me about crop prices, weather, or upload a photo of a sick plant!", "hi": "मुझसे फसल की कीमतों, मौसम के बारे में पूछें, या किसी बीमार पौधे की तस्वीर अपलोड करें!"},
    "chat_placeholder": {"en": "Ask a follow-up question...", "hi": "अगला प्रश्न पूछें..."},
    "spinner_thinking": {"en": "Thinking...", "hi": "सोच रहा हूँ..."},
    "spinner_analyzing": {"en": "Analyzing the image...", "hi": "तस्वीर का विश्लेषण हो रहा है..."},
    "upload_prompt": {"en": "Choose a plant leaf image...", "hi": "पौधे की पत्ती की एक तस्वीर चुनें..."},
    "upload_caption": {"en": "Uploaded Image.", "hi": "अपलोड की गई तस्वीर।"},
    "post_diagnosis_message": {"en": "Here is the diagnosis for your plant.", "hi": "आपके पौधे की जांच की रिपोर्ट यहाँ है।"},
    "back_to_menu": {"en": "⬅ Back to Menu", "hi": "⬅ मेनू पर वापस जाएं"}
}
st.set_page_config(page_title="KrishiMitra", page_icon=TEXT["page_icon"], layout="centered")

if 'language' not in st.session_state: st.session_state.language = 'en'
if "messages_en" not in st.session_state: st.session_state.messages_en = []
if "messages_hi" not in st.session_state: st.session_state.messages_hi = []
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'hybrid'  # Start in 'hybrid' mode (cards + chat)
if 'view' not in st.session_state: st.session_state.view = 'menu'
if "initial_prompt" not in st.session_state: st.session_state.initial_prompt = None
if 'card_clicked' not in st.session_state: st.session_state.card_clicked = None
if 'cards_hidden' not in st.session_state: st.session_state.cards_hidden = False

lang = st.session_state.language

# Translation function
def simple_translate_to_hindi(text_to_translate):
    translator = Translator()
    translation = translator.translate(text_to_translate, dest='hi')
    return translation.text

# --- 2. BILINGUAL AGENT FUNCTIONS ---

def get_market_price(query, location='indore', lang='en'):
    """
    Identifies a known crop from the user's query and scrapes its live price.
    If the crop is not recognized, it provides a link to the main commodities page.
    """
    query = query.lower()
    
    # This dictionary maps keywords to the specific URL slugs on the website
    CROP_URL_SLUGS = {
        "soybean": "soyabean-soyabean",
        "soya bean": "soyabean-soyabean",
        "सोयाबीन": "soyabean-soyabean",
        "wheat": "wheat",
        "gehu": "wheat",
        "गेहूं": "wheat",
        "cotton": "cotton-kapas",
        "kapas": "cotton-kapas",
        "कपास": "cotton-kapas"
    }
    
    crop_slug = None
    crop_display_name = ""
    for keyword, slug in CROP_URL_SLUGS.items():
        if keyword in query:
            crop_slug = slug
            crop_display_name = keyword.split('-')[0].capitalize()
            break
            
    # --- NEW, IMPROVED FALLBACK LOGIC ---
    if not crop_slug:
        commodities_url = "https://mandibhavindia.in/commodities"
        if lang == 'en':
            return f"I don't have a specific scraper for that crop yet. You can find a full list of all available commodities here:\n{commodities_url}"
        else:
            return f"मेरे पास अभी उस फसल के लिए एक विशिष्ट स्क्रैपर नहीं है। आप सभी उपलब्ध जिंसों की पूरी सूची यहां देख सकते हैं:\n{commodities_url}"

    # --- Scraper Logic (remains the same) ---
    URL = f"https://mandibhavindia.in/commodity/{crop_slug}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price_table = soup.find('table')
        if not price_table:
            raise ValueError("Price table not found on the page.")

        rows = price_table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            market_name = cells[0].get_text(strip=True).lower()
            if location in market_name:
                min_price = cells[2].get_text(strip=True)
                max_price = cells[3].get_text(strip=True)
                modal_price = cells[4].get_text(strip=True)
                
                if lang == 'en':
                    return f"""
                    Here are the live prices for *{crop_display_name}* in the *{location.capitalize()}* market:
                    - *Min Price:* ₹{min_price} / Quintal
                    - *Max Price:* ₹{max_price} / Quintal
                    - *Modal (Average) Price:* ₹{modal_price} / Quintal
                    """
                else:
                    return f"""
                    *{location.capitalize()}* मंडी में *{crop_display_name}* के लाइव भाव यहाँ दिए गए हैं:
                    - *न्यूनतम मूल्य:* ₹{min_price} / क्विंटल
                    - *अधिकतम मूल्य:* ₹{max_price} / क्विंटल
                    - *औसत मूल्य:* ₹{modal_price} / क्विंटल
                    """
        
        return f"Could not find price data for {location.capitalize()} in the {crop_display_name} listings today. You can check all markets here: {URL}"

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        if lang == 'en':
            return f"Sorry, I couldn't fetch the live prices right now. You can check manually at this link:\n{URL}"
        else:
            return f"माफ़ कीजिए, मैं अभी लाइव भाव प्राप्त नहीं कर सका। आप इस लिंक पर स्वयं जांच सकते हैं:\n{URL}"
    


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
    """Returns comprehensive weather forecast in the selected language."""

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found. Please set it in the .env file."
    
    # Get current weather
    current_url = "http://api.openweathermap.org/data/2.5/weather"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    try:
        # Get current weather
        current_params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        current_response = requests.get(current_url, params=current_params)
        
        # Get 5-day forecast
        forecast_params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        forecast_response = requests.get(forecast_url, params=forecast_params)
        
        if current_response.status_code == 200 and forecast_response.status_code == 200:
            current_data = current_response.json()
            forecast_data = forecast_response.json()
            
            # Extract current weather data
            temp = current_data['main']['temp']
            feels_like = current_data['main']['feels_like']
            humidity = current_data['main']['humidity']
            pressure = current_data['main']['pressure']
            wind_speed = current_data['wind']['speed']
            wind_direction = current_data['wind'].get('deg', 0)
            weather_desc = current_data['weather'][0]['description']
            weather_main = current_data['weather'][0]['main']
            visibility = current_data.get('visibility', 10000) / 1000  # Convert to km
            
            # Get sunrise and sunset times
            sunrise = time.strftime('%H:%M', time.localtime(current_data['sys']['sunrise']))
            sunset = time.strftime('%H:%M', time.localtime(current_data['sys']['sunset']))
            
            # Analyze forecast for trends
            forecast_list = forecast_data['list']
            temp_trend = []
            rain_chance = []
            
            for item in forecast_list[:8]:  # Next 24 hours (3-hour intervals)
                temp_trend.append(item['main']['temp'])
                if 'rain' in item.get('weather', [{}])[0].get('main', '').lower():
                    rain_chance.append(True)
                else:
                    rain_chance.append(False)
            
            # Calculate trends
            temp_min = min(temp_trend)
            temp_max = max(temp_trend)
            rain_probability = (sum(rain_chance) / len(rain_chance)) * 100 if rain_chance else 0
            
            # Professional weather descriptions
            weather_descriptions = {
                'Clear': {
                    'en': 'Clear skies with excellent visibility',
                    'hi': 'साफ आसमान, उत्कृष्ट दृश्यता'
                },
                'Clouds': {
                    'en': 'Partly cloudy conditions',
                    'hi': 'आंशिक रूप से बादल छाए रहेंगे'
                },
                'Rain': {
                    'en': 'Rainy conditions expected',
                    'hi': 'बारिश की संभावना है'
                },
                'Thunderstorm': {
                    'en': 'Thunderstorm activity likely',
                    'hi': 'आंधी-तूफान की संभावना है'
                },
                'Drizzle': {
                    'en': 'Light drizzle expected',
                    'hi': 'हल्की बूंदाबांदी की संभावना है'
                },
                'Mist': {
                    'en': 'Misty conditions with reduced visibility',
                    'hi': 'धुंधली स्थिति, कम दृश्यता'
                },
                'Fog': {
                    'en': 'Foggy conditions with poor visibility',
                    'hi': 'कोहरा, खराब दृश्यता'
                },
                'Snow': {
                    'en': 'Snowfall expected',
                    'hi': 'बर्फबारी की संभावना है'
                }
            }
            
            # Get appropriate description
            weather_desc_localized = weather_descriptions.get(
                weather_main, 
                {'en': weather_desc, 'hi': simple_translate_to_hindi(weather_desc)}
            )
            
            # Wind direction helper
            def get_wind_direction(degrees):
                directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
                index = round(degrees / 22.5) % 16
                return directions[index]
            
            wind_dir = get_wind_direction(wind_direction)
            
            # Build comprehensive weather report
            if lang == 'hi':
                report = f"""🌤 {location} का विस्तृत मौसम विवरण

वर्तमान स्थिति:
* तापमान: {temp}°C (महसूस हो रहा: {feels_like}°C)
* मौसम: {weather_desc_localized['hi']}
* आर्द्रता: {humidity}%
* वायु दाब: {pressure} hPa
* हवा: {wind_speed} km/h {wind_dir} दिशा से
* दृश्यता: {visibility:.1f} km

सूर्योदय/सूर्यास्त:
* सूर्योदय: {sunrise}
* सूर्यास्त: {sunset}

24 घंटे का पूर्वानुमान:
* तापमान सीमा: {temp_min:.1f}°C - {temp_max:.1f}°C
* बारिश की संभावना: {rain_probability:.0f}%

कृषि सलाह:
{f"⚠ बारिश की संभावना है - फसल संरक्षण के उपाय करें" if rain_probability > 30 else "✅ मौसम अनुकूल है - सामान्य कृषि गतिविधियां जारी रखें"}"""
            else:
                report = f"""🌤 Detailed Weather Report for {location}

Current Conditions:
* Temperature: {temp}°C (Feels like: {feels_like}°C)
* Weather: {weather_desc_localized['en']}
* Humidity: {humidity}%
* Pressure: {pressure} hPa
* Wind: {wind_speed} km/h from {wind_dir}
* Visibility: {visibility:.1f} km

Sunrise/Sunset:
* Sunrise: {sunrise}
* Sunset: {sunset}

24-Hour Forecast:
* Temperature Range: {temp_min:.1f}°C - {temp_max:.1f}°C
* Rain Probability: {rain_probability:.0f}%

Agricultural Advisory:
{f"⚠ Rain expected - Take crop protection measures" if rain_probability > 30 else "✅ Weather favorable - Continue normal farming activities"}"""

            return report
        else:
            return {"en": f"Error: Could not retrieve weather data for {location}.", "hi": f"त्रुटि: {location} के लिए मौसम डेटा प्राप्त नहीं किया जा सका।"}[lang]
    except requests.exceptions.RequestException as e:
        return f"A network error occurred: {e}"

# NOTE: The mocked diagnose_plant_disease function has been removed.

def route_query(query, lang='en'):
    """Router that directs query to the correct agent based on language."""
    query = query.lower()
    location = extract_location(query) or 'indore' # Use extracted location or default to Indore

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
        # --- Pass BOTH the query and the location ---
        return get_market_price(query, location, lang)
    elif any(word in query for word in keywords["weather"]["en"] + keywords["weather"]["hi"]):
        if location:
            return get_weather_forecast(location, lang)
        else:
            return "Sure, I can get the weather. For which city?" if lang == 'en' else "ज़रूर, मैं मौसम बता सकता हूँ। किस शहर के लिए?"
    elif any(word in query for word in keywords["disease"]["en"] + keywords["disease"]["hi"]):
        return TEXT["trigger_disease"][lang]
    else:
        return TEXT["fallback_message"][lang]



def process_and_display(prompt, change_view=False):
    # This function now accepts an optional flag
    prompt_en = simple_translate_to_hindi(prompt) if lang == 'hi' else prompt
    prompt_hi = simple_translate_to_hindi(prompt) if lang == 'en' else prompt
    st.session_state.messages_en.append({"role": "user", "content": prompt_en})
    st.session_state.messages_hi.append({"role": "user", "content": prompt_hi})
    
    response_en = route_query(prompt_en, 'en')
    response_hi = simple_translate_to_hindi(response_en)
    st.session_state.messages_en.append({"role": "assistant", "content": response_en})
    st.session_state.messages_hi.append({"role": "assistant", "content": response_hi})
    
    # If the flag is set (i.e., a card was clicked), change the view mode
    if change_view:
        st.session_state.view_mode = 'chat_only'
        
    st.rerun()

# --- 3. STREAMLIT APP ---



# --- Page Config ---
st.markdown("""
<style>
    body{
        background-color:#FAF8F1;    
    }
    .header-lang-container button[kind="secondary"] {
        background-color: #2a2a72;
        color: #fff;
        font-weight: bold;
        font-size: 16px;
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    /* --- Agent Box Styles --- */
    .crop-agent-box {
        background-color: #F0FFF0; border: 1px solid #D0E0D0;
        border-radius: 0.75rem; padding: 1rem; margin-top: 1rem;
    }
    button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #222 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        white-space: normal !important;
        line-height: 1.3 !important;
    }

    button[kind="secondary"]:hover {
        background-color: #eaeaea;
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    button[kind="secondary"]:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(0,123,255,.25);
    }
</style>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown(f"## {TEXT['sidebar_title'][lang]}")
    st.markdown(TEXT['sidebar_welcome'][lang])
    st.markdown("---")
    st.markdown(TEXT['sidebar_what_i_do'][lang])
    st.markdown(TEXT['sidebar_feature_1'][lang])
    st.markdown(TEXT['sidebar_feature_2'][lang])
    st.markdown(TEXT['sidebar_feature_3'][lang])
    st.markdown(TEXT['sidebar_feature_4'][lang])
    st.markdown("---")

# --- 6. MAIN APP LAYOUT ---
# Header
titles = {
    "en": "KrishiMitra",
    "hi": "कृषिमित्र"
}
header_cols = st.columns([1, 4, 2])
with header_cols[0]:
    st.image("logo op 1.png", width=110)
with header_cols[1]:
    st.markdown(f"<h2 style='margin: 0; padding-top: 18px; font-size:50px;'>{titles.get(st.session_state.language, 'KrishiMitra')}</h2>", unsafe_allow_html=True)
with header_cols[2]:
    lang_map = {"English": "en", "हिंदी": "hi"}
    selected_label = st.radio(
        "Language",
        options=list(lang_map.keys()),
        index=0 if st.session_state.language == "en" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    selected_lang = lang_map[selected_label]

    if st.session_state.language != selected_lang:
        st.session_state.language = selected_lang
        st.rerun()


# Only show cards if cards are not hidden
if st.session_state.view_mode == 'hybrid' and not st.session_state.cards_hidden:
    # Row 1
    # Hybrid Mode Cards (Refactored with custom HTML + button)
    card_data = [
        {
            "title": TEXT['pest_alert_title'][lang],
            "desc": TEXT['pest_alert_desc'][lang],
            "icon": "🐛",
            "key": "pest_card"
        },
        {
            "title": TEXT['water_manage_title'][lang],
            "desc": TEXT['water_manage_desc'][lang],
            "icon": "💧",
            "key": "water_card"
        },
        {
            "title": TEXT['market_price_title'][lang],
            "desc": TEXT['market_price_desc'][lang],
            "icon": "🏷",
            "key": "price_card"
        },
        {
            "title": TEXT['crop_planner_title'][lang],
            "desc": TEXT['crop_planner_desc'][lang],
            "icon": "🌱",
            "key": "planner_card"
        }
    ]

    # Render cards in 2 columns
    # Render cards in 2 columns - FULLY CLICKABLE
    for i in range(0, len(card_data), 2):
        col1, col2 = st.columns(2)
        for idx, col in enumerate([col1, col2]):
            if i + idx < len(card_data):
                card = card_data[i + idx]
                with col:
                    clicked = st.button(
                        f"{card['icon']}  \n### {card['title']}  \n{card['desc']}",
                        key=card['key'],
                        use_container_width=True
                    )
                    if clicked:
                        st.session_state.card_clicked = card['desc']
                        st.session_state.cards_hidden = True
                        st.rerun() 



    # Crop Agent box
    st.markdown(f"""
    <div class="crop-agent-box">
        <div style="font-weight: bold; color: #333;">🌱 {TEXT['crop_agent_title'][lang]}: <span style="font-weight: 500;">{TEXT['crop_agent_desc'][lang]}</span></div>
        <div style="font-size: 0.9rem; color: #555;">{TEXT['best_crop_suggestion'][lang]}</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

# --- 8. CHAT HISTORY (always visible) ---
messages_to_display = st.session_state.messages_hi if lang == 'hi' else st.session_state.messages_en
if not messages_to_display:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(TEXT["welcome_message"][lang])
for message in messages_to_display:
    with st.chat_message(message["role"], avatar="🧑‍🌾" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# File upload logic (always visible if triggered)
last_message = messages_to_display[-1] if messages_to_display else {}
if last_message.get("role") == "assistant" and TEXT["trigger_upload_check"][lang] in last_message.get("content", "").lower():
    uploaded_file = st.file_uploader(TEXT["upload_prompt"][lang], type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.success("Image uploaded! Analysis would proceed here.")

# --- 9. CHAT INPUT BAR (always visible) ---
# Handle card clicks and set initial prompt
if 'card_clicked' not in st.session_state:
    st.session_state.card_clicked = None

# Check if a card was clicked and set the initial prompt
if st.session_state.card_clicked:
    initial_prompt = st.session_state.card_clicked
    st.session_state.card_clicked = None  # Reset
    # Process the prompt immediately
    process_and_display(initial_prompt)

# Create chat input
user_input = st.chat_input(TEXT["main_chat_placeholder"][lang], key="main_chat")
if user_input:
    process_and_display(user_input) # A normal chat input does not change the view