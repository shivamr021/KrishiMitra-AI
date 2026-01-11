import requests
import numpy as np
import json
import os
import uuid
from keras.utils import load_img, img_to_array
from keras.applications.efficientnet import preprocess_input
from core.config import settings
from keras.models import Model
from keras.applications import EfficientNetB0
from keras.layers import Input, GlobalAveragePooling2D, Dense, Dropout
import google.generativeai as genai
from PIL import Image

def create_model_architecture(num_classes):
    inputs = Input(shape=(224, 224, 3))
    base_model = EfficientNetB0(weights=None, include_top=False, input_tensor=inputs)
    x = base_model.output
    x = GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = Dense(256, activation='relu', name="dense_256")(x)
    x = Dropout(0.5, name="dropout_layer")(x)
    outputs = Dense(num_classes, activation='softmax', name="output_layer")(x)
    model = Model(inputs=inputs, outputs=outputs)
    return model

try:
    with open(settings.CLASS_NAMES_PATH, 'r') as f:
        CLASS_NAMES = json.load(f)
    model = create_model_architecture(num_classes=len(CLASS_NAMES))
    model.load_weights(settings.MODEL_PATH)
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load ML model or class names: {e}")
    model = None
    CLASS_NAMES = []

HEALTHY_CLASSES = {
    "Apple leaf",
    "Bell_pepper leaf",
    "Blueberry leaf",
    "Cherry leaf",
    "Peach leaf",
    "Raspberry leaf",
    "Soyabean leaf",
    "Strawberry leaf",
    "Tomato leaf",
    "grape leaf"
}

REMEDY_KNOWLEDGE_BASE = {
    "Apple Scab Leaf": "Apply a fungicide containing captan or mancozeb. Prune infected areas and remove fallen leaves to reduce fungal spread.",
    "Apple rust leaf": "Use fungicides like myclobutanil or triadimefon. Remove nearby cedar trees if possible, as they are alternate hosts for the rust fungus.",
    "Bell_pepper leaf spot": "Apply copper-based bactericides preventatively. Ensure good air circulation and avoid overhead watering.",
    "Corn Gray leaf spot": "Use resistant corn hybrids and practice crop rotation with non-host crops. Fungicides like pyraclostrobin can be effective.",
    "Corn leaf blight": "Practice crop rotation and tillage to bury crop residue. Apply fungicides if the disease appears early on susceptible hybrids.",
    "Corn rust leaf": "Plant resistant hybrids. Foliar fungicides can be applied when rust pustules first appear.",
    "Potato leaf early blight": "Apply a fungicide containing mancozeb or chlorothalonil. Maintain plant health with proper nutrition and irrigation.",
    "Potato leaf late blight": "Extremely destructive. Immediately remove and destroy affected plants. Apply a copper-based or systemic fungicide preventatively.",
    "Squash Powdery mildew leaf": "Apply horticultural oils, neem oil, or fungicides containing sulfur or potassium bicarbonate. Improve air circulation around plants.",
    "grape leaf black rot": "Prune out and destroy infected parts (leaves, fruit). Apply fungicides like mancozeb or captan starting from early spring.",
    "Tomato Early blight leaf": "Apply fungicides containing chlorothalonil or mancozeb. Mulch around plants and use stakes to keep them off the ground.",
    "Tomato Septoria leaf spot": "Remove infected lower leaves. Apply fungicides like chlorothalonil. Avoid overhead watering.",
    "Tomato leaf bacterial spot": "Apply copper-based sprays. Difficult to control once established. Remove infected plants to prevent spread.",
    "Tomato leaf late blight": "Very serious. Remove and destroy infected plants immediately. Use preventative fungicides like chlorothalonil.",
    "Tomato leaf mosaic virus": "There is no cure. Remove and destroy infected plants to prevent spread to others. Control insects that may transmit the virus.",
    "Tomato leaf yellow virus": "No cure. Transmitted by whiteflies. Control whitefly populations with insecticides or neem oil. Remove and destroy infected plants.",
    "Tomato mold leaf": "Also known as Leaf Mold. Ensure good air circulation and lower humidity. Apply fungicides containing chlorothalonil or mancozeb."
}
DEFAULT_REMEDY = "Consult a local agricultural expert for specific treatment options."
IMG_SIZE = 224

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    print("✅ Gemini Vision model configured successfully for pest detection fallback.")
except Exception as e:
    vision_model = None
    print(f"WARNING: Could not configure Gemini Vision model. Fallback will not work. Error: {e}")

def diagnose_with_vision_ai(image_path: str) -> str:
    if not vision_model:
        return "AI Vision model is not available. Please check server configuration."
    try:
        img = Image.open(image_path)
        prompt = (
            "You are an expert agriculturalist. Analyze this image of a plant leaf. "
            "Identify any disease or pest. If it's healthy, say so. "
            "Provide a short, clear diagnosis and a suggested remedy. "
            "Format the response as: 'Diagnosis: [Your Diagnosis]. Suggested Remedy: [Your Remedy].' "
            "Disclaimer: This is an AI suggestion. Consult a local expert."
        )
        response = vision_model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        return "The advanced AI analysis failed. Please ensure the image is clear."

def diagnose_from_url(image_url: str) -> str:
    if not model:
        return "Error: The primary diagnosis model is not loaded. Please check server logs."
    
    try:
        response = requests.get(
            image_url,
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        )
        response.raise_for_status()
        temp_dir = os.getenv("TEMP_DIR", "/tmp") 
        os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, f"{uuid.uuid4()}.jpg")
        with open(image_path, "wb") as f: f.write(response.content)
    except Exception as e:
        print(f"Image Download Error: {e}")
        return "Could not download the image from the provided URL. Please try again."

    try:
        img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE), color_mode='rgb')
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        processed_image = preprocess_input(img_array)
        predictions = model.predict(processed_image, verbose=0)
        
        confidence = np.max(predictions[0])
        class_name = CLASS_NAMES[np.argmax(predictions[0])]
        
        CONFIDENCE_THRESHOLD = 0.50
        
        if confidence >= CONFIDENCE_THRESHOLD:
            print(f"--- High Confidence Diagnosis ({confidence:.1%}) from Local Model ---")
            
            is_healthy = class_name in HEALTHY_CLASSES
            diagnosis = class_name.replace('_', ' ')
            os.remove(image_path)

            if is_healthy:
                return (
                    f"✅ *Diagnosis:* Healthy\n\n"
                    f"Looks like a healthy {diagnosis}.\n\n"
                    f"- *Recommendation:* Your plant appears healthy. Continue to monitor for pests and ensure proper watering.\n"
                    f"_(Model Confidence: {confidence:.1%})_"
                )
            else:
                remedy = REMEDY_KNOWLEDGE_BASE.get(class_name, DEFAULT_REMEDY)
                return (
                    f"🩺 *Diagnosis:* {diagnosis}\n\n"
                    f"- *Suggested Remedy:* {remedy}\n\n"
                    f"_(Model Confidence: {confidence:.1%})_\n\n"
                    f"```Disclaimer: This is an AI suggestion. Always consult a local expert.```"
                )
        else:
            print(f"--- Low Confidence ({confidence:.1%}). Falling back to Gemini Vision AI. ---")
            vision_result = diagnose_with_vision_ai(image_path)
            os.remove(image_path)
            return vision_result

    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        print(f"Prediction Error: {e}")
        return "Could not process the image. Please try sending a clear photo of a single leaf."
