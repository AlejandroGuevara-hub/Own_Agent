"""Constructor de objetos ``Intencion``.

Transforma los tokens ya clasificados en el contrato de datos que el
executor entiende. Resuelve verbos ambiguos (ej. ``consultar`` →
``consultar_sistema`` vs ``consultar_web``) y completa argumentos
dinámicos desde los tokens.
"""

from src.models import Intencion, Accion, ErrorAgente
from src.config.constants import VERBOS_A_PRIMITIVA, VERBOS_A_PRIMITIVA_EN, VERBOS_AMBIGUOS, VERBOS_AMBIGUOS_EN
from src.config import config


def construir(
    tokens: list[str],
    tipo: str,
    ejecucion: str,
) -> Intencion | ErrorAgente:
    """Construye el objeto ``Intencion`` a partir de los tokens clasificados.
    

    Flujo interno:
        1. Obtiene el id de primitiva desde ``VERBOS_A_PRIMITIVA``.
        2. Si el verbo es ambiguo (mapea a ``None``), resuelve con
           ``VERBOS_AMBIGUOS`` usando ``tokens[1]`` como desambiguador.
        3. Recupera la definición YAML de la primitiva vía ``config.obtener_primitiva``.
        4. Si la acción YAML tiene ``objetivo: ""``, lo reemplaza con
           el primer argumento del usuario (comandos como ``abrir``).
        5. Construye el objeto ``Accion`` y lo envuelve en ``Intencion``.

    Args:
        tokens: Lista de tokens completa (verbo + argumentos).
        tipo: Tipo de comando (``"primitiva"`` o ``"paquete"``).
        ejecucion: Modalidad de ejecución (``"instantanea"`` o ``"programada"``).

    Returns:
        Objeto ``Intencion`` listo para ejecutar, o ``ErrorAgente`` si
        el verbo no está registrado o los parámetros son inválidos.

    Errors:
        CMD_VACIO: Si no hay tokens.
        CMD_DESCONOCIDO: Si el verbo no está en ``VERBOS_A_PRIMITIVA``
            o la primitiva no existe en YAML.
        PARAM_INVALIDO: Si un verbo ambiguo no tiene suficientes tokens
            para desambiguar.
    """
    idioma = config.obtener_setting("idioma", "es")
    verbos_a_primitiva = VERBOS_A_PRIMITIVA_EN if idioma == "en" else VERBOS_A_PRIMITIVA
    verbos_ambiguos = VERBOS_AMBIGUOS_EN if idioma == "en" else VERBOS_AMBIGUOS
    if not tokens:
        return ErrorAgente(
            codigo="CMD_VACIO",
            origen="interpreter/builder",
            detalle="No escribiste ningún comando.",
            accion=None,
        )

    if tipo == "paquete":
        paquetes = config.obtener_paquetes()

        id_busqueda = tokens[0]
        paquete = paquetes.get(id_busqueda)

        if paquete is None and len(tokens) > 1:
            id_busqueda = " ".join(tokens[1:])
            paquete = paquetes.get(id_busqueda)

        if paquete is None:
            id_busqueda = " ".join(tokens)
            paquete = paquetes.get(id_busqueda)

        if paquete is None:
            return ErrorAgente(
                codigo="CMD_DESCONOCIDO",
                origen="interpreter/builder",
                detalle=f"Paquete '{tokens}' no encontrado.",
                accion=None)

        acciones = []
        for accion_yaml in paquete["acciones"]:
            acciones.append(Accion(
                tipo=accion_yaml["tipo"],
                objetivo=accion_yaml["objetivo"],
                args=accion_yaml.get("args", []),
                confirmacion=False,
            ))

        return Intencion(
            id=paquete["id"],
            tipo=tipo,
            ejecucion=ejecucion,
            schedule=None,
            acciones=acciones,
        )

    verbo = tokens[0]

    if verbo not in verbos_a_primitiva:
        return ErrorAgente(
            codigo="CMD_DESCONOCIDO",
            origen="interpreter/builder",
            detalle=f"El comando '{verbo}' no existe.",
            accion=None,
        )

    id_primitiva = verbos_a_primitiva[verbo]

    if id_primitiva is None:
        if len(tokens) < 2 or tokens[1] not in verbos_ambiguos.get(verbo, {}):
            opciones = list(verbos_ambiguos.get(verbo, {}).keys())
            return ErrorAgente(
                codigo="PARAM_INVALIDO",
                origen="interpreter/builder",
                detalle=f"'{verbo}' necesita especificar: {opciones}",
                accion=None,
            )
        id_primitiva = verbos_ambiguos[verbo][tokens[1]]
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

    confirmacion = primitiva.get("guard") == "confirmar"
    accion = Accion(
        tipo=accion_yaml["tipo"],
        objetivo=objetivo,
        args=args,
        confirmacion=confirmacion,
    )

    return Intencion(
        id=id_primitiva,
        tipo=tipo,
        ejecucion=ejecucion,
        schedule=None,
        acciones=[accion],
    )
