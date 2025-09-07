# CheckMate

Multilingual, real-time fake news detection backend using HuggingFace zero-shot model.

## Features
- Zero-shot classification with `joeddav/xlm-roberta-large-xnli` (multilingual).
- Credibility score (0-100) combining model confidence and source trust.
- FastAPI backend with `/analyze` endpoint.

## Quick run (local)
1. Install dependencies:
```bash
pip install -r requirements.txt
