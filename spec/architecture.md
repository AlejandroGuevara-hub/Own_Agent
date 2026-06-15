# Arquitectura del Agente

## Capas del sistema

```
[Entrada]  →  [Interpreter]  →  [Executor]  →  [OS Windows]
                                     ↕
                               [Scheduler]
                                     ↕
                               [Notifier]  →  [Usuario]
                                     ↕
                                [Config]
```

## Flujo completo de ejecución

```
1. Usuario escribe un comando en consola
2. main.py recibe el texto
3. main.py llama a interpreter.parsear(texto)
4. interpreter.tokenizer divide el texto en tokens
5. interpreter.classifier identifica tipo e intención
6. interpreter.builder construye el objeto Intencion
7. main.py recibe la Intencion y llama a executor.ejecutar(intencion)
8. executor itera las acciones del objeto Intencion
9. Por cada accion:
     si tipo == "proceso" → executor.processes lanza subprocess
     si tipo == "funcion" → executor.dispatcher llama función interna
10. Si alguna acción falla → construye ErrorAgente → retorna a main.py
11. main.py pasa resultado o error a notifier.mostrar()
12. notifier formatea y muestra al usuario
```

## Estructura de carpetas

```
/agente-personal
  /spec                        ← documentación antes del código
    README.md
    architecture.md
    commands.md
    modules.md
    roadmap.md
    cases.md

  /src
    /interpreter               ← parsea y clasifica el comando
    /executor                  ← ejecuta acciones primitivas
    /scheduler                 ← gestiona tareas programadas
    /notifier                  ← maneja output al usuario
    /config                    ← lee y valida los YAML

  /commands                    ← archivos YAML de paquetes y primitivas
    primitives.yaml
    packages.yaml

  /logs                        ← registro de ejecuciones y errores

  /tests                       ← pruebas por módulo

  main.py                      ← orquestador, no ejecuta lógica
  requirements.txt
```

## Contratos de datos entre módulos

### Intencion
Objeto que `interpreter` entrega a `executor`.

```python
@dataclass
class Intencion:
    id: str                  # identificador del comando
    tipo: str                # "primitiva" | "paquete"
    ejecucion: str           # "instantanea" | "programada"
    schedule: dict | None    # {"hora": "08:00", "dias": ["lun"]} | None
    acciones: list[Accion]
```

### Accion
Unidad mínima ejecutable.

```python
@dataclass
class Accion:
    tipo: str        # "proceso" | "funcion"
    objetivo: str    # "firefox.exe" | "ajustar_volumen"
    args: list[str]  # parámetros en orden
```

### ErrorAgente
Objeto de error uniforme. Lo construye el módulo que detecta el fallo.

```python
@dataclass
class ErrorAgente:
    codigo: str       # ver catálogo en cases.md
    origen: str       # módulo que detectó el error
    detalle: str      # mensaje legible para el usuario
    accion: str|None  # acción que falló (si aplica)
```
