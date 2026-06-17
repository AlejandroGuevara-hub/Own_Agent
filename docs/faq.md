# FAQ

## Instalación

### ¿Qué versiones de Python son compatibles?
Python 3.11 o superior. El proyecto usa `str | None` (PEP 604) y `list[str]` (PEP 585).

### ¿Funciona en Linux o macOS?
No. El proyecto está diseñado específicamente para Windows (APIs COM, `winotify`, `pycaw`).

### ¿Necesito instalar algo adicional?
Las dependencias están en `requirements.txt`. Algunas funciones internas
(pycaw, comtypes) requieren tener los controladores de audio de Windows actualizados.

## Uso

### ¿Cómo agrego un nuevo comando primitivo?
1. Agrega la implementación en `src/executor/functions.py`
2. Registra la función en `src/executor/dispatcher.py`
3. Agrega el verbo en `src/config/constants.py` (`VERBOS`, `VERBOS_A_PRIMITIVA`)
4. Define la primitiva en `commands/primitives.yaml`
5. Documenta en `spec/commands.md`

### ¿Cómo creo un paquete nuevo?
Agrega una entrada en `commands/packages.yaml` siguiendo la estructura documentada
en `spec/commands.md`. No necesitas modificar código Python.

### ¿Por qué algunos comandos no hacen nada?
Varias primitivas son stubs (implementación pendiente). Ver el roadmap en
`spec/roadmap.md` y la tabla de comandos en `README.md`.

## Técnicas

### ¿Cómo se manejan los errores?
Todo error se propaga como `ErrorAgente`. El módulo que detecta la falla
construye el objeto y lo retorna. `notifier.mostrar()` lo formatea para el usuario.

### ¿Qué significa fail-fast?
Si una acción dentro de un paquete falla, el paquete completo se detiene
inmediatamente. No se ejecutan las acciones siguientes.

### ¿Puedo cambiar la configuración sin reiniciar?
Actualmente los YAML se cargan una sola vez al iniciar. La recarga en caliente
está planeada para Fase 2.

## Desarrollo

### ¿Cómo ejecuto los tests?
El proyecto está en fase inicial. Los tests se agregarán durante el desarrollo.
```bash
# Una vez implementados:
python -m pytest tests/
```
