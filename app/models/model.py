from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Multilingual zero-shot classifier (XNLI backbone -> supports ~100 languages)
# Note: first run will download model weights (~1.2GB) 
CLASSIFIER_MODEL_NAME = "joeddav/xlm-roberta-large-xnli"

# initialize pipeline once (costly)
try:
    classifier = pipeline("zero-shot-classification", model=CLASSIFIER_MODEL_NAME)
except Exception as e:
    logger.exception("Failed to initialize transformer pipeline. Make sure transformers and torch are installed.")
    classifier = None

# two labels we want to distinguish
LABELS = ["real", "fake"]

def predict_text(text: str):
    """
    Returns: (mapped_label, confidence) where mapped_label in {"real","fake","unverified"}
    """
    if classifier is None:
        # graceful fallback
        return "unverified", 0.0

    # use the pipeline
    out = classifier(text, LABELS)
    # out: dict with 'labels' and 'scores'
    top_label = out["labels"][0]
    top_score = float(out["scores"][0])
    # map label (pipeline could return the labels as we passed them)
    mapped = top_label.lower()
    # safety: if top_score is very low, mark as unverified
    if top_score < 0.45:
        return "unverified", top_score
    return mapped, top_score
