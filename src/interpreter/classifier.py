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
    """Identifica la categoría del comando y su tipo de ejecución.

    Lógica de clasificación (por orden de evaluación):
        1. Si ``tokens`` está vacío → ``CMD_VACIO``.
        2. Si ``tokens[0]`` está en ``VERBOS["es"]`` → ``("primitiva", "instantanea")``.
        3. Si ``tokens[0]`` está en ``nombres_paquetes`` → ``("paquete", "instantanea")``.
        4. Si no coincide con nada → ``CMD_DESCONOCIDO``.

    Args:
        tokens: Lista de tokens del comando (al menos 1 elemento).
        nombres_paquetes: Conjunto de palabras clave que disparan paquetes.

    Returns:
        Tupla ``(tipo, ejecucion)`` donde:
            - ``tipo``: ``"primitiva"`` o ``"paquete"``
            - ``ejecucion``: ``"instantanea"`` o ``"programada"``
        O un ``ErrorAgente`` si no se pudo clasificar.

    Errors:
        CMD_VACIO: Si la lista de tokens está vacía.
        CMD_DESCONOCIDO: Si el primer token no coincide con nada registrado.
    """
    if not tokens:
        return ErrorAgente(
            codigo="CMD_VACIO",
            origen="interpreter/classifier",
            detalle="No escribiste ningún comando.",
            accion=None,
        )

    token = tokens[0]

    if token in VERBOS["es"]:
        return ("primitiva", "instantanea")

    if token in nombres_paquetes:
        return ("paquete", "instantanea")

    return ErrorAgente(
        codigo="CMD_DESCONOCIDO",
        origen="interpreter/classifier",
        detalle=f"El comando '{token}' no existe.",
        accion=None,
    )
