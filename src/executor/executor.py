"""Itera las acciones de una Intencion y las ejecuta secuencialmente.

Aplica la política **fail-fast**: ante el primer error detiene toda
la ejecución y retorna el ``ErrorAgente`` inmediatamente.
"""

from src.models import Intencion, Accion, ErrorAgente
from src.executor import processes, dispatcher
from src.notifier import notifier
from src.logger import logger


def ejecutar(intencion: Intencion) -> str | ErrorAgente:
    """Itera las acciones de la Intencion. Detiene en el primer error (fail-fast)."""
    for accion in intencion.acciones:
        resultado = _ejecutar_accion(accion)
        logger.registrar(resultado, accion.objetivo)
        if isinstance(resultado, ErrorAgente):
            return resultado
    return "OK"


def _ejecutar_accion(accion: Accion) -> str | ErrorAgente:
    """Ejecuta una acción individual según su tipo."""
    if accion.confirmacion:
        if not notifier.confirmar(f"¿Confirmas ejecutar '{accion.objetivo}'?"):
            return ErrorAgente(
                codigo="ACCION_CANCELADA",
                origen="executor",
                detalle="Acción cancelada por el usuario.",
                accion=accion.objetivo)
    if accion.tipo == "proceso":
        return processes.lanzar(accion.objetivo, accion.args)
    if accion.tipo == "funcion":
        return dispatcher.DISPATCHER[accion.objetivo](accion.args)
