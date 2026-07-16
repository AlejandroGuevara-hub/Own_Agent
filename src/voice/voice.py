import sounddevice as sd
import numpy as np
import whisper
import pyttsx3
from src.config import config

_modelo_whisper = None
_engine_tts = None

def _cargar_modelos() -> None:
    global _modelo_whisper, _engine_tts
    if _modelo_whisper is None:
        _modelo_whisper = whisper.load_model("tiny")
    if _engine_tts is None:
        _engine_tts = pyttsx3.init()

def escuchar() -> str:
    _cargar_modelos()
    sample_rate = 16000
    umbral = config.obtener_setting("umbral_silencio", 0.01)
    segundos_silencio = config.obtener_setting("segundos_silencio", 2)
    duracion_maxima = config.obtener_setting("duracion_maxima", 30)

    bloques = []
    bloques_silencio = 0
    limite_silencio = int(segundos_silencio * sample_rate / 1024)
    limite_maximo = int(duracion_maxima * sample_rate / 1024)

    with sd.InputStream(samplerate=sample_rate, channels=1,
                        blocksize=1024, dtype="float32") as stream:
        while True:
            bloque, _ = stream.read(1024)
            bloques.append(bloque.copy())
            volumen = np.abs(bloque).mean()
            if volumen < umbral:
                bloques_silencio += 1
            else:
                bloques_silencio = 0
            if bloques_silencio >= limite_silencio:
                break
            if len(bloques) >= limite_maximo:
                break

    audio = np.concatenate(bloques, axis=0).flatten()
    resultado = _modelo_whisper.transcribe(audio, language="es", fp16=False)
    return resultado["text"].strip()

def hablar(texto: str) -> None:
    _cargar_modelos()
    _engine_tts.say(texto)
    _engine_tts.runAndWait()
