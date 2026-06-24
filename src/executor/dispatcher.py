"""Dispatcher que mapea nombres de funciones internas a sus implementaciones.

Centraliza el registro de funciones disponibles para que el executor
no tenga que conocerlas individualmente. Escalar implica solo agregar
una nueva entrada en ``DISPATCHER``.
"""

from src.executor import functions


DISPATCHER: dict[str, callable] = {
    "ajustar_volumen":   functions.ajustar_volumen,
    "subir_volumen":     functions.subir_volumen,
    "bajar_volumen":     functions.bajar_volumen,
    "ajustar_brillo":    functions.ajustar_brillo,
    "consultar_sistema": functions.consultar_sistema,
    "cerrar_proceso":    functions.cerrar_proceso,
    "listar_procesos":   functions.listar_procesos,
    "mover_archivo":     functions.mover_archivo,
    "crear_archivo":     functions.crear_archivo,
    "eliminar_archivo":  functions.eliminar_archivo,
    "programar_alarma":  functions.programar_alarma,
    "programar_recordatorio": functions.programar_recordatorio,
    "esperar":           functions.esperar,
    "notificar":         functions.notificar,
    "consultar_web":     functions.consultar_web,
}
