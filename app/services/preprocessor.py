import logging
import re
from typing import Dict, List, Tuple

import nltk
from nltk import word_tokenize, pos_tag
from langdetect import detect_langs
import spacy

# Setup
logger = logging.getLogger(__name__)
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """Remove extra spaces and normalize text"""
    return re.sub(r'\s+', ' ', text.strip())


def extract_keywords(text: str) -> List[str]:
    """Extract nouns and verbs using POS tagging (NLTK)"""
    try:
        words = text.split()  # ← avoid using word_tokenize to skip punkt error
        tags = pos_tag(words)
        return [word.lower() for word, tag in tags if tag.startswith("NN") or tag.startswith("VB")]
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}")
        return []



def extract_entities(text: str) -> List[Dict]:
    """Extract named entities with spaCy"""
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char, "confidence": 1.0}
        for ent in doc.ents
    ]


def detect_language(text: str) -> Tuple[str, float]:
    """Detect language using langdetect"""
    try:
        langs = detect_langs(text)
        best = langs[0]
        return best.lang, best.prob
    except Exception:
        return "unknown", 0.0


def generate_paraphrases(text: str) -> List[str]:
    """Placeholder for paraphrasing (currently disabled)"""
    return []  # Replace with actual logic if needed


def preprocess_claim(text: str) -> Dict:
    """Main pipeline to preprocess the input claim"""
    cleaned = clean_text(text)
    lang, confidence = detect_language(cleaned)
    logger.info(f"🗣️ Language: {lang} ({confidence:.2f})")

    keywords = extract_keywords(cleaned)
    logger.info(f"📦 Keywords: {keywords}")

    entities = extract_entities(cleaned)
    logger.info(f"🏷️ Entities: {[e['text'] for e in entities]}")

    paraphrases = generate_paraphrases(cleaned)
    word_count = len(text.split())  # ← replace word_tokenize with split
    sentence_count = len(re.findall(r'[.!?]', cleaned))

    return {
        "original_text": text,
        "cleaned_text": cleaned,
        "detected_language": lang,
        "language_confidence": confidence,
        "entities": entities,
        "keywords": keywords,
        "intent": "general_claim",
        "paraphrases": paraphrases,
        "word_count": word_count,
        "sentence_count": sentence_count
    }
