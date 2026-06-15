import subprocess

from src.models import ErrorAgente


def lanzar(objetivo: str, args: list[str]) -> str | ErrorAgente:
    """Lanza ejecutables externos con subprocess."""
    try:
        subprocess.Popen([objetivo] + args)
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
