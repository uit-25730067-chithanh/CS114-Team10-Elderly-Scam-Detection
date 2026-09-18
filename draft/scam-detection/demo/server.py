"""
Production FastAPI Application Server for Civic Guard Elder Scam Detection.
Direct integration with XGBoost ML model (5,015 features) and modern client UI.
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add current demo directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from components.model_adapter import get_detector
from components.sample_data import SAMPLE_MESSAGES
from components.keyword_highlighter import SCAM_KEYWORDS, PSYCHOLOGICAL_INDICATORS

app = FastAPI(
    title="Civic Guard Scam SMS Detection Portal",
    description="Production-grade public safety API for elder fraud prevention",
    version="2.4.0"
)

detector = get_detector()

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    text: str
    risk_score: float
    is_scam: bool
    status_label: str
    theme_color: str
    matched_keywords: list[str]
    detected_indicators: list[dict]

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "model_ready": detector.is_ready,
        "model_name": detector.model_name
    }

@app.get("/api/samples")
def get_samples():
    return SAMPLE_MESSAGES

@app.post("/api/predict", response_model=PredictionResponse)
def predict_sms(req: PredictionRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung tin nhắn.")

    res = detector.predict(text)
    risk_score = res["risk_score"]
    is_scam = res["is_scam"]

    # Match keywords
    lower = text.lower()
    matched_kw = [k for k in SCAM_KEYWORDS if k in lower]

    # Match psychological indicators
    matched_ind = []
    for item in PSYCHOLOGICAL_INDICATORS:
        found = [k for k in item["keywords"] if k in lower]
        if found:
            matched_ind.append({
                "label": item["label"],
                "keywords": found[:3]
            })

    if risk_score >= 0.70:
        status_label = "MỨC ĐỘ NGUY HIỂM CAO (LỪA ĐẢO)"
        theme_color = "#DC2626"
    elif risk_score >= 0.35:
        status_label = "CẦN LƯU Ý XÁC MINH (NGHI VẤN)"
        theme_color = "#D97706"
    else:
        status_label = "AN TÂM (TIN NHẮN BÌNH THƯỜNG)"
        theme_color = "#16A34A"

    return PredictionResponse(
        text=text,
        risk_score=risk_score,
        is_scam=is_scam,
        status_label=status_label,
        theme_color=theme_color,
        matched_keywords=matched_kw,
        detected_indicators=matched_ind
    )

# Static directory
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8503, reload=False)
