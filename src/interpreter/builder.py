from src.models import Intencion, Accion, ErrorAgente
from src.config.constants import VERBOS_A_PRIMITIVA, VERBOS_AMBIGUOS
from src.config import config


def construir(
    tokens: list[str],
    tipo: str,
    ejecucion: str,
) -> Intencion | ErrorAgente:
    """Construye el objeto Intencion a partir de los tokens clasificados."""
    if not tokens:
        return ErrorAgente(
            codigo="CMD_VACIO",
            origen="interpreter/builder",
            detalle="No escribiste ningún comando.",
            accion=None,
        )

    verbo = tokens[0]

    if verbo not in VERBOS_A_PRIMITIVA:
        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/builder",
            detalle=f"El comando '{verbo}' no existe.",
            accion=None,
        )

    id_primitiva = VERBOS_A_PRIMITIVA[verbo]

    if id_primitiva is None:
        if len(tokens) < 2 or tokens[1] not in VERBOS_AMBIGUOS.get(verbo, {}):
            opciones = list(VERBOS_AMBIGUOS.get(verbo, {}).keys())
            return ErrorAgente(
                codigo="PARAM_INVALIDO",
                origen="interpreter/builder",
                detalle=f"'{verbo}' necesita especificar: {opciones}",
                accion=None,
            )
        id_primitiva = VERBOS_AMBIGUOS[verbo][tokens[1]]
        args = tokens[2:]
    else:
        args = tokens[1:]

    primitiva = config.obtener_primitiva(id_primitiva)
    if primitiva is None:
        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/builder",
            detalle=f"Primitiva '{id_primitiva}' no definida en YAML.",
            accion=None,
        )

    accion_yaml = primitiva["acciones"][0]

    if accion_yaml["objetivo"] == "":
        objetivo = tokens[1] if len(tokens) > 1 else ""
    else:
        objetivo = accion_yaml["objetivo"]

    accion = Accion(
        tipo=accion_yaml["tipo"],
        objetivo=objetivo,
        args=args,
    )

    return Intencion(
        id=id_primitiva,
        tipo=tipo,
        ejecucion=ejecucion,
        schedule=None,
        acciones=[accion],
    )
