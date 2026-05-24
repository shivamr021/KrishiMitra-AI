# KrishiMitra Architecture

## System Overview

KrishiMitra is a multilingual AI-powered agricultural assistant delivered through WhatsApp.

The system combines:
- Computer Vision
- LLM-based reasoning
- Real-time agricultural APIs
- Hybrid inference routing

to provide scalable farmer assistance.

---

## High-Level Workflow

User
↓
Twilio WhatsApp Webhook
↓
FastAPI Backend
↓
Intent Router
├── Weather Agent
├── Market Price Agent
└── Disease Detection Agent
        ↓
Custom CNN Model
        ↓ low confidence
Gemini Vision Fallback
        ↓
Response Generator
↓
WhatsApp Response

---

## Core Technologies

- FastAPI
- TensorFlow/Keras
- Gemini Pro Vision
- Twilio API
- Hugging Face Spaces
- OpenWeatherMap API
