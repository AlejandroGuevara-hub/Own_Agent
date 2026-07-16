"""Módulo de entrada y salida por voz.

Expone las funciones ``escuchar`` (STT con Whisper) y
``hablar`` (TTS con pyttsx3).
"""

from src.voice.listener import escuchar
from src.voice.speaker import hablar, voces_disponibles

__all__ = ["escuchar", "hablar", "voces_disponibles"]
