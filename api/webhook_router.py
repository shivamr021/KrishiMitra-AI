import json
import traceback
from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from typing import Annotated, Optional
from core import router as tools
from agents.pest_detection_agent import diagnose_from_url
from utils.ai_processor import handle_query_with_ai, translate_final_text

router = APIRouter()
user_sessions = {}

@router.post("/chat")
async def chat_webhook(
    From: Annotated[str, Form()],
    Body: Annotated[Optional[str], Form()] = None,
    NumMedia: Annotated[int, Form()] = 0,
    MediaUrl0: Annotated[Optional[str], Form()] = None
):

    response_twiml = MessagingResponse()
    final_reply = ""
    user_id = From

    try:
        if NumMedia > 0 and MediaUrl0:
            diagnosis_en = diagnose_from_url(MediaUrl0)
            lang_code = user_sessions.get(user_id, {}).get("lang_code", "en")
            final_reply = translate_final_text(diagnosis_en, lang_code)
        else:
            print(f"--- User Query Received: \"{Body}\" ---")
            ai_action = handle_query_with_ai(Body)
            print(f"--- AI Action Parsed: {json.dumps(ai_action, indent=2)} ---")

            if "final_response" in ai_action:
                final_reply = ai_action["final_response"]
            
            elif "call_tool" in ai_action:
                tool_info = ai_action["call_tool"]
                tool_name = tool_info.get("tool_name")
                params = tool_info.get("parameters", {})
                lang_code = tool_info.get("lang_code", "en")
                
                user_sessions[user_id] = {"lang_code": lang_code}

                tool_result = ""
                if tool_name == "get_weather_forecast":
                    tool_result = tools.get_weather_forecast(params.get("location"))
                elif tool_name == "get_market_price":
                    tool_result = tools.get_market_price(params.get("commodity"), params.get("location"))
                elif tool_name == "diagnose_plant_disease":
                    tool_result = "Okay, please send me a clear photo of the plant's leaf."
                else:
                    tool_result = "I'm not sure how to handle that yet. Can you try rephrasing?"
                
                final_reply = translate_final_text(tool_result, lang_code)

    except Exception:
        traceback.print_exc()
        final_reply = "I'm sorry, a critical error occurred. Please try again in a moment."

    if not final_reply:
        final_reply = "I'm sorry, I couldn't process that request. Please try rephrasing."

    response_twiml.message(final_reply)
    
    final_response_str = str(response_twiml)
    print(f"--- Sending TwiML Response: {final_response_str} ---")
    return Response(content=final_response_str, media_type="application/xml")
