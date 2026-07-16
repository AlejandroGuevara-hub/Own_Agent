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
        "subir", "bajar", "recargar",
    },
    "en": {
        "open", "close", "list", "adjust", "create",
        "move", "delete", "schedule", "wait", "notify",
        "query", "raise", "lower", "reload",
    },
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
    "recargar":  "recargar_config",
}

VERBOS_A_PRIMITIVA_EN: dict[str, str | None] = {
    "open":    "abrir_proceso",
    "close":   "cerrar_proceso",
    "list":    "listar_procesos",
    "adjust":  None,
    "create":  "crear_archivo",
    "move":    "mover_archivo",
    "delete":  "eliminar_archivo",
    "schedule": None,
    "wait":    "esperar",
    "notify":  "notificar",
    "query":   None,
    "raise":   "subir_volumen",
    "lower":   "bajar_volumen",
    "reload":  "recargar_config",
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

VERBOS_AMBIGUOS_EN: dict[str, dict[str, str]] = {
    "adjust": {
        "volume": "ajustar_volumen",
        "brightness": "ajustar_brillo",
    },
    "schedule": {
        "alarm":    "programar_alarma",
        "reminder": "programar_recordatorio",
    },
    "query": {
        "system": "consultar_sistema",
        "web":    "consultar_web",
    },
}

MENSAJES_ERROR: dict[str, dict[str, str]] = {
    "es": {
        "CMD_VACIO":         "No escribiste ningún comando.",
        "CMD_DESCONOCIDO":   "El comando '{token}' no existe.",
        "PARAM_INVALIDO":    "El parámetro '{param}' no es válido.",
        "RUTA_INVALIDA":     "La ruta '{ruta}' no existe.",
        "APP_NO_ENCONTRADA": "La aplicación '{app}' no está instalada.",
        "ERROR_APP":         "La aplicación '{app}' reportó un error.",
        "ACCION_CANCELADA":  "Acción cancelada por el usuario.",
    },
    "en": {
        "CMD_VACIO":         "You didn't type any command.",
        "CMD_DESCONOCIDO":   "The command '{token}' does not exist.",
        "PARAM_INVALIDO":    "The parameter '{param}' is not valid.",
        "RUTA_INVALIDA":     "The path '{ruta}' does not exist.",
        "APP_NO_ENCONTRADA": "The application '{app}' is not installed.",
        "ERROR_APP":         "The application '{app}' reported an error.",
        "ACCION_CANCELADA":  "Action cancelled by user.",
    },
}
