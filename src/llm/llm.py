"""Interpretación de lenguaje natural vía Ollama.

Fallback para cuando el classifier no reconoce un comando:
envía el texto del usuario a un modelo local y lo traduce al
formato de comandos del agente.
"""

import ollama

_cache: dict[str, str] = {}

SYSTEM_PROMPT = """Eres un intérprete de comandos para un agente de automatización Windows.
El usuario escribió un comando en lenguaje natural. Tradúcelo al formato exacto del sistema.

FORMATO DE RESPUESTA (obligatorio):
- Todo en minúsculas
- Sin puntos, comas ni caracteres extra
- Máximo: verbo + 1 objetivo + 2 parámetros
- Si no puedes traducir: responde exactamente DESCONOCIDO

VERBOS DISPONIBLES (elige solo uno):
abrir, cerrar, listar, ajustar, crear, mover, eliminar,
programar, esperar, notificar, consultar, subir, bajar, recargar

EJEMPLOS:
"abre firefox"              → abrir firefox.exe
"abre vs code"              → abrir code.exe
"abre el navegador"         → abrir firefox.exe
"abre chrome"               → abrir chrome.exe
"abre el explorador"        → abrir explorer.exe
"abre spotify"              → abrir spotify.exe
"abre youtube en firefox"    → abrir firefox.exe https://youtube.com
"abre youtube"               → abrir firefox.exe https://youtube.com
"oye abre firefox"          → abrir firefox.exe
"pon el volumen al 50"      -> ajustar volumen 50
"cierra el navegador"       -> cerrar firefox.exe
"muéstrame los procesos"    -> listar
"sube el volumen"           -> subir volumen
"baja el volumen"           -> bajar volumen
"sube el sonido"            -> subir volumen
"baja el sonido"            -> bajar volumen
"no entiendo esto"          -> DESCONOCIDO
"recarga la config"         -> recargar config
"recarga config"            -> recargar config"""


def interpretar(texto: str) -> str:
    """Envía el texto del usuario al LLM local y retorna la traducción.

    Los resultados se cachean por clave normalizada (minúsculas + strip)
    para evitar llamadas repetidas al mismo texto.

    Args:
        texto: Texto libre del usuario (ej. ``"abre el navegador"``).

    Returns:
        Comando traducido (ej. ``"abrir firefox.exe"``), o
        ``"desconocido"`` si el LLM no pudo interpretarlo.
    """
    clave = texto.lower().strip()
    if clave in _cache:
        return _cache[clave]

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": texto},
        ],
    )
    resultado = response["message"]["content"].strip().lower()
    _cache[clave] = resultado
    return resultado
