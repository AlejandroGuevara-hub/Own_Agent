import time
from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from src.models import ErrorAgente


def ajustar_volumen(args: list[str]) -> str | ErrorAgente:
    try:
        nivel = int(args[0])
        if not 0 <= nivel <= 100:
            raise ValueError
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        volumen_escalar = nivel / 100.0
        volume.SetMasterVolumeLevelScalar(volumen_escalar, None)
        return "OK"
    except (IndexError, ValueError):
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="El nivel debe ser un número entero entre 0 y 100.",
            accion="ajustar_volumen")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al ajustar volumen: {str(e)}",
            accion="ajustar_volumen")


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
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'esperar'",
            accion="esperar",
        )
    try:
        segundos = int(args[0])
        time.sleep(segundos)
        return "OK"
    except ValueError:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle=f"Los segundos deben ser un número entero, recibido: '{args[0]}'",
            accion="esperar",
        )


def notificar(args: list[str]) -> str | ErrorAgente:
    """Muestra una notificación toast en Windows."""
    if len(args) < 3:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'notificar'",
            accion="notificar",
        )
    try:
        from winotify import Notification

        titulo = args[0]
        mensaje = args[1]
        duracion = "long" if int(args[2]) > 5 else "short"

        toast = Notification(
            app_id="Agente Personal",
            title=titulo,
            msg=mensaje,
            duration=duracion,
        )
        toast.show()
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al mostrar notificación: {str(e)}",
            accion="notificar",
        )


def consultar_web(args: list[str]) -> str | ErrorAgente:
    """Realiza una consulta web (funcionalidad completa en Fase 2)."""
