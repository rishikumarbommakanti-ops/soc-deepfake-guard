# Example Audio Files

This directory contains example audio files for testing the SOC Deepfake Guard detector.

## Generating Test Audio Files

To generate test audio files automatically, run:

```bash
python generate_test_audio.py
```

This will create 4 test WAV files:
- `test_sine_wave.wav` - Pure 440Hz tone (0.3 amplitude)
- `test_noise.wav` - White noise (0.1 amplitude)
- `test_speech_like.wav` - Multi-frequency speech simulation
- `test_complex.wav` - Mixed combination of above

## Testing with CLI

```bash
# Test single file
python cli.py examples/test_sine_wave.wav

# Test all files
python cli.py examples/*.wav

# Save results to JSON
python cli.py examples/test_sine_wave.wav -o results.json
```

## Audio Specifications

All generated test files have:
- **Sample Rate**: 16,000 Hz (16 kHz)
- **Duration**: 3 seconds
- **Format**: WAV (PCM)
- **Bit Depth**: 32-bit float

## Audio Characteristics

| File | Type | Frequency Range | Use Case |
|------|------|-----------------|----------|
| test_sine_wave.wav | Pure tone | 440 Hz | Clean audio baseline |
| test_noise.wav | White noise | Full spectrum | Background noise handling |
| test_speech_like.wav | Multi-freq | 200-1600 Hz | Speech simulation |
| test_complex.wav | Mixed | Full spectrum | Real-world scenario |

## Expected Detection Results

These test files are **NOT real deepfakes** - they are synthetic audio for testing purposes.

Expected output for test files:
- **Sine Wave**: LOW risk (pure tone, unnaturalness detected)
- **Noise**: LOW risk (background pattern)
- **Speech-like**: MEDIUM risk (may trigger on unnatural patterns)
- **Complex**: MEDIUM risk (mixed frequencies)

**Note**: The detector is trained on real deepfake audio. These synthetic test files help verify the pipeline works correctly, but don't represent actual deepfake threats.

## Using Real Audio

To test with real audio files:

```bash
python cli.py path/to/your/audio.wav
```

Supported formats:
- `.wav` (preferred)
- `.mp3`
- `.m4a`
- `.ogg`

## Troubleshooting

### "No such file or directory" error
Make sure you're in the project root directory:
```bash
cd soc-deepfake-guard
python cli.py examples/test_sine_wave.wav
```

### Audio file not recognized
Ensure the file is a valid audio format and 16kHz sample rate. Convert if needed:
```bash
ffmpeg -i input.mp3 -ar 16000 output.wav
```

### First detection is slow
The Hugging Face model (~370MB) is downloaded on first use. Subsequent runs are ~2s per file.

## Creating Custom Test Audio

To generate custom test audio with different parameters:

```bash
python generate_test_audio.py --duration 5 --sample-rate 16000 --output-dir custom_audio
```

Options:
- `--duration`: Length in seconds (default: 3)
- `--sample-rate`: Hz (default: 16000)
- `--output-dir`: Output directory (default: examples)
