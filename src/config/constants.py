VERBOS: dict[str, set[str]] = {
    "es": {
        "abrir", "cerrar", "listar", "ajustar",
        "crear", "mover", "eliminar", "programar",
        "esperar", "notificar", "consultar",
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
