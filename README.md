# Own Agent

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Agente de automatización personal para Windows. Interpreta comandos de texto del usuario, ejecuta acciones en el sistema operativo y programa tareas recurrentes. Diseñado para evolucionar desde comandos fijos (Fase 1) hasta lenguaje natural (Fase 2) y entrada por voz (Fase 3).

## Quick Start

```bash
git clone <repo-url>
cd agente-personal
pip install -r requirements.txt
python main.py
```

Escribe `ayuda` o `>>> ` seguido de un comando. Ejemplos:

```
>>> abrir firefox https://notion.so
>>> modo estudio
>>> cerrar firefox
```

## Stack Tecnológico

| Librería | Versión | Propósito |
|---|---|---|
| Python | ≥3.11 | Lenguaje base |
| APScheduler | ≥3.10, <4.0 | Tareas programadas |
| PyYAML | ≥6.0, <7.0 | Carga de configuración |
| rich | ≥13.0, <14.0 | Interfaz de consola |
| pyautogui | ≥0.9, <1.0 | Automatización de GUI |
| comtypes | ≥1.3.0 | API COM de Windows |
| pycaw | ≥20181226 | Control de audio |
| winotify | ≥0.1.0 | Notificaciones toast |

## Arquitectura

```
[Entrada] → [Interpreter] → [Executor] → [OS Windows]
                               ↕
                         [Scheduler]
                               ↕
                         [Notifier] → [Usuario]
                               ↕
                          [Config]
```

### Módulos

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Orquestador. Coordina el flujo completo sin lógica de negocio. |
| `src/interpreter` | Parsea y clasifica comandos de texto → `Intencion`. |
| `src/executor` | Ejecuta acciones primitivas (procesos y funciones internas). |
| `src/scheduler` | Gestiona tareas programadas con APScheduler. |
| `src/notifier` | Maneja toda la salida al usuario (consola + notificaciones). |
| `src/config` | Carga y expone configuración desde YAML en memoria. |
| `src/models.py` | Contratos de datos compartidos (`Intencion`, `Accion`, `ErrorAgente`). |

## Comandos Disponibles (Fase 1)

### Primitivas de proceso

| Comando | Ejemplo | Descripción |
|---|---|---|
| `abrir <ejecutable> [args...]` | `abrir firefox https://notion.so` | Lanza un proceso externo |
| `abrir_url <navegador> <url>` | `abrir_url firefox https://example.com` | Abre URL en navegador |
| `abrir_archivo <ruta>` | `abrir_archivo C:/docs/reporte.pdf` | Abre archivo con app predeterminada |

### Primitivas de sistema

| Comando | Ejemplo | Descripción |
|---|---|---|
| `ajustar volumen <0-100>` | `ajustar volumen 50` | Ajusta volumen del sistema |
| `ajustar brillo <0-100>` | `ajustar brillo 70` | Ajusta brillo de pantalla ⏳ |
| `consultar sistema <tipo>` | `consultar sistema ram` | Muestra métricas del sistema ⏳ |

### Primitivas de archivos

| Comando | Ejemplo | Descripción |
|---|---|---|
| `crear <ruta> <ext>` | `crear C:/docs nota md` | Crea archivo vacío ⏳ |
| `mover <origen> <destino>` | `mover C:/a.txt C:/b.txt` | Mueve/renombra archivo ⏳ |
| `eliminar <ruta>` | `eliminar C:/tmp.dat` | Elimina archivo (requiere confirmación) ⏳ |

### Primitivas de tiempo

| Comando | Ejemplo | Descripción |
|---|---|---|
| `programar alarma <HH:MM> <msg>` | `programar alarma 14:30 Reunion` | Alarma única ⏳ |
| `programar recordatorio <HH:MM> <msg>` | `programar recordatorio 09:00 Daily` | Recordatorio recurrente ⏳ |
| `esperar <segundos>` | `esperar 10` | Pausa dentro de un paquete ✅ |

### Primitivas de notificación

| Comando | Ejemplo | Descripción |
|---|---|---|
| `notificar <titulo> <msg> <dur>` | `notificar Alerta "Texto" 5` | Notificación toast ✅ |

### Web

| Comando | Ejemplo | Descripción |
|---|---|---|
| `consultar web <query>` | `consultar web clima hoy` | Consulta web ⏳ |

✅ = Implementado | ⏳ = Pendiente (ver `spec/roadmap.md`)

### Paquetes predefinidos

Los paquetes son secuencias de acciones definidas en YAML:

| Palabra clave | Acciones |
|---|---|
| `modo estudio` | Abre Firefox (Notion), VS Code y Spotify |
| `iniciar jornada` / `buenos dias` | Abre Outlook, Slack y muestra notificación |
| `apagar todo` / `fin jornada` | Notifica, espera 10s, cierra apps (programado 19:00 lun-vie) |

Ver `commands/packages.yaml` para definiciones completas.

## Comandos Destructivos

Los comandos marcados con `guard: confirmar` requieren confirmación del usuario antes de ejecutarse. En Fase 1, solo `eliminar_archivo` usa este mecanismo. Si el usuario cancela, el paquete completo se detiene.

## Manejo de Errores

Todo error es un objeto `ErrorAgente` con esta estructura:

```python
@dataclass
class ErrorAgente:
    codigo: str       # Código simbólico (CMD_VACIO, CMD_DESCONOCIDO, etc.)
    origen: str       # Módulo que detectó el error
    detalle: str      # Mensaje legible
    accion: str|None  # Acción que falló
```

Catálogo completo en `spec/cases.md`.

## Roadmap

| Fase | Objetivo | Estado |
|---|---|---|
| 1 | MVP con comandos fijos | En desarrollo |
| 2 | Lenguaje natural (LLM local + Ollama) | Planeado |
| 3 | Voz (Whisper + TTS) | Planeado |

Detalles en `spec/roadmap.md`.

## Convenciones de Código

| Aspecto | Decisión |
|---|---|
| Idioma del código | Inglés (variables, funciones, clases) |
| Idioma de verbos de comando | Español (Fase 1) |
| Idioma de mensajes al usuario | Español (Fase 1) |
| Formato de configuración | YAML |
| Manejo de errores | Siempre retornar `ErrorAgente`, nunca imprimir directo |
| Logs | Pendiente — cada acción irá a `/logs` con timestamp |
| Fail-fast | Ante cualquier error en un paquete, se detiene todo |

## Variables de Entorno

Actualmente el proyecto no requiere variables de entorno. Ver `docs/env-vars.md` para futuras configuraciones.

## Documentación

| Archivo | Contenido |
|---|---|
| `spec/architecture.md` | Arquitectura, capas y contratos de datos |
| `spec/commands.md` | Catálogo completo de comandos |
| `spec/modules.md` | Definición de módulos y pseudocódigo |
| `spec/cases.md` | Casos borde y catálogo de errores |
| `spec/roadmap.md` | Roadmap por fases |
| `docs/glossary.md` | Glosario técnico |
| `docs/faq.md` | Preguntas frecuentes |
| `docs/troubleshooting.md` | Guía de solución de problemas |
| `docs/deployment.md` | Guía de despliegue |
| `docs/adr/` | Architecture Decision Records |

## Licencia

MIT
