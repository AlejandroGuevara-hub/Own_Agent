"""Orquestador del agente personal.

Coordina el flujo completo. No ejecuta lógica de negocio.
No importa subprocess, yaml, ni hace output directo al usuario.
"""

from src.config import config
from src.scheduler import scheduler
from src.interpreter import interpreter
from src.executor import executor
from src.models import ErrorAgente
from src.notifier import notifier
from src.voice import voice as _voice


def iniciar() -> None:
    """Inicia el agente: carga config y arranca scheduler."""
    config.cargar()
    scheduler.iniciar()


def loop() -> None:
    """Bucle principal de escucha de comandos."""
    comando_voz = config.obtener_setting("comando_voz", "voice")
    while True:
        texto = input(">>> ")
        if texto.strip() == f"/{comando_voz}":
            notifier.mostrar("Escuchando...")
            texto = _voice.escuchar()
            notifier.mostrar(f"Escuché: {texto}")
        if not texto:
            continue
        intencion = interpreter.parsear(texto)
        if isinstance(intencion, ErrorAgente):
            notifier.mostrar(intencion)
            continue
        resultado = executor.ejecutar(intencion)
        notifier.mostrar(resultado)


def main() -> None:
    iniciar()
    loop()


if __name__ == "__main__":
    main()
