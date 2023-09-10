import spacy

class SectorExtractor:
    def __init__(self, model_path="en_core_web_sm"):
        # Load the spaCy language model
        self.nlp = spacy.load(model_path)

    def extract_sector_subsector(self, text):
        # Process the text with spaCy
        doc = self.nlp(text)

        # Initialize variables to store sector and subsector
        sector = None
        subsector = None

        # Define keywords that may indicate the start of the subsector
        subsector_start_keywords = ["in", "for", "at", "to", "with", "by", "of"]

        # Iterate through tokens in the text
        for token in doc:
            if token.ent_type_ == "ORG" and not sector:
                # Check if the organization is a suitable sector
                sector = token.text
            elif token.ent_type_ != "ORG":
                # Check if the token is in the subsector_start_keywords
                if token.text.lower() in subsector_start_keywords:
                    # Look for subsector in the following tokens
                    subsector_tokens = []
                    for next_token in token.doc[token.i + 1:]:
                        if next_token.ent_type_ == "ORG":
                            break
                        subsector_tokens.append(next_token.text)
                    subsector = " ".join(subsector_tokens)

        return sector, subsector
