# Evaluation Results

## Dataset
- PlantDoc Dataset
- 27 crop disease categories

## Model
- EfficientNetB0
- Transfer Learning
- TensorFlow/Keras

## Validation Accuracy
~47% on real-world PlantDoc validation data.

## Key Observations
- Real-world agricultural images were significantly more challenging than controlled datasets.
- Confidence-based Gemini fallback improved handling of uncertain predictions.
- The system prioritized robustness and practical deployment integration over benchmark-only optimization.

## Failure Cases
- Low-light images
- motion blur
- visually similar fungal diseases
- compressed WhatsApp images
