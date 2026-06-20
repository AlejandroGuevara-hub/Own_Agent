"""Sistema de logs del agente.

Cada acción ejecutada se registra en ``/logs/agente.log`` con formato:
    [YYYY-MM-DD HH:MM:SS] [RESULTADO] ORIGEN - DETALLE

Usa el módulo estándar ``logging``. No requiere librerías externas.
"""

import logging
from pathlib import Path

from src.models import ErrorAgente


_LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
_LOG_FILE = _LOG_DIR / "agente.log"

_logger = logging.getLogger("agente")
_logger.setLevel(logging.DEBUG)

_LOG_DIR.mkdir(parents=True, exist_ok=True)
_file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8", mode="a")
_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)


def registrar(resultado: str | ErrorAgente, accion: str) -> None:
    """Registra en el log el resultado de una acción ejecutada.

    Args:
        resultado: ``"OK"`` (éxito) u objeto ``ErrorAgente`` (fallo).
        accion: Identificador de la acción ejecutada (ej. ``"abrir_proceso"``).
    """
    if isinstance(resultado, ErrorAgente):
        _logger.error("%s - %s: %s", resultado.origen, resultado.codigo, resultado.detalle)
    else:
        _logger.info("OK - %s", accion)
