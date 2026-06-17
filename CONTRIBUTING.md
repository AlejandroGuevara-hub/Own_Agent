# Contributing

## Entorno de desarrollo

```bash
git clone <repo-url>
cd agente-personal
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # si existe
```

## Convenciones

- **Código:** Inglés (variables, funciones, clases, comentarios técnicos)
- **Comandos/verbos:** Español (Fase 1)
- **Docstrings:** Estilo de una línea o Google-style para funciones complejas
- **Manejo de errores:** Siempre retornar `ErrorAgente`, nunca `print()` directo
- **Toda salida al usuario** debe pasar por `notifier.mostrar()`
- **Ningún módulo** debe importar `subprocess`, `yaml` o hacer IO directo (excepto los autorizados)

## Estructura de ramas

- `main` — estable, listo para producción
- `feature/*` — nuevas funcionalidades
- `fix/*` — correcciones de bugs
- `docs/*` — mejoras de documentación

## Proceso de PR

1. Asegúrate de que el código pase `python -m compileall src`
2. Si agregas una primitiva nueva, regístrala en:
   - `src/executor/dispatcher.py`
   - `src/config/constants.py` (VERBOS, VERBOS_A_PRIMITIVA, etc.)
   - `commands/primitives.yaml`
   - `spec/commands.md`
3. Si agregas un código de error nuevo, documéntalo en `spec/cases.md`
4. Verifica que no haya `print()` en el código nuevo

## Estándares

| Aspecto | Estándar |
|---|---|
| Formateo | PEP 8 |
| Tipado | Type hints obligatorios en funciones públicas |
| Archivos YAML | `encoding: utf-8`, 2 espacios de indentación |
| Commits | Convencional Commits (`feat:`, `fix:`, `docs:`, `refactor:`) |
