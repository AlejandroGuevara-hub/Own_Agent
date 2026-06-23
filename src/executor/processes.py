"""Lanza procesos externos del sistema operativo usando ``subprocess``.

Es el único módulo autorizado para ejecutar ``subprocess.Popen``.
Ningún otro módulo debe importar ``subprocess`` directamente.
"""

import subprocess

from src.models import ErrorAgente


def lanzar(objetivo: str, args: list[str]) -> str | ErrorAgente:
    """Lanza un ejecutable externo con ``subprocess.Popen``.

    No espera a que el proceso termine (modo fire-and-forget).

    Args:
        objetivo: Nombre o ruta del ejecutable (ej. ``"firefox.exe"``).
        args: Lista de argumentos de línea de comandos.

    Returns:
        ``"OK"`` si el proceso se lanzó sin errores.

    Errors:
        APP_NO_ENCONTRADA: Si el ejecutable no existe o no está en PATH.
        ERROR_APP: Si ocurre cualquier otro error en el lanzamiento.
    """
    try:
        if "firefox" in objetivo.lower() and args:
            cmd = [objetivo, "--new-tab"] + args
        else:
            cmd = [objetivo] + args
        subprocess.Popen(cmd)
        return "OK"
    except FileNotFoundError:
        return ErrorAgente(
            codigo="APP_NO_ENCONTRADA",
            origen="executor/processes",
            detalle=f"La aplicación '{objetivo}' no está instalada o la ruta es incorrecta.",
            accion=objetivo)
    except Exception as e:
        return ErrorAgente(
            codigo="ERROR_APP",
            origen="executor/processes",
            detalle=f"La aplicación '{objetivo}' reportó un error: {str(e)}",
            accion=objetivo)
