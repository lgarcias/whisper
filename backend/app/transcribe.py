import os
import json
from typing import Literal, Optional, Dict, Any, cast
from .config import settings
from .storage import new_job_dir

Engine = Literal["openai", "faster"]
Device = Literal["auto", "cpu", "cuda"]


def pick_device(requested: Device) -> str:
    if requested == "cuda":
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"
    if requested == "auto":
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"
    return "cpu"


def transcribe_job(audio_path: str,
                   engine: Engine = cast(Engine, settings.DEFAULT_ENGINE),
                   model: str = settings.DEFAULT_MODEL,
                   device: Device = cast(Device, settings.DEFAULT_DEVICE),
                   task: Literal["transcribe", "translate"] = "transcribe",
                   language: Optional[str] = None,
                   compute_type: str = settings.DEFAULT_COMPUTE,
                   job_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Run transcription and save results under {TRANSCRIPTS_DIR}/{job_id}.
    Returns metadata and result file paths.
    """
    dev = pick_device(device)
    job_id = job_id or "manual"
    outdir = new_job_dir(job_id)

    text = ""
    segments_serializable = []

    if engine == "faster":
        from faster_whisper import WhisperModel
    # If dev == 'cuda', use float16 (or provided compute_type); on CPU default to int8
        ct = compute_type if dev == "cuda" else "int8"
        model_obj = WhisperModel(model, device=dev, compute_type=ct)
        segments, info = model_obj.transcribe(
            audio_path, task=task, language=language)
        for s in segments:
            segments_serializable.append({
                "start": float(s.start),
                "end": float(s.end),
                "text": s.text
            })
        text = "".join(s["text"] for s in segments_serializable)
        detected_lang = getattr(info, "language", None)
    else:
        import whisper
        m = whisper.load_model(model)
        if dev == "cuda":
            m = m.to("cuda")
        result: Dict[str, Any] = m.transcribe(
            audio_path, task=task, language=language)
        text = result.get("text", "")
        detected_lang = result.get("language")
    # Normalize segments
        for s in result.get("segments", []):
            segments_serializable.append({
                "start": float(s.get("start", 0.0)),
                "end": float(s.get("end", 0.0)),
                "text": s.get("text", "")
            })

    # Save output files
    txt_path = os.path.join(outdir, "transcript.txt")
    json_path = os.path.join(outdir, "result.json")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "engine": engine,
            "device": dev,
            "model": model,
            "task": task,
            "language": language or detected_lang,
            "text": text.strip(),
            "segments": segments_serializable
        }, f, ensure_ascii=False, indent=2)

    return {
        "engine": engine,
        "device": dev,
        "model": model,
        "task": task,
        "language": language or detected_lang,
        "text_path": txt_path,
        "json_path": json_path,
        "outdir": outdir
    }
