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
from src.llm import llm as _llm
from src.interpreter import tokenizer as _tokenizer


def clasificar(
    tokens: list[str],
    nombres_paquetes: set[str],
    texto_original: str = "",
) -> tuple[str, str, list[str]] | ErrorAgente:
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
            return ("paquete", "instantanea", tokens)
        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/classifier",
            detalle=f"Paquete '{id_paquete}' no existe.",
            accion=None)

    frase_completa = " ".join(tokens)
    if frase_completa in nombres_paquetes:
        return ("paquete", "instantanea", tokens)

    token = tokens[0]
    if token in VERBOS["es"]:
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
        if tokens_llm and tokens_llm[0] in VERBOS["es"]:
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
