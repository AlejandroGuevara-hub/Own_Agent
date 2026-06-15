from src.models import Intencion, Accion, ErrorAgente
from src.executor import processes, dispatcher


def ejecutar(intencion: Intencion) -> str | ErrorAgente:
    """Itera las acciones de la Intencion. Detiene en el primer error (fail-fast)."""
    for accion in intencion.acciones:
        resultado = _ejecutar_accion(accion)
        if isinstance(resultado, ErrorAgente):
            return resultado
    return "OK"


def _ejecutar_accion(accion: Accion) -> str | ErrorAgente:
    """Ejecuta una acción individual según su tipo."""
    if accion.tipo == "proceso":
        return processes.lanzar(accion.objetivo, accion.args)
    if accion.tipo == "funcion":
        return dispatcher.DISPATCHER[accion.objetivo](accion.args)
