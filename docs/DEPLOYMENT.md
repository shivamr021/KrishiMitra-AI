# Deployment Workflow

## Frontend
- Deployed on Vercel
- Handles landing page and WhatsApp redirection

## Backend
- Deployed on Hugging Face Spaces
- FastAPI + Gunicorn/Uvicorn stack

## Messaging Integration
- Twilio WhatsApp Sandbox
- Webhook-based request handling

## AI Pipeline
- Local TensorFlow model for primary inference
- Gemini Vision fallback for uncertain predictions
