"""Clasificador de comandos.

Determina si un comando es una **primitiva** (verbo registrado) o un
**paquete** (id definido en YAML), y su tipo de ejecución
(instantánea o programada).

Orden de evaluación:
    1. Si tokens[0] == PREFIJO_PAQUETE → busca " ".join(tokens[1:]) como id
    2. Si la frase completa está en nombres_paquetes → paquete
    3. Si tokens[0] está en VERBOS["es"] → primitiva
    4. fallback a LLM (Ollama) para lenguaje natural → primitiva si reconoce
    5. Si nada coincide → ErrorAgente(CMD_DESCONOCIDO)
"""

from src.models import ErrorAgente
from src.config.constants import VERBOS, PREFIJO_PAQUETE
from src.config import config as _config
from src.llm import interpreter as _llm
from src.interpreter import tokenizer as _tokenizer

STOPWORDS = {
    "ponme", "pon", "activa", "inicia", "ejecuta", "abre",
    "en", "a", "el", "la", "los", "las", "un", "una",
    "de", "del", "al", "con", "para", "por", "y", "o"
}


def _match_paquete(texto: str, nombres_paquetes: set[str]) -> str | None:
    palabras_usuario = set(texto.lower().split()) - STOPWORDS
    if not palabras_usuario:
        return None

    mejor = None
    mejor_score = 0

    for nombre in nombres_paquetes:
        palabras_paquete = set(nombre.replace("_", " ").split())
        score = len(palabras_usuario & palabras_paquete)
        if score > mejor_score:
            mejor_score = score
            mejor = nombre

    return mejor if mejor_score > 0 else None


def clasificar(
    tokens: list[str],
    nombres_paquetes: set[str],
    texto_original: str = "",
) -> tuple[str, str, list[str]] | ErrorAgente:
    idioma = _config.obtener_setting("idioma", "es")
    verbos = VERBOS[idioma]
    if not tokens:
        return ErrorAgente(
            codigo="CMD_VACIO",
            origen="interpreter/classifier",
            detalle="No escribiste ningún comando.",
            accion=None,
        )

    if tokens[0] == PREFIJO_PAQUETE:
        id_paquete = " ".join(tokens[1:])
        if id_paquete in nombres_paquetes:
            return ("paquete", "instantanea", [id_paquete])

        id_normalizado = id_paquete.replace(" ", "_")
        if id_normalizado in nombres_paquetes:
            return ("paquete", "instantanea", [id_normalizado])

        match = _match_paquete(id_paquete, nombres_paquetes)
        if match:
            return ("paquete", "instantanea", [match])

        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/classifier",
            detalle=f"Paquete '{id_paquete}' no existe.",
            accion=None)

    frase_completa = " ".join(tokens)
    if frase_completa in nombres_paquetes:
        return ("paquete", "instantanea", tokens)

    match = _match_paquete(frase_completa, nombres_paquetes)
    if match:
        tokens_match = [PREFIJO_PAQUETE] + match.split("_")
        return ("paquete", "instantanea", [match])

    token = tokens[0]
    if token in verbos:
        return ("primitiva", "instantanea", tokens)

    if texto_original:
        comando_llm = _llm.interpretar(texto_original)
        if comando_llm == "desconocido":
            return ErrorAgente(
                codigo="CMD_DESCONOCIDO",
                origen="interpreter/classifier",
                detalle=f"El comando '{texto_original}' no existe.",
                accion=None)

        tokens_llm = _tokenizer.dividir(comando_llm)
        if tokens_llm and tokens_llm[0] in verbos:
            return ("primitiva", "instantanea", tokens_llm)

        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/classifier",
            detalle=f"El comando '{tokens_llm[0] if tokens_llm else texto_original}' no existe.",
            accion=None)

    return ErrorAgente(
        codigo="CMD_DESCONOCIDO",
        origen="interpreter/classifier",
        detalle=f"El comando '{token}' no existe.",
        accion=None,
    )
