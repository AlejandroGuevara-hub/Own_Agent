from pathlib import Path

import yaml


_COMMANDS_DIR: Path = Path(__file__).resolve().parent.parent.parent / "commands"

_primitivas: list[dict] = []
_paquetes: list[dict] = []
_paquetes_por_id: dict[str, dict] = {}
_nombres_paquetes: set[str] = set()
_settings: dict = {}


def cargar() -> None:
    """Carga todos los archivos YAML de ``/commands`` en memoria.

    Lee ``primitives.yaml``, ``packages.yaml`` y ``settings.yaml``,
    construye el índice ``_paquetes_por_id`` para búsqueda rápida
    por id de paquete y guarda la configuración general en ``_settings``.
    Esta función se invoca una sola vez al iniciar el agente.

    Raises:
        FileNotFoundError: Si alguno de los archivos YAML no existe.
        yaml.YAMLError: Si el contenido YAML es inválido.
    """
    primitives_path = _COMMANDS_DIR / "primitives.yaml"
    packages_path = _COMMANDS_DIR / "packages.yaml"
    settings_path = _COMMANDS_DIR / "settings.yaml"

    with open(primitives_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _primitivas.clear()
    _primitivas.extend(data.get("primitivas", []))

    with open(packages_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _paquetes.clear()
    _paquetes_por_id.clear()
    _nombres_paquetes.clear()

    for pkg in data.get("paquetes", []):
        _paquetes.append(pkg)
        pkg_id = pkg["id"]
        _paquetes_por_id[pkg_id] = pkg
        _nombres_paquetes.add(pkg_id)

    with open(settings_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _settings.clear()
    if data:
        _settings.update(data)


def obtener_paquetes() -> dict:
    """Retorna copia del índice ``id → paquete``.

    Returns:
        Diccionario donde cada clave es el id del paquete
        y su valor es el dict completo del paquete YAML.
    """
    return dict(_paquetes_por_id)


def obtener_nombres_paquetes() -> set[str]:
    """Retorna copia del conjunto de ids de paquetes.

    Returns:
        Set con todos los ids de paquetes cargados.
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


def obtener_setting(clave: str, defecto=None):
    """Retorna el valor de una clave de configuración general.

    Los valores se cargan desde ``settings.yaml`` al iniciar el agente.

    Args:
        clave: Nombre de la clave (ej. ``"idioma"``).
        defecto: Valor por defecto si la clave no existe.

    Returns:
        El valor asociado a ``clave``, o ``defecto`` si no se encuentra.
    """
    return _settings.get(clave, defecto)


def recargar() -> None:
    """Recarga todos los YAML de ``/commands`` sin reiniciar el agente.

    Limpia los índices actuales y vuelve a llamar a ``cargar()``.
    """
    global _primitivas, _paquetes_por_id, _nombres_paquetes, _settings
    _primitivas.clear()
    _paquetes_por_id.clear()
    _nombres_paquetes.clear()
    _settings.clear()
    cargar()
