#!/usr/bin/env python3
"""Generate test audio files for SOC Deepfake Guard testing."""

import numpy as np
import soundfile as sf
from pathlib import Path
import argparse

def generate_sine_wave(duration: float = 3.0, frequency: float = 440, sr: int = 16000) -> np.ndarray:
    """Generate pure sine wave audio."""
    t = np.linspace(0, duration, int(sr * duration))
    audio = np.sin(2 * np.pi * frequency * t) * 0.3
    return audio.astype(np.float32)

def generate_noise_audio(duration: float = 3.0, sr: int = 16000) -> np.ndarray:
    """Generate white noise audio."""
    samples = int(sr * duration)
    audio = np.random.normal(0, 0.1, samples).astype(np.float32)
    return audio

def generate_speech_like_audio(duration: float = 3.0, sr: int = 16000) -> np.ndarray:
    """Generate speech-like audio with multiple frequencies."""
    t = np.linspace(0, duration, int(sr * duration))
    # Combine multiple frequencies to simulate speech
    frequencies = [200, 400, 800, 1600]
    audio = np.zeros_like(t)
    for freq in frequencies:
        audio += np.sin(2 * np.pi * freq * t) * 0.1
    # Add amplitude modulation
    env = (np.sin(2 * np.pi * 2 * t) + 1) / 2  # 2 Hz amplitude variation
    audio = audio * env
    return (audio / np.max(np.abs(audio)) * 0.3).astype(np.float32)

def main():
    parser = argparse.ArgumentParser(description="Generate test audio files")
    parser.add_argument(
        "--output-dir",
        default="examples",
        help="Output directory for test audio files"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=3.0,
        help="Duration of audio files in seconds"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Sample rate of audio files"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Generate test audio files
    print("Generating test audio files...")
    
    # 1. Pure sine wave (clean audio)
    sine_audio = generate_sine_wave(args.duration, 440, args.sample_rate)
    sine_path = output_dir / "test_sine_wave.wav"
    sf.write(sine_path, sine_audio, args.sample_rate)
    print(f"✓ Created: {sine_path}")
    
    # 2. White noise
    noise_audio = generate_noise_audio(args.duration, args.sample_rate)
    noise_path = output_dir / "test_noise.wav"
    sf.write(noise_path, noise_audio, args.sample_rate)
    print(f"✓ Created: {noise_path}")
    
    # 3. Speech-like audio
    speech_audio = generate_speech_like_audio(args.duration, args.sample_rate)
    speech_path = output_dir / "test_speech_like.wav"
    sf.write(speech_path, speech_audio, args.sample_rate)
    print(f"✓ Created: {speech_path}")
    
    # 4. Complex audio (combined)
    complex_audio = 0.5 * sine_audio + 0.3 * noise_audio + 0.2 * speech_audio
    complex_audio = (complex_audio / np.max(np.abs(complex_audio))).astype(np.float32)
    complex_path = output_dir / "test_complex.wav"
    sf.write(complex_path, complex_audio, args.sample_rate)
    print(f"✓ Created: {complex_path}")
    
    print(f"\n✓ All test audio files generated in '{output_dir}' directory")
    print(f"  Sample rate: {args.sample_rate} Hz")
    print(f"  Duration: {args.duration}s each")
    print(f"\nTest with CLI:")
    print(f"  python cli.py examples/test_sine_wave.wav")
    print(f"  python cli.py examples/test_speech_like.wav")

if __name__ == "__main__":
    main()
