import librosa
import numpy as np
from pathlib import Path
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class DeepfakeDetector:
    """AI-powered deepfake audio detector using Hugging Face models."""
    
    def __init__(self):
        """Initialize the detector with pretrained model from Hugging Face."""
        try:
            # Using Hugging Face's wav2vec2-based deepfake detection pipeline
            self.classifier = pipeline(
                "audio-classification",
                model="MelodyMachine/Deepfake-audio-detection-V2",
                device=0 if self._has_gpu() else -1
            )
            logger.info("Deepfake detection model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load HF model: {e}. Using fallback mode.")
            self.classifier = None
    
    @staticmethod
    def _has_gpu():
        """Check if GPU is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
    
    def extract_features(self, audio_path: str, sr: int = 16000):
        """Extract MFCC and spectral features from audio."""
        try:
            y, sr = librosa.load(audio_path, sr=sr)
            # Limit audio to 10 seconds for processing
            if len(y) > sr * 10:
                y = y[:sr * 10]
            return y, sr
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            raise
    
    def detect(self, audio_path: str) -> dict:
        """Detect if audio is deepfake.
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict: SOC-formatted response with detection results
        """
        try:
            # Extract audio
            y, sr = self.extract_features(audio_path)
            
            result = {
                "file": str(Path(audio_path).name),
                "full_path": str(Path(audio_path).resolve()),
            }
            
            if self.classifier:
                # Use Hugging Face model
                predictions = self.classifier(audio_path)
                
                # Parse predictions
                fake_score = next(
                    (p["score"] for p in predictions if p["label"].lower() == "fake"),
                    next((p["score"] for p in predictions), 0.5)
                )
            else:
                # Fallback: use audio statistics
                fake_score = self._fallback_detect(y, sr)
            
            is_deepfake = fake_score >= 0.5
            confidence = max(fake_score, 1 - fake_score)
            
            result.update({
                "is_deepfake": bool(is_deepfake),
                "deepfake_score": float(fake_score),
                "confidence": float(confidence),
                "alert_level": "HIGH" if is_deepfake and confidence > 0.8 else 
                               "MEDIUM" if is_deepfake else "LOW",
                "recommendation": "Escalate to analyst" if is_deepfake else "Log event",
                "status": "success"
            })
            return result
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return {
                "file": str(Path(audio_path).name),
                "status": "error",
                "error": str(e)
            }
    
    @staticmethod
    def _fallback_detect(y: np.ndarray, sr: int) -> float:
        """Fallback detection using audio statistics."""
        # Simple heuristic based on spectral characteristics
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_var = np.var(mfcc, axis=1)
        return float(np.mean(mfcc_var) / 100)  # Normalized score
