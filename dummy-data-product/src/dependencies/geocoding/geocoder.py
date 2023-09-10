import spacy
import re

class LocationExtractor:
    def __init__(self, model_path="en_core_web_sm"):
        self.nlp = spacy.load(model_path)

    def process_text(self, text):
        # Replace non-alphabet characters with a blank space
        cleaned_text = re.sub(r'[^a-zA-Z ]', ' ', text)
        return cleaned_text.upper()

    def extract_locations(self, text):
        # Process the text
        doc = self.nlp(text)

        # Extract location entities
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        return locations

    def process_and_extract(self, text):
        cleaned_text = self.process_text(text)
        locations = self.extract_locations(cleaned_text)
        return locations
