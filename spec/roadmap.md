# Roadmap

## Fase 1 — MVP con comandos fijos

**Objetivo:** agente funcional con comandos de texto predefinidos.

**Criterios de completitud:**
- [ ] `config` carga YAML al iniciar sin errores
- [ ] `interpreter` clasifica correctamente primitivas y paquetes
- [x] `executor` ejecuta las 13 primitivas del catálogo
- [x] `scheduler` dispara tareas programadas a la hora correcta
- [x] `notifier` muestra todos los errores del catálogo en formato uniforme
- [x] Guard clause funcional en `eliminar_archivo`
- [ ] Fail-fast funcional en paquetes
- [ ] Logs generados en `/logs` con timestamp por cada ejecución
- [ ] Al menos 3 paquetes de ejemplo en `packages.yaml`

**Stack:**
- Python 3.11+
- subprocess, APScheduler, PyYAML, rich, pyautogui, dataclasses

---

## Fase 2 — Lenguaje natural

**Objetivo:** el agente entiende texto libre, no solo comandos exactos.

**Nuevas funcionalidades:**
- Integración con Ollama (LLM local) en `classifier`
- El LLM interpreta la intención cuando el texto no coincide con verbos registrados
- Soporte de inglés en `VERBOS["en"]`
- Comando `recargar config` que recarga YAML sin reiniciar el agente
- `consultar_web` completo con resultados desde el LLM

**Criterios de completitud:**
- [ ] `classifier` tiene fallback a LLM cuando no reconoce el comando
- [ ] Verbos en inglés registrados y funcionales
- [ ] `recargar_config()` en `config` sin reiniciar el scheduler
- [ ] `consultar_web` retorna respuesta coherente al usuario

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
