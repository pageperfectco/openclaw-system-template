#!/usr/bin/env python3
"""Fast local audio transcription using faster-whisper (CTranslate2).
Usage: python3 transcribe.py <audio_file> [--model base|tiny|small]
"""
import sys
import os
import time
import subprocess
import tempfile

def transcribe(audio_path, model_size="base"):
    # Convert to WAV if not already
    if not audio_path.endswith(".wav"):
        wav_path = tempfile.mktemp(suffix=".wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path],
            capture_output=True, check=True
        )
    else:
        wav_path = audio_path

    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(wav_path, language="en", beam_size=1)
    text = " ".join([s.text.strip() for s in segments])

    # Cleanup temp wav
    if wav_path != audio_path and os.path.exists(wav_path):
        os.unlink(wav_path)

    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: transcribe.py <audio_file> [--model base]", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_size = "base"
    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model_size = sys.argv[idx + 1]
    
    start = time.time()
    result = transcribe(audio_file, model_size)
    elapsed = time.time() - start
    print(result)
    print(f"\n[{elapsed:.1f}s | model: {model_size}]", file=sys.stderr)
