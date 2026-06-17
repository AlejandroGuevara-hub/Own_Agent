"""Punto de entrada del módulo **interpreter**.

Coordina el pipeline de parseo: tokenizer → classifier → builder.
Ningún otro módulo debe importar tokenizer, classifier o builder
directamente.
"""

from src.models import Intencion, ErrorAgente
from src.interpreter import tokenizer, classifier, builder
from src.config import config


def parsear(texto: str) -> Intencion | ErrorAgente:
    """Convierte texto crudo del usuario en un objeto ``Intencion``.

    Pipeline interno:
        1. ``tokenizer.dividir(texto)`` → tokens
        2. ``classifier.clasificar(tokens)`` → (tipo, ejecucion)
        3. ``builder.construir(tokens, tipo, ejecucion)`` → Intencion

    Si classifier retorna un ErrorAgente, se propaga inmediatamente
    sin llamar a builder.

    Args:
        texto: Línea de texto ingresada por el usuario.

    Returns:
        Objeto ``Intencion`` listo para ejecutar, o ``ErrorAgente`` si
        el comando no pudo ser parseado.
    """
    tokens = tokenizer.dividir(texto)
    nombres_paquetes = config.obtener_nombres_paquetes()
    clasificacion = classifier.clasificar(tokens, nombres_paquetes)
    if isinstance(clasificacion, ErrorAgente):
        return clasificacion
    tipo, ejecucion = clasificacion
    intencion = builder.construir(tokens, tipo, ejecucion)
    return intencion
