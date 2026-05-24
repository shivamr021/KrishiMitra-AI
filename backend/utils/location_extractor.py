import json
import re
import spacy
from core.config import settings

nlp = spacy.load("en_core_web_sm")
INDIAN_CITIES = []
try:
    with open(settings.INDIAN_CITIES_PATH, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            INDIAN_CITIES = [city.lower() for city in data]
except Exception as e:
    print(f"Error loading cities file: {e}")

def extract_location(text: str) -> str | None:
    """Extracts a location (city) from the text."""
    words = re.findall(r'\w+', text.lower())
    for city in INDIAN_CITIES:
        if city in words:
            return city.capitalize()
    
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
            
    return None
