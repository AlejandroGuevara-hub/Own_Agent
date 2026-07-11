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
- NUNCA respondas con números solos o respuestas directas
- Si puedes responder la pregunta, tradúcela a: consultar web [pregunta]
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
"hazme una alarma para las 08:31"         → programar alarma 08:31 alarma
"ponme una alarma a las 9"                → programar alarma 09:00 alarma
"recuérdame algo a las 10:30"             → programar recordatorio 10:30 lun,mar,mie,jue,vie mensaje
"programa una alarma para las 08:31"      → programar alarma 08:31 alarma
"programa un recordatorio para las 08:32" → programar recordatorio 08:32 lun,mar,mie,jue,vie mensaje
"recarga la config"         -> recargar config
"recarga config"            -> recargar config
"creame un archivo hola.txt en C:/carpeta"     → crear C:/carpeta/hola.txt
"crea un archivo llamado test.py en C:/codigo" → crear C:/codigo/test.py
"crea el archivo notas.txt en el escritorio"   → crear C:/Users/diego/Desktop/notas.txt
"creame un archivo"                            → DESCONOCIDO
"consulta qué es Python"     → consultar web qué es Python
"busca información sobre IA" → consultar web inteligencia artificial
"qué es machine learning"    → consultar web machine learning
"cual es el mejor ejercicio para pecho"  → consultar web mejor ejercicio pecho
"investiga quien es juan wagner"         → consultar web quien es juan wagner
"investiga en la web sobre Python"       → consultar web Python
"busca quien es Elon Musk"               → consultar web quien es Elon Musk
"qué es la fotosíntesis"                 → consultar web fotosíntesis
"cuantos centimetros son un pie"         → consultar web cuantos centimetros son un pie
"cómo funciona un motor"                 → consultar web cómo funciona un motor
"cuantos mililitros son un litro"     → consultar web cuantos mililitros son un litro
"cuanto es 100 grados fahrenheit"     → consultar web conversion 100 grados fahrenheit celsius
"cuanto es una milla en kilometros"   → consultar web cuantos kilometros es una milla"""


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

    try:
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
    except Exception:
        return "desconocido"
