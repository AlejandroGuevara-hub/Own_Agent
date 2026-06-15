# Agente Personal de Automatización

## Qué es

Un agente de automatización personal para Windows que interpreta comandos de texto del usuario y ejecuta acciones en el sistema operativo. Diseñado para crecer en fases desde comandos fijos hasta lenguaje natural y voz.

## Problema que resuelve

Eliminar la fricción de ejecutar tareas repetitivas manualmente: abrir aplicaciones, programar alarmas, lanzar entornos de trabajo completos con un solo comando.

## Fases del proyecto

### Fase 1 — MVP con comandos fijos
- Comandos de texto por consola
- Acciones primitivas sobre el OS
- Paquetes de acciones definidos en YAML
- Scheduler para tareas programadas
- Sistema de errores uniforme

### Fase 2 — Lenguaje natural
- Interpretación de texto libre con LLM local (Ollama)
- Soporte multiidioma de verbos (inglés)
- Comando `recargar config` sin reiniciar el agente

### Fase 3 — Voz y expansión
- Input por voz con Whisper
- Output por TTS con pyttsx3
- Análisis del sistema (RAM, CPU, batería, red)
- Editor de paquetes YAML desde el agente

## Restricciones de diseño

- Los archivos YAML son de solo lectura durante una sesión activa.
- Toda salida al usuario pasa exclusivamente por `notifier`.
- `main.py` coordina pero no ejecuta lógica de negocio.
- Ningún módulo usa `print()` directamente.
- Ante cualquier error en un paquete, se detiene toda ejecución (fail-fast).

## Stack técnico Fase 1

| Librería | Uso |
|---|---|
| `subprocess` | Lanzar procesos externos |
| `APScheduler` | Tareas programadas |
| `PyYAML` | Carga de archivos de configuración |
| `rich` | Interfaz de consola |
| `pyautogui` | Automatización de GUI si subprocess no alcanza |
| `dataclasses` | Contratos de datos entre módulos |

## Convenciones de código

| Aspecto | Decisión |
|---|---|
| Idioma del código | Inglés (variables, funciones, clases) |
| Idioma de verbos | Español (Fase 1) |
| Idioma de mensajes al usuario | Español (Fase 1) |
| Formato de configuración | YAML |
| Manejo de errores | Siempre retornar `ErrorAgente`, nunca imprimir directo |
| Logs | Cada acción ejecutada queda en `/logs` con timestamp |
