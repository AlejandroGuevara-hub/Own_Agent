"""Modelos de datos para intenciones y acciones del agente."""

from dataclasses import dataclass


@dataclass
class Accion:
    """Unidad mínima ejecutable dentro de una Intencion.

    Attributes:
        tipo: Tipo de ejecución — ``"proceso"`` (externo vía subprocess)
            o ``"funcion"`` (interna del agente).
        objetivo: Identificador del destino. Para procesos es el ejecutable
            (ej. ``"firefox.exe"``); para funciones es el nombre registrado
            en el dispatcher (ej. ``"ajustar_volumen"``).
        args: Lista de argumentos posicionales que se pasan al objetivo.
    """
    tipo: str
    objetivo: str
    args: list[str]
    confirmacion: bool = False


@dataclass
class Intencion:
    """Contrato entre el módulo **interpreter** y el módulo **executor**.

    Representa un comando ya parseado, clasificado y listo para ejecutar.

    Attributes:
        id: Identificador único del comando (ej. ``"abrir_proceso"``).
        tipo: Categoría del comando — ``"primitiva"`` o ``"paquete"``.
        ejecucion: Modalidad de ejecución — ``"instantanea"`` o ``"programada"``.
        schedule: Configuración de programación temporal. ``None`` si es
            instantáneo; ``{"hora": "08:00", "dias": ["lun"]}`` si es programado.
        acciones: Lista ordenada de acciones a ejecutar (fail-fast).
    """
    id: str
    tipo: str
    ejecucion: str
    schedule: dict | None
    acciones: list[Accion]
