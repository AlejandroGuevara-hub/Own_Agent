from src.models import ErrorAgente


def ajustar_volumen(args: list[str]) -> str | ErrorAgente:
    """Ajusta el volumen del sistema (0-100)."""


def ajustar_brillo(args: list[str]) -> str | ErrorAgente:
    """Ajusta el brillo de la pantalla (0-100)."""


def consultar_sistema(args: list[str]) -> str | ErrorAgente:
    """Consulta métricas del sistema: ram, cpu, bateria, red."""


def cerrar_proceso(args: list[str]) -> str | ErrorAgente:
    """Cierra un proceso por nombre."""


def listar_procesos(args: list[str]) -> str | ErrorAgente:
    """Lista los procesos activos."""


def mover_archivo(args: list[str]) -> str | ErrorAgente:
    """Mueve un archivo de ruta_origen a ruta_destino."""


def crear_archivo(args: list[str]) -> str | ErrorAgente:
    """Crea un archivo vacío con una extensión específica (txt, md, py)."""


def eliminar_archivo(args: list[str]) -> str | ErrorAgente:
    """Elimina un archivo. Requiere confirmación del usuario."""


def programar_alarma(args: list[str]) -> str | ErrorAgente:
    """Programa una alarma a una hora específica."""


def programar_recordatorio(args: list[str]) -> str | ErrorAgente:
    """Programa un recordatorio recurrente."""


def esperar(args: list[str]) -> str | ErrorAgente:
    """Pausa la ejecución por una cantidad de segundos."""


def notificar(args: list[str]) -> str | ErrorAgente:
    """Muestra una notificación toast en Windows."""


def consultar_web(args: list[str]) -> str | ErrorAgente:
    """Realiza una consulta web (funcionalidad completa en Fase 2)."""
