# app/routers/analyze.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Tuple
from transformers import pipeline
from langdetect import detect

router = APIRouter()

# Initialize multilingual NLI pipeline (Hugging Face)
# Automatically downloads the model on first run
classifier = pipeline("text-classification", model="joeddav/xlm-roberta-large-xnli")

# Pydantic request model
class AnalyzeRequest(BaseModel):
    text: str
    source: str  # e.g., "whatsapp", "news", "tweet"

# Pydantic response model
class AnalyzeResponse(BaseModel):
    prediction: str
    confidence: float
    credibility_score: float
    verdict: str
    explain: str
    components: Dict[str, float]

def compute_credibility(confidence: float, source: str) -> float:
    """Combine classifier confidence with source trust to get a credibility score."""
    # Example source weights
    source_weights = {
        "whatsapp": 0.3,
        "tweet": 0.5,
        "news": 0.9,
    }
    weight = source_weights.get(source.lower(), 0.5)
    score = confidence * 100 * weight
    return round(score, 2)

def analyze_text(text: str, source: str) -> Tuple[str, float]:
    """Run NLI classifier and return predicted label and confidence."""
    # Detect language (optional, can be used for logging or preprocessing)
    lang = detect(text)

    results = classifier(text, top_k=1)
    label = results[0]["label"].lower()  # 'entailment', 'contradiction', etc.
    confidence = float(results[0]["score"])

    # Map NLI label to fake/real
    if label in ["contradiction", "neutral"]:
        prediction = "fake"
    else:
        prediction = "real"

    return prediction, confidence

@router.post("/analyze/", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> Any:
    text = request.text
    source = request.source

    prediction, confidence = analyze_text(text, source)
    credibility = compute_credibility(confidence, source)

    if credibility > 70:
        verdict = "Likely True"
    elif credibility > 40:
        verdict = "Possibly False"
    else:
        verdict = "Likely False"

    explanation = f"Prediction: {prediction}, Confidence: {confidence:.2f}, Source weight applied."

    return AnalyzeResponse(
        prediction=prediction,
        confidence=confidence,
        credibility_score=credibility,
        verdict=verdict,
        explain=explanation,
        components={"classifier": confidence, "source": compute_credibility(1.0, source)},
    )
