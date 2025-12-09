from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
import logging
from app.detector import DeepfakeDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SOC Deepfake Guard API",
    description="AI-powered deepfake audio detection for SOC alert triage",
    version="0.1.0"
)

# Enable CORS for SOC/SOAR integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

detector = DeepfakeDetector()

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "SOC Deepfake Guard",
        "version": "0.1.0"
    }

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    """Analyze audio file for deepfakes.
    
    Returns SOC-formatted JSON with detection results.
    """
    try:
        # Save uploaded file
        temp_path = UPLOAD_DIR / file.filename
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run detection
        logger.info(f"Analyzing: {file.filename}")
        result = detector.detect(str(temp_path))
        
        # Cleanup
        temp_path.unlink()
        
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )

@app.post("/analyze-url")
async def analyze_url(audio_url: str):
    """Analyze audio from URL (future enhancement)."""
    return {
        "status": "not_implemented",
        "message": "URL analysis coming in v0.2.0"
    }

@app.get("/stats")
async def get_stats():
    """Get detection statistics (for dashboard)."""
    return {
        "total_analyses": 0,
        "deepfakes_detected": 0,
        "avg_confidence": 0.0,
        "model": "MelodyMachine/Deepfake-audio-detection-V2"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
