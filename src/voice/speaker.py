"""Síntesis de voz con pyttsx3."""

import pyttsx3

_engine: pyttsx3.Engine | None = None
_VOCES: dict[str, str] = {
    "es": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0",
    "en": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0",
}


def _obtener_engine() -> pyttsx3.Engine:
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine


def voces_disponibles() -> list[dict]:
    engine = _obtener_engine()
    return [
        {"id": v.id, "nombre": v.name, "idiomas": v.languages}
        for v in engine.getProperty("voices")
    ]


def hablar(texto: str, idioma: str = "es") -> None:
    """Reproduce el texto por los altavoces.

    Args:
        texto: Texto a sintetizar.
        idioma: Código ISO del idioma (``"es"``, ``"en"``).
    """
    engine = _obtener_engine()
    voz = _VOCES.get(idioma)
    if voz:
        engine.setProperty("voice", voz)
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 0.9)
    engine.say(texto)
    engine.runAndWait()
