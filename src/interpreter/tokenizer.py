"""Tokenizador del lenguaje de comandos.

Convierte el texto crudo del usuario en una lista plana de tokens
separados por espacios en blanco.
"""


def dividir(texto: str) -> list[str]:
    """Divide el texto en tokens usando ``str.split()``.

    La tokenización es posicional: el primer token es el verbo o
    palabra clave, y los siguientes son argumentos.

    Example:
        >>> dividir("abrir firefox https://notion.so")
        ["abrir", "firefox", "https://notion.so"]

    Args:
        texto: Línea completa ingresada por el usuario.

    Returns:
        Lista de tokens (strings). Retorna lista vacía si ``texto``
        está vacío o solo contiene espacios.
    """
    return texto.strip().split()
