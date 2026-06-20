"""Gestor de tareas programadas basado en APScheduler.

Registra, inicia y cancela tareas que deben ejecutarse en un momento
específico o con recurrencia semanal.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from src.models import Intencion

_scheduler = BackgroundScheduler()


def iniciar() -> None:
    """Inicializa el scheduler de APScheduler.

    Debe llamarse una sola vez al arrancar el agente, después de
    ``config.cargar()``.
    """
    if not _scheduler.running:
        _scheduler.start()


def registrar(intencion: Intencion) -> None:
    """Registra una nueva tarea programada en el scheduler.

    Args:
        intencion: Objeto ``Intencion`` con ``ejecucion="programada"``
            y un ``schedule`` que contenga ``hora`` y ``dias``.

    Nota: El registro directo de jobs se realiza desde ``functions.py``.
    Este método está preparado para uso futuro desde el pipeline
    ``interpreter → executor → scheduler``.
    """


def cancelar(id: str) -> None:
    """Cancela una tarea programada existente.

    Args:
        id: Identificador de la tarea a cancelar (coincide con
            ``Intencion.id``).
    """
    try:
        _scheduler.remove_job(id)
    except Exception:
        pass


def obtener_scheduler() -> BackgroundScheduler:
    """Retorna la instancia única del BackgroundScheduler.

    Permite que otros módulos (ej. ``functions.py``) agreguen jobs
    directamente sobre la misma instancia del scheduler.
    """
    return _scheduler
