"""Modelos de datos para errores del agente."""

from dataclasses import dataclass


@dataclass
class ErrorAgente:
    """Objeto de error uniforme utilizado en todo el agente.

    Lo construye exclusivamente el módulo que detecta la falla.
    Nunca se imprime directamente — ``notifier`` es quien lo muestra.

    Attributes:
        codigo: Código simbólico del error. Ver catálogo en ``spec/cases.md``.
        origen: Ruta del módulo que originó el error (ej. ``"executor/functions"``).
        detalle: Mensaje legible para el usuario final.
        accion: Identificador de la acción que falló, o ``None`` si no aplica.
    """
    codigo: str
    origen: str
    detalle: str
    accion: str | None
