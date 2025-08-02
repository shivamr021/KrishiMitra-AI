# 🌿 KrishiMitra - AI Assistant for Farmers

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.1-orange.svg)](https://streamlit.io)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19.0-FF6F00.svg)](https://www.tensorflow.org/)

KrishiMitra is a bilingual, AI-powered conversational agent designed to provide small farmers with critical information about market prices, weather forecasts, and real-time plant disease diagnosis.

## ✨ Screenshot

*(Here you should add a high-quality screenshot or an animated GIF of the app in action. This is the most important part of the README.)*

![KrishiMitra Demo](path/to/your/screenshot.png)

## 🎯 Problem Statement & SDG Alignment

This project addresses the critical need for accessible, real-time agricultural information for small farmers, who often lack the resources for timely decision-making. By providing instant diagnoses and data, KrishiMitra directly contributes to:
- **SDG 1: No Poverty**
- **SDG 2: Zero Hunger**
- **SDG 13: Climate Action**

## 🚀 Features

- **🗣️ Bilingual Chat Interface:** Fully functional in both English and Hindi.
- **🔬 Pest Alert Agent:** Upload a photo of a plant leaf and get an instant AI-powered diagnosis with a confidence score.
- **🌦️ Water Management Agent:** Get a simple, real-time weather forecast.
- **📈 Market Price Agent:** Get current market prices for key crops like Soybean and Wheat.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend & ML:** Python, TensorFlow, Keras
- **Key Libraries:** NumPy, Pandas, OpenCV
- **APIs:** OpenWeatherMap (for weather forecast)

## ⚙️ Getting Started

### Prerequisites

- Python 3.11+
- Git

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/shivamr021/KrishiMitra-AI.git](https://github.com/shivamr021/KrishiMitra-AI.git)
    cd KrishiMitra-AI
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # For macOS/Linux
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the following command from the root directory:

```sh
streamlit run app.py

The application will open in your default web browser.

## 👥 Our Team

This project was built as part of the IBM SkillsBuild AI-ML Internship by **Team Code Push Pray**.

| Name               | Role                   | GitHub Profile                                     | LinkedIn Profile                                       |
| ------------------ | ---------------------- | -------------------------------------------------- | ------------------------------------------------------ |
| **Shivam Rathod** | Team Lead / Integrator | [GitHub](https://github.com/shivamr021)    | [LinkedIn](https://www.linkedin.com/in/shivamrathod021/)    |
| **Shatakshi Tiwari**| Co-Lead / CV Lead    | [GitHub](https://github.com/Shatakshi0216) | [LinkedIn](https://www.linkedin.com/in/shatakshitiwari017/)  |
| **Sahil Kukreja** | Co-Lead / Agent Lead   | [GitHub](https://github.com/Sahilkukreja30) | [LinkedIn](https://www.linkedin.com/in/sahil-kukreja-943993289/)  |
| **Sumedha** | Frontend / Jr. Dev     | [their-github-id](https://github.com/their-id)    | [their-linkedin-id](https://linkedin.com/in/their-id)  |
| **Rachit** | Frontend / Jr. Dev     | [their-github-id](https://github.com/their-id)     | [their-linkedin-id](https://linkedin.com/in/their-id)  |
| **Nitika** | Documentation / Jr. Dev| [their-github-id](https://github.com/their-id)     | [their-linkedin-id](https://linkedin.com/in/their-id)  |
| **Pratishta** | Documentation / Jr. Dev| [their-github-id](https://github.com/their-id)  | [their-linkedin-id](https://linkedin.com/in/their-id)  |

## 🙏 Acknowledgments

- **IBM SkillsBuild** for the internship opportunity.
- **PlantVillage Dataset** for providing the data for our disease detection model.
- The developers of **TensorFlow** and **Streamlit**.
