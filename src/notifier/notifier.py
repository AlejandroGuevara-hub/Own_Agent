"""Módulo de salida al usuario.

Único módulo autorizado para hacer output. Centraliza el formateo
con la librería ``rich`` y evita el uso de ``print()`` directo en
el resto del código.
"""

from rich.console import Console
from rich.text import Text

from src.models import ErrorAgente
from src.config import config


_console = Console()


def mostrar(resultado: str | ErrorAgente) -> None:
    """Formatea y muestra un resultado o error al usuario.

    - Si es ``ErrorAgente``: muestra el código en rojo negrita, el
      origen en rojo y el detalle en blanco.
    - Si es ``str``: muestra el texto en verde.

    Args:
        resultado: ``"OK"``, texto informativo, o un objeto ``ErrorAgente``.
    """
    if isinstance(resultado, ErrorAgente):
        t = Text()
        t.append(f"[{resultado.codigo}] ", style="bold red")
        t.append(f"{resultado.origen}: ", style="red")
        t.append(resultado.detalle, style="white")
        _console.print(t)
    else:
        _console.print(resultado, style="green")

    if config.obtener_setting("voz_activa", False) and resultado != "OK":
        _hablar(resultado.detalle if isinstance(resultado, ErrorAgente) else resultado)


def _hablar(texto: str) -> None:
    try:
        from src.voice.voice import hablar
        hablar(texto)
    except ImportError:
        pass


def confirmar(mensaje: str) -> bool:
    """Solicita confirmación al usuario para comandos destructivos.

    El usuario tiene un máximo de 3 intentos para responder ``s``
    (confirma) o ``n`` (cancela). Cualquier otra respuesta se ignora
    y se vuelve a preguntar.

    Args:
        mensaje: Texto que se muestra al usuario junto con ``[s/n]``.

    Returns:
        ``True`` si el usuario confirma, ``False`` si cancela.
        También retorna ``False`` si se agotan los 3 intentos.
    """
    for _ in range(3):
        respuesta = input(f"{mensaje} [s/n] ").strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
    return False
