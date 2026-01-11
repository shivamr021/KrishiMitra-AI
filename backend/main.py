import numpy as np
from fastapi import FastAPI, Request
from api import webhook_router
from utils.ai_processor import handle_query_with_ai
from agents.pest_detection_agent import model as pest_model
from typing import Any

app = FastAPI(
    title="KrishiMitra AI Backend",
    description="Backend service for the KrishiMitra WhatsApp Chatbot.",
    version="2.1.0"
)

# --- Application Startup Event for Warm-Up ---
@app.on_event("startup")
def warmup_models():
    """
    Runs when the application starts to initialize models and prevent 
    cold-start timeouts on the first user request.
    """
    print("🚀 Starting model warm-up...")
    
    # 1. Warm up the Gemini AI model
    try:
        print("   - Warming up Gemini AI...")
        handle_query_with_ai("Hello")
        print("   ✅ Gemini AI is warm.")
    except Exception as e:
        print(f"   ⚠️ Could not warm up Gemini AI: {e}")

    # 2. Warm up the Pest Detection (TensorFlow) model
    try:
        if pest_model:
            print("   - Warming up Pest Detection model...")
            dummy_image = np.zeros((1, 224, 224, 3), dtype=np.float32)
            pest_model.predict(dummy_image, verbose=0)
            print("   ✅ Pest Detection model is warm.")
        else:
            print("   ⚠️ Pest Detection model not found, skipping warm-up.")
    except Exception as e:
        print(f"   ⚠️ Could not warm up Pest Detection model: {e}")
        
    print("✅ Warm-up complete. Application is ready.")

# Include the main webhook router
app.include_router(webhook_router.router, prefix="/twilio", tags=["Twilio Webhook"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "KrishiMitra Backend is running!"}

@app.post("/twilio/error")
async def twilio_error_webhook(request: Request) -> dict[str, Any]:
    """
    Twilio Debugger often posts as x-www-form-urlencoded.
    Be permissive: try JSON, then form, else log raw body.
    Never raise here.
    """
    ctype = request.headers.get("content-type", "")
    payload: dict[str, Any] = {}

    try:
        if "application/json" in ctype.lower():
            payload = await request.json()
        else:
            form = await request.form()
            payload = dict(form)
    except Exception as e:
        raw = (await request.body())[:2000]
        print("[TWILIO DEBUGGER RAW]", raw)
        print("[TWILIO DEBUGGER PARSE ERROR]", e)

    print("[TWILIO DEBUGGER PAYLOAD]", payload)
    return {"status": "received"}