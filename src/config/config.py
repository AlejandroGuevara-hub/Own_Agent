from pathlib import Path

import yaml


_COMMANDS_DIR: Path = Path(__file__).resolve().parent.parent.parent / "commands"

_primitivas: list[dict] = []
_paquetes: list[dict] = []
_paquetes_por_trigger: dict[str, dict] = {}
_nombres_paquetes: set[str] = set()


def cargar() -> None:
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
    return dict(_paquetes_por_trigger)


def obtener_nombres_paquetes() -> set[str]:
    return set(_nombres_paquetes)


def obtener_primitiva(id: str) -> dict | None:
    for p in _primitivas:
        if p.get("id") == id:
            return p
    return None
