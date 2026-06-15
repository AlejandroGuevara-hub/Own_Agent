from dataclasses import dataclass, field


@dataclass
class Accion:
    tipo: str        # "proceso" | "funcion"
    objetivo: str    # "firefox.exe" | "ajustar_volumen"
    args: list[str]  # parámetros en orden


@dataclass
class Intencion:
    id: str                  # identificador del comando
    tipo: str                # "primitiva" | "paquete"
    ejecucion: str           # "instantanea" | "programada"
    schedule: dict | None    # {"hora": "08:00", "dias": ["lun"]} | None
    acciones: list[Accion]


@dataclass
class ErrorAgente:
    codigo: str       # ver catálogo en cases.md
    origen: str       # módulo que detectó el error
    detalle: str      # mensaje legible para el usuario
    accion: str | None  # acción que falló (si aplica)
