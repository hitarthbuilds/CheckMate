import re
from langdetect import detect, DetectorFactory

# make language detection deterministic
DetectorFactory.seed = 0

def normalize_text(text: str) -> str:
    if not text:
        return text
    t = text.strip()
    # collapse long repeated punctuation
    t = re.sub(r'([!?.,])\1{1,}', r'\1', t)
    # remove excessive whitespace
    t = re.sub(r'\s+', ' ', t)
    return t

def detect_lang(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"
