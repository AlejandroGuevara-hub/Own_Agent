"""Gestor de tareas programadas basado en APScheduler.

Registra, inicia y cancela tareas que deben ejecutarse en un momento
específico o con recurrencia semanal.
"""

from src.models import Intencion


def iniciar() -> None:
    """Inicializa el scheduler de APScheduler.

    Debe llamarse una sola vez al arrancar el agente, después de
    ``config.cargar()``.

    Nota: Implementación pendiente (Fase 1). Deberá crear una instancia
    de ``BackgroundScheduler`` y llamar a ``start()``.
    """


def registrar(intencion: Intencion) -> None:
    """Registra una nueva tarea programada en el scheduler.

    Args:
        intencion: Objeto ``Intencion`` con ``ejecucion="programada"``
            y un ``schedule`` que contenga ``hora`` y ``dias``.

    Nota: Implementación pendiente (Fase 1). Deberá agregar un job
    cron o date según la configuración de la intención.
    """


def cancelar(id: str) -> None:
    """Cancela una tarea programada existente.

    Args:
        id: Identificador de la tarea a cancelar (coincide con
            ``Intencion.id``).

    Nota: Implementación pendiente (Fase 1). Deberá llamar a
    ``scheduler.remove_job(id)``.
    """
