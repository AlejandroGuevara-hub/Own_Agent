"""Catálogo de verbos reconocidos y sus mapeos a primitivas.

Separado de ``config.py`` para que classifier y builder puedan
importarlo sin arrastrar dependencias de YAML o rutas de archivos.
"""

PREFIJO_PAQUETE = "paquete"  # configurable por el usuario en Fase 3

VERBOS: dict[str, set[str]] = {
    "es": {
        "abrir", "cerrar", "listar", "ajustar",
        "crear", "mover", "eliminar", "programar",
        "esperar", "notificar", "consultar",
        "subir", "bajar",
    },
    "en": set(),
}

VERBOS_A_PRIMITIVA: dict[str, str | None] = {
    "abrir":     "abrir_proceso",
    "cerrar":    "cerrar_proceso",
    "listar":    "listar_procesos",
    "ajustar":   None,
    "crear":     "crear_archivo",
    "mover":     "mover_archivo",
    "eliminar":  "eliminar_archivo",
    "programar": None,
    "esperar":   "esperar",
    "notificar": "notificar",
    "consultar": None,
    "subir":     "subir_volumen",
    "bajar":     "bajar_volumen",
}

VERBOS_AMBIGUOS: dict[str, dict[str, str]] = {
    "ajustar": {
        "volumen": "ajustar_volumen",
        "brillo":  "ajustar_brillo",
    },
    "programar": {
        "alarma":       "programar_alarma",
        "recordatorio": "programar_recordatorio",
    },
    "consultar": {
        "sistema": "consultar_sistema",
        "web":     "consultar_web",
    },
}
