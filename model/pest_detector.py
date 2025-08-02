import tensorflow as tf
import numpy as np
from keras.utils import load_img, img_to_array

# --- Constants ---
# Define the path to your saved model
MODEL_PATH = 'model/saved_model/krishi_pest_model.h5'
IMG_SIZE = 224

# CRITICAL: You must replace this with the full list of 38 class names
# from your Colab notebook (the `class_names` variable).
# The order MUST be exactly the same.
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry___Powdery_mildew',
    'Cherry___healthy',
    'Corn___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn___Common_rust',
    'Corn___Northern_Leaf_Blight',
    'Corn___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]


# --- Load the Model ---
# We load the model once when the script is first imported for efficiency.
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


def diagnose_plant_disease(image_path):
    """
    Takes an image file path, preprocesses it, and returns the predicted disease name.
    
    Args:
        image_path: Path to the uploaded image file.

    Returns:
        A string containing the predicted class name, or an error message.
    """
    if model is None:
        return "Model not loaded. Please check server logs."

    try:
        # Load and preprocess the image
        img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create a batch
        img_array /= 255.0  # Normalize to [0,1]

        # Make a prediction
        predictions = model.predict(img_array)
        
        # Get the class with the highest probability
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        return predicted_class_name

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Could not process the image. Please try another one."