from pydantic import BaseModel
from typing import Optional, Dict

class AnalyzeRequest(BaseModel):
    text: str
    # optional hint about where the text came from (whatsapp, tweet, news, social, unknown)
    source: Optional[str] = "unknown"
    # optional language hint (auto by default)
    lang: Optional[str] = "auto"

class AnalyzeResponse(BaseModel):
    prediction: str
    confidence: float
    credibility_score: int
    verdict: str
    explain: str
    components: Dict[str, float]
