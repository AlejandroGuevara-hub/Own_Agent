# Roadmap

## Fase 1 — MVP con comandos fijos

**Objetivo:** agente funcional con comandos de texto predefinidos.

**Criterios de completitud:**
- [x] `config` carga YAML al iniciar sin errores
- [x] `interpreter` clasifica correctamente primitivas y paquetes
- [x] `executor` ejecuta las 19 primitivas del catálogo
- [x] `scheduler` dispara tareas programadas a la hora correcta
- [x] `notifier` muestra todos los errores del catálogo en formato uniforme
- [x] Guard clause funcional en `eliminar_archivo`
- [x] Fail-fast funcional en paquetes
- [x] Logs generados en `/logs` con timestamp por cada ejecución
- [x] Al menos 3 paquetes de ejemplo en `packages.yaml`

**Stack:**
- Python 3.11+
- subprocess, APScheduler, PyYAML, rich, pyautogui, comtypes, pycaw
- winotify, screen-brightness-control, psutil, ollama, dataclasses

---

## Fase 2 — Lenguaje natural

**Objetivo:** el agente entiende texto libre, no solo comandos exactos.

**Nuevas funcionalidades:**
- [x] Integración con Ollama (LLM local) en `classifier`
- [x] El LLM interpreta la intención cuando el texto no coincide con verbos registrados
- [x] Caché de traducciones LLM para evitar llamadas repetidas
- [x] Comando `recargar config` que recarga YAML sin reiniciar el agente
- [x] Búsqueda web con DuckDuckGo + resumen Ollama (`consultar_web`)
- [x] Separación del módulo llm en interpreter.py y searcher.py
- [ ] Soporte de inglés en `VERBOS["en"]`

**Criterios de completitud:**
- [x] `classifier` tiene fallback a LLM cuando no reconoce el comando
- [x] `recargar_config()` en `config` sin reiniciar el scheduler
- [x] `subir_volumen` y `bajar_volumen` como verbos directos
- [x] `notificar()` con valores por defecto (argumentos opcionales)
- [x] `consultar_web` retorna respuesta coherente al usuario (ddgs + Ollama)
- [ ] Verbos en inglés registrados y funcionales

---

## Fase 3 — Voz y expansión

**Objetivo:** el agente se puede usar completamente por voz.

**Nuevas funcionalidades:**
- Input por voz con Whisper (speech-to-text)
- Output por voz con pyttsx3 (text-to-speech)
- Análisis del sistema en tiempo real (RAM, CPU, batería, red)
- Editor de paquetes YAML desde el agente (interfaz interna)
- Soporte de más idiomas en `VERBOS`

**Criterios de completitud:**
- [ ] Input de voz detectado y convertido a texto correctamente
- [ ] Output de voz funcional para notificaciones y errores
- [x] `consultar_sistema` retorna métricas en tiempo real
- [ ] Editor de paquetes no requiere editar YAML manualmente

---

## Notas de escalabilidad

- El `dispatcher` en `executor` escala sin tocar lógica: solo agregar entradas.
- Los paquetes escalan sin tocar código: solo agregar archivos YAML.
- El soporte multiidioma escala sin tocar `classifier`: solo agregar entradas a `VERBOS`.
- La adición de nuevos tipos de errores escala sin tocar `notifier`: solo agregar al catálogo.
