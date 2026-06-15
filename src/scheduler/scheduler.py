from src.models import Intencion


def iniciar() -> None:
    """Inicia el scheduler de APScheduler."""


def registrar(intencion: Intencion) -> None:
    """Registra una tarea programada."""


def cancelar(id: str) -> None:
    """Cancela una tarea programada por su id."""
