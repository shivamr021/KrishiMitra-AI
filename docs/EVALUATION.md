# Model Evaluation

## Datasets Used

### PlantVillage
- Controlled environment dataset
- Used for initial transfer learning experiments

### PlantDoc
- Real-world crop disease dataset
- Used to improve real-world robustness

---

## Evaluation Goals

The evaluation pipeline focused on:
- prediction consistency
- confidence-based fallback routing
- real-world image handling
- disease classification quality

---

## Key Observations

- PlantVillage achieved high validation accuracy but generalized poorly on real-world farmer images.
- PlantDoc improved robustness under real-world conditions.
- Confidence-threshold routing to Gemini Vision improved handling of uncertain predictions.

---

## Current Limitations

- Low-light images reduce prediction reliability
- Similar fungal diseases may be confused
- Limited support for unseen crop categories

---

## Future Improvements

- Larger multilingual agricultural dataset
- Confidence calibration
- Ensemble inference
- Offline inference optimization
