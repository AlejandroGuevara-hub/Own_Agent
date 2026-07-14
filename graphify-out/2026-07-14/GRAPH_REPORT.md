# Graph Report - agente-personal  (2026-07-13)

## Corpus Check
- 51 files · ~14,150 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 333 nodes · 369 edges · 40 communities (36 shown, 4 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ad07133`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- models.py
- ErrorAgente
- Own Agent
- Definición de Módulos
- main.py
- FAQ
- Catálogo de Comandos
- Catálogo de errores
- scheduler.py
- Deployment Guide
- Catálogo de Errores de Desarrollo
- Agente Personal de Automatización
- Troubleshooting
- Arquitectura del Agente
- Contributing
- ADR-001: Arquitectura de Capas con Orquestador
- ADR-002: Manejo de Errores Uniforme con ErrorAgente
- bug_report.md
- Roadmap
- [Unreleased]
- feature_request.md
- PULL_REQUEST_TEMPLATE.md
- Security Policy
- dependencies
- opencode.json
- interpreter.py
- searcher.py
- Variables de Entorno
- graphify.js
- AGENTS.md
- glossary.md

## God Nodes (most connected - your core abstractions)
1. `ErrorAgente` - 36 edges
2. `Own Agent` - 12 edges
3. `Catálogo de Errores de Desarrollo` - 11 edges
4. `Intencion` - 10 edges
5. `Troubleshooting` - 10 edges
6. `Definición de Módulos` - 10 edges
7. `Comandos Disponibles (Fase 1)` - 8 edges
8. `Agente Personal de Automatización` - 8 edges
9. `Catálogo de errores` - 8 edges
10. `Catálogo de Comandos` - 8 edges

## Surprising Connections (you probably didn't know these)
- `loop()` --indirect_call--> `ErrorAgente`  [INFERRED]
  main.py → src/models.py
- `clasificar()` --references--> `ErrorAgente`  [EXTRACTED]
  src/interpreter/classifier.py → src/models.py
- `ejecutar()` --references--> `ErrorAgente`  [EXTRACTED]
  src/executor/executor.py → src/models.py
- `_ejecutar_accion()` --references--> `ErrorAgente`  [EXTRACTED]
  src/executor/executor.py → src/models.py
- `subir_volumen()` --references--> `ErrorAgente`  [EXTRACTED]
  src/executor/functions.py → src/models.py

## Import Cycles
- None detected.

## Communities (40 total, 4 thin omitted)

### Community 0 - "models.py"
Cohesion: 0.07
Nodes (29): Catálogo de verbos reconocidos y sus mapeos a primitivas.  Separado de ``config., Dispatcher que mapea nombres de funciones internas a sus implementaciones.  Cent, ejecutar(), _ejecutar_accion(), Itera las acciones de una Intencion y las ejecuta secuencialmente.  Aplica la po, Itera las acciones de la Intencion. Detiene en el primer error (fail-fast)., Ejecuta una acción individual según su tipo., lanzar() (+21 more)

### Community 1 - "ErrorAgente"
Cohesion: 0.10
Nodes (30): ajustar_brillo(), ajustar_volumen(), bajar_volumen(), cerrar_proceso(), consultar_sistema(), consultar_web(), crear_archivo(), _disparar_notificacion() (+22 more)

### Community 2 - "Own Agent"
Cohesion: 0.10
Nodes (20): Arquitectura, Comandos Destructivos, Comandos Disponibles (Fase 1), Convenciones de Código, Documentación, Licencia, Manejo de Errores, Módulos (+12 more)

### Community 3 - "Definición de Módulos"
Cohesion: 0.10
Nodes (20): builder.py, classifier.py, /config, Definición de Módulos, Diagrama de clases (modelos de datos), dispatcher.py, /executor, executor.py (+12 more)

### Community 4 - "main.py"
Cohesion: 0.13
Nodes (16): iniciar(), loop(), main(), Orquestador del agente personal.  Coordina el flujo completo. No ejecuta lógica, Inicia el agente: carga config y arranca scheduler., Bucle principal de escucha de comandos., cargar(), obtener_nombres_paquetes() (+8 more)

### Community 5 - "FAQ"
Cohesion: 0.12
Nodes (15): ¿Cómo agrego un nuevo comando primitivo?, ¿Cómo creo un paquete nuevo?, ¿Cómo ejecuto los tests?, ¿Cómo se manejan los errores?, Desarrollo, FAQ, ¿Funciona en Linux o macOS?, Instalación (+7 more)

### Community 6 - "Catálogo de Comandos"
Cohesion: 0.12
Nodes (15): ARCHIVOS, Catálogo de Comandos, Catálogo de primitivas, Comandos destructivos, CONFIGURACIÓN, Contrato de un comando (YAML), Detección de paquetes multi-palabra, Ejemplo de paquete (+7 more)

### Community 7 - "Catálogo de errores"
Cohesion: 0.14
Nodes (13): ACCION_CANCELADA, APP_NO_ENCONTRADA, Casos Borde y Catálogo de Errores, Catálogo de errores, CMD_DESCONOCIDO, CMD_VACIO, Comportamiento ante errores en paquetes, ERROR_APP (+5 more)

### Community 8 - "scheduler.py"
Cohesion: 0.17
Nodes (12): BackgroundScheduler, cancelar(), iniciar(), obtener_scheduler(), Gestor de tareas programadas basado en APScheduler.  Registra, inicia y cancela, Inicializa el scheduler de APScheduler.      Debe llamarse una sola vez al arran, Registra una nueva tarea programada en el scheduler.      Args:         intencio, Cancela una tarea programada existente.      Args:         id: Identificador de (+4 more)

### Community 9 - "Deployment Guide"
Cohesion: 0.17
Nodes (11): 1. Clonar el repositorio, 2. Crear y activar entorno virtual, 3. Instalar dependencias, 4. Ejecutar, Configuración de paquetes personalizados, Deployment Guide, Despliegue como ejecutable (opcional), Instalación (+3 more)

### Community 10 - "Catálogo de Errores de Desarrollo"
Cohesion: 0.17
Nodes (11): 10. Leve: `touch()` falla si el archivo ya existe, 1. tokenizer falla con rutas Windows (backslashes), 2. pycaw lanza "Activate must be called" en algunos equipos, 3. duckduckgo-search renombrado a ddgs, 4. classifier retornaba tokens originales en vez de traducidos por LLM, 5. LLM respondía números directos en vez de comandos, 6. Scheduler no iniciado al arrancar el agente, 7. Logger falla si no existe /logs (+3 more)

### Community 11 - "Agente Personal de Automatización"
Cohesion: 0.17
Nodes (11): Agente Personal de Automatización, Convenciones de código, Documentación asociada, Fase 1 — MVP con comandos fijos, Fase 2 — Lenguaje natural, Fase 3 — Voz y expansión, Fases del proyecto, Problema que resuelve (+3 more)

### Community 12 - "Troubleshooting"
Cohesion: 0.18
Nodes (10): El comando no se reconoce pero existe en YAML, El volumen no se ajusta, Error: "El comando 'X' no existe.", Error: "El nivel debe ser un número entero entre 0 y 100.", Error: "La aplicación 'X' no está instalada o la ruta es incorrecta.", Error: "No escribiste ningún comando.", Error: "Parámetros insuficientes para 'esperar'", Error: "Parámetros insuficientes para 'notificar'" (+2 more)

### Community 13 - "Arquitectura del Agente"
Cohesion: 0.22
Nodes (8): Accion, Arquitectura del Agente, Capas del sistema, Contratos de datos entre módulos, ErrorAgente, Estructura de carpetas, Flujo completo de ejecución, Intencion

### Community 14 - "Contributing"
Cohesion: 0.29
Nodes (6): Contributing, Convenciones, Entorno de desarrollo, Estructura de ramas, Estándares, Proceso de PR

### Community 15 - "ADR-001: Arquitectura de Capas con Orquestador"
Cohesion: 0.29
Nodes (6): ADR-001: Arquitectura de Capas con Orquestador, Consecuencias, Contexto, Decisión, Estado, Referencias

### Community 16 - "ADR-002: Manejo de Errores Uniforme con ErrorAgente"
Cohesion: 0.33
Nodes (5): ADR-002: Manejo de Errores Uniforme con ErrorAgente, Consecuencias, Contexto, Decisión, Estado

### Community 17 - "bug_report.md"
Cohesion: 0.33
Nodes (5): Captura de pantalla / logs, Comportamiento esperado, Descripción, Entorno, Reproducir

### Community 18 - "Roadmap"
Cohesion: 0.33
Nodes (5): Fase 1 — MVP con comandos fijos, Fase 2 — Lenguaje natural, Fase 3 — Voz y expansión, Notas de escalabilidad, Roadmap

### Community 19 - "[Unreleased]"
Cohesion: 0.40
Nodes (4): Added, Changelog, Pending (Fase 1), [Unreleased]

### Community 20 - "feature_request.md"
Cohesion: 0.40
Nodes (4): Alternativas consideradas, Contexto adicional, Problema, Solución propuesta

### Community 21 - "PULL_REQUEST_TEMPLATE.md"
Cohesion: 0.40
Nodes (4): Checklist, Descripción, Pruebas realizadas, Tipo de cambio

### Community 22 - "Security Policy"
Cohesion: 0.40
Nodes (4): Consideraciones de seguridad, Reporting a Vulnerability, Security Policy, Supported Versions

### Community 23 - "dependencies"
Cohesion: 0.50
Nodes (3): @opencode-ai/plugin, dependencies, @opencode-ai/plugin

### Community 24 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 25 - "interpreter.py"
Cohesion: 0.50
Nodes (3): interpretar(), Interpretación de lenguaje natural vía Ollama.  Fallback para cuando el classifi, Envía el texto del usuario al LLM local y retorna la traducción.      Los result

### Community 26 - "searcher.py"
Cohesion: 0.50
Nodes (3): consultar(), Búsqueda web con DuckDuckGo y resumen vía Ollama.  Usa duckduckgo-search para ob, Busca ``query`` en DuckDuckGo y resume los resultados con Ollama.      Args:

## Knowledge Gaps
- **152 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `@opencode-ai/plugin`, `Descripción`, `Reproducir` (+147 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ErrorAgente` connect `ErrorAgente` to `models.py`, `main.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `Intencion` connect `models.py` to `scheduler.py`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `obtener_scheduler()` connect `scheduler.py` to `ErrorAgente`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `$schema`, `.opencode/plugins/graphify.js`, `@opencode-ai/plugin` to the rest of the system?**
  _152 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07422402159244265 - nodes in this community are weakly interconnected._
- **Should `ErrorAgente` be split into smaller, more focused modules?**
  _Cohesion score 0.1028225806451613 - nodes in this community are weakly interconnected._
- **Should `Own Agent` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._