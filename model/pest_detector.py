import tensorflow as tf
import numpy as np
import json
import os
from keras.utils import load_img, img_to_array
from keras.applications.efficientnet import preprocess_input
# --- Add imports needed to rebuild the model ---
from keras.applications import EfficientNetB0
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Input

# --- Constants ---
MODEL_PATH = 'model/saved_model/krishi_multicrop_model.keras'
CLASS_NAMES_PATH = 'model/class_names.json'
IMG_SIZE = 224

# --- Load Class Names ---
try:
    with open(CLASS_NAMES_PATH, 'r') as f:
        CLASS_NAMES = json.load(f)
except Exception as e:
    print(f"[ERROR] Failed to load class names: {e}")
    CLASS_NAMES = []

# --- Function to build the exact EfficientNetB0 architecture ---
def create_model_architecture(num_classes):
    """
    This must be IDENTICAL to the architecture in your training script,
    minus the data augmentation layers.
    """
    # Define the input layer
    inputs = Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    
    # Load the base model with a blank slate for weights
    base_model = EfficientNetB0(weights=None, include_top=False, input_tensor=inputs)
    
    # Recreate the classifier head
    x = base_model.output
    x = GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = Dense(256, activation='relu', name="dense_256")(x)
    x = Dropout(0.5, name="dropout_layer")(x)
    outputs = Dense(num_classes, activation='softmax', name="output_layer")(x)
    
    # Create the final model
    model = Model(inputs=inputs, outputs=outputs)
    return model

# --- Load Model using the Robust Load Weights Method ---
try:
    # 1. Create the empty architecture
    model = create_model_architecture(num_classes=len(CLASS_NAMES))
    # 2. Load your trained weights into that architecture
    model.load_weights(MODEL_PATH)
    print("✅ Model loaded successfully using the robust load_weights method.")
except Exception as e:
    print(f"CRITICAL ERROR: Failed to build architecture or load weights: {e}")
    model = None

# --- Knowledge Base for Remedies (Tailored to PlantDoc classes) ---
REMEDY_KNOWLEDGE_BASE = {
    "Apple Scab Leaf": "Apply a fungicide containing myclobutanil or captan. Prune infected areas and ensure good air circulation.",
    "Apple leaf": "Your apple plant appears healthy. Continue to monitor for pests and ensure proper watering.",
    "Bell_pepper leaf spot": "Avoid overhead watering. Apply copper-based bactericides preventatively.",
    "Bell_pepper leaf": "Your pepper plant looks healthy! Ensure it gets plenty of sunlight.",
    "Blueberry leaf": "Your blueberry plant appears healthy. Maintain acidic soil conditions for best results.",
    "Cherry leaf": "Your cherry plant appears healthy. Watch for common pests like aphids.",
    "Corn Gray leaf spot": "Use resistant hybrids and practice crop rotation. Fungicides may be necessary in severe cases.",
    "Corn leaf blight": "Remove infected plant debris after harvest. Use resistant corn varieties.",
    "Corn rust leaf": "Plant resistant hybrids. Apply a suitable fungicide if the infection occurs early.",
    "Peach leaf": "Your peach plant appears healthy. Ensure proper pruning during the dormant season.",
    "Potato leaf early blight": "Prune lower leaves, apply mulch, and use a fungicide containing mancozeb or chlorothalonil.",
    "Potato leaf late blight": "Immediately remove and destroy affected leaves. Apply a copper-based fungicide. Avoid overhead watering.",
    "Raspberry leaf": "Your raspberry plant appears healthy. Ensure it has good support and air circulation.",
    "Soyabean leaf": "Your soybean crop looks healthy. Monitor for common pests like soybean aphids.",
    "Squash Powdery mildew leaf": "Apply neem oil or a sulfur-based fungicide. Increase air circulation.",
    "Strawberry leaf": "Your strawberry plant appears healthy. Use straw mulch to keep fruit off the soil.",
    "Tomato leaf": "Your tomato plant looks healthy! Keep an eye out for hornworms.",
    "Tomato leaf bacterial spot": "Avoid overhead watering and working with wet plants. Apply copper sprays.",
    "Tomato leaf late blight": "Difficult to control. Remove and destroy infected plants immediately. Use preventative fungicides.",
    "Tomato leaf mosaic virus": "There is no cure. Remove and destroy infected plants to prevent spread. Control insects that may transmit the virus.",
    "Tomato Septoria leaf spot": "Remove infected leaves. Improve air circulation. Use a fungicide containing chlorothalonil.",
    "grape leaf": "Your grape vine appears healthy. Proper pruning is key for a good harvest.",
    "grape leaf black rot": "Prune out and destroy infected parts of the plant. Apply fungicides during the growing season."
    # Add other remedies as needed based on your class_names.json
}
DEFAULT_REMEDY = "Consult a local agricultural expert for specific treatment options."

def diagnose_plant_disease(image_path):
    """
    Diagnoses a plant disease with the correct logic for the PlantDoc dataset's
    class name format (e.g., 'Squash Powdery mildew leaf').
    """
    if model is None or not CLASS_NAMES:
        return "Error: Model or class names are not loaded. Please check server logs."
    
    try:
        # 1. Prediction (This part is working perfectly)
        img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        processed_image = preprocess_input(img_array)
        predictions = model.predict(processed_image)
        
        prediction_confidence = np.max(predictions[0])
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        # --- CORRECTED FORMATTING LOGIC ---
        # The predicted name is the full diagnosis.
        full_diagnosis_name = predicted_class_name.replace('_', ' ')
        remedy = REMEDY_KNOWLEDGE_BASE.get(predicted_class_name, DEFAULT_REMEDY)

        # A simple check to see if the label indicates a healthy plant
        disease_keywords = ['scab', 'rot', 'rust', 'blight', 'spot', 'virus', 'mold', 'mildew']
        is_healthy = not any(keyword in full_diagnosis_name.lower() for keyword in disease_keywords)

        # 2. Format the friendly response
        if is_healthy:
            response = f"""
            Looks like good news!
            - **Plant:** {full_diagnosis_name}
            - **Status:** Healthy
            - **Recommendation:** {remedy}
            *(Confidence: {prediction_confidence:.1%})*
            """
        else:
            response = f"""
            Okay, I've analyzed the image. Here's what I found:
            - **Diagnosis:** {full_diagnosis_name}
            - **Suggested Remedy:** {remedy}
            *(Model Confidence: {prediction_confidence:.1%})*
            
            **Disclaimer:** This is an AI-generated suggestion. Please consult with a local agricultural expert before applying any treatment.
            """
        return response.strip()

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Could not process the image. Please try another one."