from pathlib import Path

import yaml


_COMMANDS_DIR: Path = Path(__file__).resolve().parent.parent.parent / "commands"

_primitivas: list[dict] = []
_paquetes: list[dict] = []
_paquetes_por_trigger: dict[str, dict] = {}
_nombres_paquetes: set[str] = set()


def cargar() -> None:
    """Carga todos los archivos YAML de ``/commands`` en memoria.

    Lee ``primitives.yaml`` y ``packages.yaml``, construye los índices
    ``_paquetes_por_trigger`` y ``_nombres_paquetes`` para búsqueda
    rápida por palabra clave. Esta función se invoca una sola vez al
    iniciar el agente.

    Raises:
        FileNotFoundError: Si alguno de los archivos YAML no existe.
        yaml.YAMLError: Si el contenido YAML es inválido.
    """
    primitives_path = _COMMANDS_DIR / "primitives.yaml"
    packages_path = _COMMANDS_DIR / "packages.yaml"

    with open(primitives_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _primitivas.clear()
    _primitivas.extend(data.get("primitivas", []))

    with open(packages_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _paquetes.clear()
    _paquetes_por_trigger.clear()
    _nombres_paquetes.clear()

    for pkg in data.get("paquetes", []):
        _paquetes.append(pkg)
        for palabra in pkg.get("trigger", {}).get("palabras_clave", []):
            _paquetes_por_trigger[palabra] = pkg
            _nombres_paquetes.add(palabra)


def obtener_paquetes() -> dict:
    """Retorna copia del índice ``palabra_clave → paquete``.

    Returns:
        Diccionario donde cada clave es una palabra clave registrada
        y su valor es el dict completo del paquete YAML.
    """
    return dict(_paquetes_por_trigger)


def obtener_nombres_paquetes() -> set[str]:
    """Retorna copia del conjunto de palabras clave de paquetes.

    Returns:
        Set con todas las palabras clave que disparan paquetes.
    """
    return set(_nombres_paquetes)


def obtener_primitiva(id: str) -> dict | None:
    """Busca una primitiva por su id en la lista cargada.

    Args:
        id: Identificador de la primitiva (ej. ``"abrir_proceso"``).

    Returns:
        El dict YAML de la primitiva, o ``None`` si no existe.
    """
    for p in _primitivas:
        if p.get("id") == id:
            return p
    return None
