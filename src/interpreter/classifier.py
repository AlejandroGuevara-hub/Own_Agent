"""Clasificador de comandos.

Determina si un comando es una **primitiva** (verbo registrado) o un
**paquete** (palabra clave definida en YAML), y su tipo de ejecución
(instantánea o programada).
"""

from src.models import ErrorAgente
from src.config.constants import VERBOS


def clasificar(
    tokens: list[str],
    nombres_paquetes: set[str],
) -> tuple[str, str] | ErrorAgente:
    if not tokens:
        return ErrorAgente(
            codigo="CMD_VACIO",
            origen="interpreter/classifier",
            detalle="No escribiste ningún comando.",
            accion=None,
        )

    frase_completa = " ".join(tokens)
    if frase_completa in nombres_paquetes:
        return ("paquete", "instantanea")

    token = tokens[0]
    if token in VERBOS["es"]:
        return ("primitiva", "instantanea")

    return ErrorAgente(
        codigo="CMD_DESCONOCIDO",
        origen="interpreter/classifier",
        detalle=f"El comando '{token}' no existe.",
        accion=None,
    )
