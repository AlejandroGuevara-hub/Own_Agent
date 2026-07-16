"""Grabación de micrófono y transcripción con Whisper."""

import tempfile
import time
import sounddevice as sd
import numpy as np
import whisper

_modelo: whisper.Whisper | None = None


def _cargar_modelo() -> whisper.Whisper:
    global _modelo
    if _modelo is None:
        _modelo = whisper.load_model("base")
    return _modelo


def escuchar(duracion: int = 5, idioma: str = "es") -> str:
    """Graba audio del micrófono y transcribe con Whisper.

    Args:
        duracion: Segundos de grabación.
        idioma: Código ISO del idioma (``"es"``, ``"en"``).

    Returns:
        Texto transcrito, o cadena vacía si no se detectó voz.
    """
    fs = 16000
    grabacion = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype="float32")
    sd.wait()

    audio = np.squeeze(grabacion)
    if np.max(np.abs(audio)) < 0.01:
        return ""

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        import scipy.io.wavfile as wav
        wav.write(tmp.name, fs, (audio * 32767).astype(np.int16))
        modelo = _cargar_modelo()
        resultado = modelo.transcribe(tmp.name, language=idioma, fp16=False)
        texto = resultado.get("text", "").strip()

    return texto
