from src.models import Intencion, ErrorAgente
from src.interpreter import tokenizer, classifier, builder
from src.config import config


def parsear(texto: str) -> Intencion | ErrorAgente:
    """Recibe texto crudo. Devuelve un objeto Intencion.

    Coordina tokenizer, classifier y builder.
    """
    tokens = tokenizer.dividir(texto)
    nombres_paquetes = config.obtener_nombres_paquetes()
    clasificacion = classifier.clasificar(tokens, nombres_paquetes)
    if isinstance(clasificacion, ErrorAgente):
        return clasificacion
    tipo, ejecucion = clasificacion
    intencion = builder.construir(tokens, tipo, ejecucion)
    return intencion
