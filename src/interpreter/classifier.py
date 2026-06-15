from src.models import ErrorAgente
from src.config.constants import VERBOS


def clasificar(
    tokens: list[str],
    nombres_paquetes: set[str],
) -> tuple[str, str] | ErrorAgente:
    """Identifica si el comando es primitiva o paquete,
    e instantáneo o programado.

    Retorna: ("primitiva" | "paquete", "instantanea" | "programada")
    Si tokens[0] en VERBOS["es"]       → primitiva
    Si tokens[0] en nombres_paquetes   → paquete
    Si ninguno                         → ErrorAgente(CMD_DESCONOCIDO)
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
