"""Tokenizador del lenguaje de comandos.

Convierte el texto crudo del usuario en una lista de tokens
respetando comillas con ``shlex.split()``.
"""

import shlex


def dividir(texto: str) -> list[str]:
    """Divide el texto en tokens usando ``shlex.split()``.

    Respeta comillas simples y dobles, permitiendo rutas con
    espacios como un solo token.

    Example:
        >>> dividir('abrir "C:/Program Files/Chrome/chrome.exe"')
        ["abrir", "C:/Program Files/Chrome/chrome.exe"]

    Args:
        texto: Línea completa ingresada por el usuario.

    Returns:
        Lista de tokens (strings). Si el texto está vacío retorna
        lista vacía. Si falla el parseo con shlex, cae a str.split().
    """
    try:
        texto_normalizado = texto.replace("\\", "/")
        return shlex.split(texto_normalizado)
    except ValueError:
        return texto.strip().split()
