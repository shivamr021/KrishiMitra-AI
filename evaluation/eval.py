import tensorflow as tf
import numpy as np
import json

from pathlib import Path

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from keras.applications.efficientnet import preprocess_input


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "backend/model/saved_model/krishi_multicrop_model.keras"
)

CLASS_PATH = (
    BASE_DIR
    / "backend/model/class_names.json"
)

TEST_DIR = (
    BASE_DIR
    / "evaluation/test"
)

IMG_SIZE = 224


# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading model...\n")

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

print("Model loaded successfully.")
print(f"Classes Loaded: {len(class_names)}")


# =========================================================
# IMAGE PREDICTION FUNCTION
# =========================================================

def predict_image(image_path):

    img = tf.keras.utils.load_img(
        image_path,
        target_size=(IMG_SIZE, IMG_SIZE)
    )

    img_array = tf.keras.utils.img_to_array(img)

    img_batch = np.expand_dims(img_array, axis=0)

    img_preprocessed = preprocess_input(img_batch)

    prediction = model.predict(
        img_preprocessed,
        verbose=0
    )

    predicted_index = np.argmax(prediction[0])

    confidence = float(np.max(prediction[0]))

    predicted_label = class_names[predicted_index]

    return predicted_label, confidence


# =========================================================
# EVALUATION LOOP
# =========================================================

print("\nStarting evaluation...\n")

y_true = []
y_pred = []

total_images = 0
correct_predictions = 0

for class_dir in TEST_DIR.iterdir():

    if not class_dir.is_dir():
        continue

    true_label = class_dir.name

    print(f"\nEvaluating Class: {true_label}")

    for image_path in class_dir.glob("*"):

        if image_path.suffix.lower() not in [
            ".jpg",
            ".jpeg",
            ".png"
        ]:
            continue

        try:

            predicted_label, confidence = predict_image(
                image_path
            )

            y_true.append(true_label)
            y_pred.append(predicted_label)

            total_images += 1

            is_correct = predicted_label == true_label

            if is_correct:
                correct_predictions += 1

            status = "CORRECT" if is_correct else "WRONG"

            print(
                f"{status} | "
                f"{image_path.name} | "
                f"Predicted: {predicted_label} | "
                f"Confidence: {confidence * 100:.2f}%"
            )

        except Exception as e:

            print(
                f"ERROR processing "
                f"{image_path.name}: {e}"
            )


# =========================================================
# FINAL METRICS
# =========================================================

print("\n" + "=" * 60)
print("FINAL EVALUATION RESULTS")
print("=" * 60)

accuracy = accuracy_score(y_true, y_pred)

print(f"\nTotal Images Evaluated: {total_images}")

print(f"Correct Predictions: {correct_predictions}")

print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:\n")

print(
    classification_report(
        y_true,
        y_pred
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_true,
        y_pred
    )
)

print("\nEvaluation Complete.\n")
