from rich.console import Console
from rich.text import Text

from src.models import ErrorAgente


_console = Console()


def mostrar(resultado: str | ErrorAgente) -> None:
    """Formatea y muestra un resultado o error al usuario usando rich."""
    if isinstance(resultado, ErrorAgente):
        t = Text()
        t.append(f"[{resultado.codigo}] ", style="bold red")
        t.append(f"{resultado.origen}: ", style="red")
        t.append(resultado.detalle, style="white")
        _console.print(t)
    else:
        _console.print(resultado, style="green")


def confirmar(mensaje: str) -> bool:
    """Solicita confirmación al usuario para comandos destructivos.
    Retorna True si el usuario confirma, False si cancela.
    Máximo 3 intentos.
    """
    for _ in range(3):
        respuesta = input(f"{mensaje} [s/n] ").strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
    return False
