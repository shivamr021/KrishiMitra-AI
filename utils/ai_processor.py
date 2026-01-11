import google.generativeai as genai
import json
from core.config import settings

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
    print("✅ Gemini AI model configured successfully using 'gemini-flash-latest'.")
except Exception as e:
    model = None
    print(f"CRITICAL ERROR: Failed to configure Gemini AI. Check your API key. Error: {e}")

def handle_query_with_ai(user_query: str) -> dict:
    if not model:
        return {"final_response": "AI model is not available. Please check the server configuration."}

    meta_prompt = f"""
    You are KrishiMitra, a friendly and helpful AI assistant for farmers.
    Your primary goal is to understand a farmer's query in their native language and provide an appropriate action or response.
    Adopt a conversational and encouraging tone, like a knowledgeable friend ("mitra").
    Analyze the user's query and the language it is in.

    Your tools:
    1. `get_weather_forecast`: For weather-related queries. Requires a `location` (city name).
    2. `get_market_price`: For crop market prices ("mandi bhav"). Requires a `commodity` (e.g., "Soyabean", "Gehu") and an optional `location`.
    3. `diagnose_plant_disease`: If the user mentions a sick plant, pests, leaves with spots, etc., and wants to send a photo.
    4. `general_greeting_or_chat`: For simple greetings, thanks, or general questions that don't fit other tools.

    Analyze the query below and respond with a JSON object ONLY. The JSON object must have one of two main keys:

    A) "call_tool": If a specific tool is needed. The value MUST be an object containing:
       - "tool_name": One of the tool names from the list above.
       - "parameters": An object with the required parameters extracted from the query (e.g., {{"location": "Indore", "commodity": "Wheat"}}).
       - "lang_code": The two-letter ISO 639-1 code of the user's language (e.g., "hi" for Hindi, "en" for English, "mr" for Marathi).

    B) "final_response": Use this for `general_greeting_or_chat`. The value MUST be a complete, ready-to-send response.
       **IMPORTANT**: This final response MUST be in the user's original language, as identified by the `lang_code`.

    ---
    User Query: "{user_query}"
    ---

    Respond with ONLY the JSON object. Do not add any extra text or formatting.
    """
    try:
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        ]
        response = model.generate_content(meta_prompt, safety_settings=safety_settings)
        json_string = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_string)
    except Exception as e:
        print(f"Gemini Meta-Prompt Error: {e}")
        return {"final_response": "I'm sorry, I had trouble understanding that. Can you please rephrase?"}
    

def translate_final_text(text: str, lang_code: str) -> str:
    if lang_code == 'en' or not model:
        return text
    prompt = f"Translate the following text to the language with the code '{lang_code}'. Respond with only the translated text. Text: \"{text}\""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Final translation error: {e}")
        return text
