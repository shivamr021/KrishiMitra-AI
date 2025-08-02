import tensorflow as tf
import numpy as np
from keras.utils import load_img, img_to_array
# --- Add imports needed to rebuild the model ---
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Sequential

# --- Constants ---
# We go back to using the .h5 file, as we are only loading its weights
MODEL_PATH = 'model/saved_model/krishi_pest_model.h5'
IMG_SIZE = 224
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 
    'Apple___healthy', 'Blueberry___healthy', 'Cherry___Powdery_mildew', 
    'Cherry___healthy', 'Corn___Cercospora_leaf_spot Gray_leaf_spot', 
    'Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy', 
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

# --- Function to create the model architecture ---
def create_model_architecture(num_classes):
    """Rebuilds the exact same model architecture we used for training."""
    base_model = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3),
                             include_top=False,
                             weights='imagenet') # Weights are needed for the architecture but won't be used
    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    return model

# --- UPDATED MODEL LOADING LOGIC ---
try:
    # 1. Create a new instance of the model architecture
    model = create_model_architecture(num_classes=len(CLASS_NAMES))
    # 2. Load only the learned weights into this new model
    model.load_weights(MODEL_PATH)
except Exception as e:
    print(f"Error loading model weights: {e}")
    model = None


def diagnose_plant_disease(image_path):
    """
    Takes an image file path, preprocesses it, and returns the predicted disease name
    along with the model's confidence.
    """
    if model is None:
        return "Model not loaded. Please check server logs."
    try:
        img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        predictions = model.predict(img_array)
        
        prediction_confidence = np.max(predictions[0])
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        return f"Diagnosis: **{predicted_class_name}** (Confidence: {prediction_confidence:.1%})"

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Could not process the image. Please try another one."