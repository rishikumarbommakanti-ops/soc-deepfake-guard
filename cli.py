#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from app.detector import DeepfakeDetector
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    """CLI for SOC Deepfake Guard."""
    parser = argparse.ArgumentParser(
        description="SOC Deepfake Guard - Audio deepfake detection CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audio_sample.wav
  %(prog)s --output result.json phishing_call.wav
        """
    )
    
    parser.add_argument(
        "audio_path",
        help="Path to audio file to analyze"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save results to JSON file",
        type=str,
        default=None
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    audio_file = Path(args.audio_path)
    if not audio_file.exists():
        print(f"Error: Audio file not found: {args.audio_path}")
        return 1
    
    if not audio_file.suffix.lower() in ['.wav', '.mp3', '.m4a', '.ogg']:
        print(f"Error: Unsupported audio format. Use .wav, .mp3, .m4a, or .ogg")
        return 1
    
    # Run detection
    print(f"Analyzing: {audio_file.name}")
    detector = DeepfakeDetector()
    result = detector.detect(str(audio_file))
    
    # Output results
    if result.get("status") == "success":
        print("\n=== Detection Results ===")
        print(f"File: {result['file']}")
        print(f"Deepfake Score: {result['deepfake_score']:.2%}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Alert Level: {result['alert_level']}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Is Deepfake: {'YES' if result['is_deepfake'] else 'NO'}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        
        return 0 if not result['is_deepfake'] else 2
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        return 1

if __name__ == "__main__":
    exit(main())
