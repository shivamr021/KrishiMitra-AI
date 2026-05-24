import tensorflow as tf
import numpy as np
import json
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
from keras.applications.efficientnet import preprocess_input

MODEL_PATH = "krishi_multicrop_model.keras"
CLASS_PATH = "class_names.json"
TEST_DIR = "test"

IMG_SIZE = 224

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

y_true = []
y_pred = []

def predict_image(path):

    img = tf.keras.utils.load_img(
        path,
        target_size=(IMG_SIZE, IMG_SIZE)
    )

    arr = tf.keras.utils.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    pred = model.predict(arr, verbose=0)

    return np.argmax(pred[0])

for class_dir in Path(TEST_DIR).iterdir():

    if not class_dir.is_dir():
        continue

    true_label = class_dir.name

    for image_path in class_dir.glob("*"):

        try:

            pred_index = predict_image(image_path)
            pred_label = class_names[pred_index]

            y_true.append(true_label)
            y_pred.append(pred_label)

        except Exception as e:

            print(f"Error processing {image_path}: {e}")

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_true, y_pred))
