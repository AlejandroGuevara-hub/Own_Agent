"""Implementación de todas las funciones internas del agente.

Cada función recibe una lista de argumentos (strings) y retorna
``"OK"`` en éxito o un objeto ``ErrorAgente`` en fallo.
"""

import os
import time
import re
from datetime import datetime
from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from src.models import ErrorAgente
from src.scheduler.scheduler import obtener_scheduler


_scheduler = obtener_scheduler()


def ajustar_volumen(args: list[str]) -> str | ErrorAgente:
    """Ajusta el volumen del sistema al nivel indicado.

    Args:
        args: ``[nivel]`` — entero entre 0 y 100.

    Returns:
        ``"OK"`` si el volumen se modificó correctamente.

    Errors:
        PARAM_INVALIDO: Si ``nivel`` no es un entero en [0, 100].
        ERROR_APP: Si la API de audio falla inesperadamente.
    """
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


def subir_volumen(args: list[str]) -> str | ErrorAgente:
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        actual = round(volume.GetMasterVolumeLevelScalar() * 100)
        nuevo = min(actual + 20, 100)
        volume.SetMasterVolumeLevelScalar(nuevo / 100.0, None)
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al subir volumen: {str(e)}",
            accion="subir_volumen")


def bajar_volumen(args: list[str]) -> str | ErrorAgente:
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        actual = round(volume.GetMasterVolumeLevelScalar() * 100)
        nuevo = max(actual - 20, 0)
        volume.SetMasterVolumeLevelScalar(nuevo / 100.0, None)
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al bajar volumen: {str(e)}",
            accion="bajar_volumen")


def ajustar_brillo(args: list[str]) -> str | ErrorAgente:
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'ajustar_brillo'",
            accion="ajustar_brillo")
    try:
        import screen_brightness_control as sbc
        nivel = int(args[0])
        if not 0 <= nivel <= 100:
            return ErrorAgente(
                codigo="PARAM_INVALIDO",
                origen="executor/functions",
                detalle="El nivel debe ser un número entero entre 0 y 100.",
                accion="ajustar_brillo")
        sbc.set_brightness(nivel)
        return "OK"
    except ImportError:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle="Librería 'screen_brightness_control' no instalada. Ejecuta: pip install screen-brightness-control",
            accion="ajustar_brillo")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al ajustar brillo: {str(e)}",
            accion="ajustar_brillo")


def consultar_sistema(args: list[str]) -> str | ErrorAgente:
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'consultar_sistema'",
            accion="consultar_sistema")
    try:
        import psutil
        tipo = args[0].lower()
        if tipo == "ram":
            mem = psutil.virtual_memory()
            resultado = f"RAM: {mem.percent}% usado ({mem.used // 1024**3} GB de {mem.total // 1024**3} GB)"
        elif tipo == "cpu":
            resultado = f"CPU: {psutil.cpu_percent(interval=1)}%"
        elif tipo == "bateria":
            bat = psutil.sensors_battery()
            if bat is None:
                resultado = "No se detecta batería en el sistema."
            else:
                estado = "cargando" if bat.power_plugged else "no cargando"
                resultado = f"Batería: {bat.percent}% ({estado})"
        elif tipo == "red":
            net = psutil.net_io_counters()
            resultado = f"Red - Enviados: {net.bytes_sent // 1024} KB, Recibidos: {net.bytes_recv // 1024} KB"
        else:
            return ErrorAgente(
                codigo="PARAM_INVALIDO",
                origen="executor/functions",
                detalle=f"Tipo '{tipo}' no válido. Usa: ram, cpu, bateria o red.",
                accion="consultar_sistema")
        from src.notifier import notifier
        notifier.mostrar(resultado)
        return "OK"
    except ImportError:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle="Librería 'psutil' no instalada. Ejecuta: pip install psutil",
            accion="consultar_sistema")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al consultar sistema: {str(e)}",
            accion="consultar_sistema")


def cerrar_proceso(args: list[str]) -> str | ErrorAgente:
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'cerrar_proceso'",
            accion="cerrar_proceso")
    try:
        import psutil
        nombre = args[0]
        encontrados = 0
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] and proc.info["name"].lower() == nombre.lower():
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                    encontrados += 1
                except psutil.NoSuchProcess:
                    continue
                except psutil.TimeoutExpired:
                    proc.kill()
                    encontrados += 1
        if encontrados == 0:
            return ErrorAgente(
                codigo="APP_NO_ENCONTRADA",
                origen="executor/functions",
                detalle=f"No se encontró el proceso '{nombre}' en ejecución.",
                accion="cerrar_proceso")
        return "OK"
    except ImportError:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle="Librería 'psutil' no instalada. Ejecuta: pip install psutil",
            accion="cerrar_proceso")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al cerrar proceso '{args[0]}': {str(e)}",
            accion="cerrar_proceso")


def listar_procesos(args: list[str]) -> str | ErrorAgente:
    try:
        import psutil
        from src.notifier import notifier
        lineas = ["Procesos activos:"]
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                lineas.append(f"  {proc.info['pid']:>6}  {proc.info['name'] or '?'}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        notifier.mostrar("\n".join(lineas[:100]))
        if len(lineas) > 100:
            notifier.mostrar(f"... y {len(lineas) - 100} procesos más.")
        return "OK"
    except ImportError:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle="Librería 'psutil' no instalada. Ejecuta: pip install psutil",
            accion="listar_procesos")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al listar procesos: {str(e)}",
            accion="listar_procesos")


def mover_archivo(args: list[str]) -> str | ErrorAgente:
    if len(args) < 2:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'mover_archivo'. Uso: mover_archivo [origen] [destino]",
            accion="mover_archivo")
    try:
        import shutil
        origen, destino = args[0], args[1]
        shutil.move(origen, destino)
        return "OK"
    except FileNotFoundError:
        return ErrorAgente(
            codigo="RUTA_INVALIDA",
            origen="executor/functions",
            detalle=f"La ruta de origen '{args[0]}' no existe.",
            accion="mover_archivo")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al mover archivo: {str(e)}",
            accion="mover_archivo")


def crear_archivo(args: list[str]) -> str | ErrorAgente:
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'crear_archivo'",
            accion="crear_archivo")
    try:
        from pathlib import Path
        ruta = Path(args[0])
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.touch(exist_ok=False)
        return "OK"
    except FileExistsError:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"El archivo '{args[0]}' ya existe.",
            accion="crear_archivo")
    except Exception as e:
        return ErrorAgente(
            codigo="RUTA_INVALIDA",
            origen="executor/functions",
            detalle=f"Error al crear archivo: {str(e)}",
            accion="crear_archivo")


def eliminar_archivo(args: list[str]) -> str | ErrorAgente:
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'eliminar_archivo'",
            accion="eliminar_archivo")
    ruta = args[0]
    try:
        os.remove(ruta)
        return "OK"
    except FileNotFoundError:
        return ErrorAgente(
            codigo="RUTA_INVALIDA",
            origen="executor/functions",
            detalle=f"La ruta '{ruta}' no existe.",
            accion="eliminar_archivo")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al eliminar archivo: {str(e)}",
            accion="eliminar_archivo")


def programar_alarma(args: list[str]) -> str | ErrorAgente:
    if len(args) < 2:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'programar_alarma'. Uso: programar_alarma [HH:MM] [mensaje]",
            accion="programar_alarma")
    hora, mensaje = args[0], args[1]
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", hora)
    if not m:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle=f"Formato de hora inválido: '{hora}'. Use HH:MM (ej. 14:30).",
            accion="programar_alarma")
    h, m_min = int(m.group(1)), int(m.group(2))
    if not (0 <= h <= 23 and 0 <= m_min <= 59):
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle=f"Hora fuera de rango: '{hora}'. Debe ser entre 00:00 y 23:59.",
            accion="programar_alarma")
    try:
        _scheduler.add_job(
            _disparar_notificacion,
            trigger="cron",
            hour=h,
            minute=m_min,
            args=[mensaje],
            id=f"alarma_{h:02d}{m_min:02d}_{int(time.time())}",
            replace_existing=False,
        )
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al programar alarma: {str(e)}",
            accion="programar_alarma")


def _disparar_notificacion(mensaje: str) -> None:
    from src.notifier import notifier
    notifier.mostrar(f"ALARMA: {mensaje}")


def programar_recordatorio(args: list[str]) -> str | ErrorAgente:
    if len(args) < 3:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Parámetros insuficientes para 'programar_recordatorio'. Uso: programar_recordatorio [HH:MM] [dias] [mensaje]",
            accion="programar_recordatorio")
    hora, dias_str, mensaje = args[0], args[1], args[2]
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", hora)
    if not m:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle=f"Formato de hora inválido: '{hora}'. Use HH:MM (ej. 14:30).",
            accion="programar_recordatorio")
    h, m_min = int(m.group(1)), int(m.group(2))
    if not (0 <= h <= 23 and 0 <= m_min <= 59):
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle=f"Hora fuera de rango: '{hora}'. Debe ser entre 00:00 y 23:59.",
            accion="programar_recordatorio")
    DIA_MAP = {
        "lun": "mon", "mar": "tue", "mie": "wed", "mié": "wed",
        "jue": "thu", "vie": "fri", "sab": "sat", "dom": "sun",
    }
    dias_input = [d.strip().lower() for d in dias_str.split(",")]
    dias_en = []
    for d in dias_input:
        en = DIA_MAP.get(d)
        if not en:
            return ErrorAgente(
                codigo="PARAM_INVALIDO",
                origen="executor/functions",
                detalle=f"Día inválido: '{d}'. Usa: lun,mar,mie,jue,vie,sab,dom",
                accion="programar_recordatorio")
        dias_en.append(en)
    try:
        _scheduler.add_job(
            _disparar_notificacion,
            trigger="cron",
            day_of_week=",".join(dias_en),
            hour=h,
            minute=m_min,
            args=[mensaje],
            id=f"recordatorio_{h:02d}{m_min:02d}_{','.join(dias_input)}_{int(time.time())}",
            replace_existing=False,
        )
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al programar recordatorio: {str(e)}",
            accion="programar_recordatorio")


def esperar(args: list[str]) -> str | ErrorAgente:
    """Pausa la ejecución del hilo actual por ``N`` segundos.

    Pensado para uso dentro de paquetes que requieren esperar entre
    acciones (ej. esperar 10 segundos antes de cerrar aplicaciones).

    Args:
        args: ``[segundos]`` — entero positivo.

    Returns:
        ``"OK"`` tras completar la pausa.

    Errors:
        PARAM_INVALIDO: Si no se proporciona el argumento o no es entero.
    """
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
    """Muestra una notificación toast en Windows usando ``winotify``.

    Todos los argumentos tienen valores por defecto, por lo que
    puede llamarse sin parámetros.

    Args:
        args: ``[titulo, mensaje, duracion_seg]`` — todos opcionales.

    Returns:
        ``"OK"`` si la notificación se mostró correctamente.

    Errors:
        ERROR_APP: Si la API de notificaciones falla.
    """
    titulo = args[0] if len(args) > 0 else "Agente Personal"
    mensaje = args[1] if len(args) > 1 else "Hola mundo"
    duracion = "short"
    if len(args) > 2:
        try:
            duracion = "long" if int(args[2]) > 5 else "short"
        except ValueError:
            duracion = "short"
    try:
        from winotify import Notification

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
            accion="notificar")


def consultar_web(args: list[str]) -> str | ErrorAgente:
    """Realiza una búsqueda web usando DuckDuckGo + Ollama.

    Args:
        args: ``[query]`` — texto de la consulta.

    Returns:
        ``"OK"`` si la búsqueda se completó y el resultado se mostró.

    Errors:
        PARAM_INVALIDO: Si no hay consulta.
        ERROR_APP: Si la búsqueda falla.
    """
    if len(args) < 1:
        return ErrorAgente(
            codigo="PARAM_INVALIDO",
            origen="executor/functions",
            detalle="Escribe qué quieres consultar. Ejemplo: consultar web Python",
            accion="consultar_web")
    try:
        from src.llm import searcher
        from src.notifier import notifier
        query = " ".join(args)
        resultado = searcher.consultar(query)
        notifier.mostrar(resultado)
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al consultar web: {str(e)}",
            accion="consultar_web")


def escuchar_voz(args: list[str]) -> str | ErrorAgente:
    """Graba audio del micrófono, transcribe con Whisper y muestra el texto.

    Args:
        args: ``[duracion_seg]`` — opcional, por defecto 5 segundos.

    Returns:
        El texto transcrito si se detectó voz.
    """
    try:
        from src.voice import escuchar
        from src.notifier import notifier
        duracion = 5
        if args and args[0].isdigit():
            duracion = int(args[0])
        notifier.mostrar(f"Escuchando durante {duracion} segundos...")
        texto = escuchar(duracion=duracion)
        if not texto:
            return ErrorAgente(
                codigo="ERROR_APP",
                origen="executor/functions",
                detalle="No se detectó voz.",
                accion="escuchar_voz")
        notifier.mostrar(f"Texto detectado: {texto}")
        return texto
    except ImportError as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Falta librería de voz: {str(e)}. Ejecuta: pip install openai-whisper sounddevice scipy pyttsx3",
            accion="escuchar_voz")
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al escuchar voz: {str(e)}",
            accion="escuchar_voz")


def recargar_config(args: list[str]) -> str | ErrorAgente:
    """Recarga la configuración YAML y reinicia el scheduler.

    Args:
        args: Sin parámetros.

    Returns:
        ``"OK"`` si la recarga se completó correctamente.

    Errors:
        ERROR_APP: Si ocurre un error al recargar.
    """
    try:
        from src.config import config
        from src.scheduler import scheduler
        scheduler.reiniciar()
        config.recargar()
        return "OK"
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/functions",
            detalle=f"Error al recargar config: {str(e)}",
            accion="recargar_config")
