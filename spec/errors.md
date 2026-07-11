# Catálogo de Errores de Desarrollo

Errores encontrados durante el desarrollo, su causa raíz y la solución aplicada.

---

## 1. tokenizer falla con rutas Windows (backslashes)

**Descripción:** `shlex.split()` interpreta las barras invertidas `\` como caracteres de escape, rompiendo rutas Windows como `"C:\Users\diego\Desktop"`.

**Causa raíz:** `shlex` sigue reglas POSIX donde `\` escapa el siguiente carácter. En Windows las rutas usan `\` como separador de directorios.

**Solución:** Normalizar `\` → `/` antes de pasar a `shlex.split()`, y usar barras normales en todos los tokens posteriores.

**Archivo:** `src/interpreter/tokenizer.py`

---

## 2. pycaw lanza "Activate must be called" en algunos equipos

**Descripción:** Al llamar a `IAudioEndpointVolume`, algunos sistemas lanzan `OSError: Activate must be called`.

**Causa raíz:** `comtypes.CoInitialize()` no se había llamado antes de usar la API de audio COM. En ciertas configuraciones de Windows esto es necesario.

**Solución:** Asegurar que `comtypes.CoInitialize()` se ejecute antes de cualquier llamada a `pycaw`. Implementado como import temprano en `functions.py`.

**Archivo:** `src/executor/functions.py`

---

## 3. duckduckgo-search renombrado a ddgs

**Descripción:** El paquete `duckduckgo-search` fue reemplazado por `ddgs` (fork más activo y mantenido).

**Causa raíz:** `duckduckgo-search` 8.x presentaba errores de compatibilidad con el entorno, mientras que `ddgs` 9.x ofrecía el mismo API con mejor mantenimiento.

**Solución:** Cambiar el import de `from duckduckgo_search import DDGS` a `from ddgs import DDGS`, y actualizar `requirements.txt`.

**Archivos:** `src/llm/searcher.py`, `requirements.txt`

---

## 4. classifier retornaba tokens originales en vez de traducidos por LLM

**Descripción:** Cuando el LLM traducía un comando (ej. "sube el volumen" → "subir volumen"), el builder recibía los tokens originales `["sube", "el", "volumen"]` en vez de los traducidos `["subir", "volumen"]`.

**Causa raíz:** `clasificar()` mutaba `tokens` in-place (`tokens.clear(); tokens.extend(tokens_llm)`) pero esto no era confiable y el flujo de datos era opaco. Además, el tipo de retorno solo incluía `(tipo, ejecución)` sin los tokens a usar.

**Solución:** Cambiar el tipo de retorno de `clasificar()` a `tuple[str, str, list[str]] | ErrorAgente`, donde el tercer elemento son los tokens finales (originales si es paquete/verbo conocido, o `tokens_llm` si vienen del LLM). `interpreter.parsear()` ahora desempaqueta `tipo, ejecucion, tokens_finales` y pasa estos al builder.

**Archivos:** `src/interpreter/classifier.py`, `src/interpreter/interpreter.py`

---

## 5. LLM respondía números directos en vez de comandos

**Descripción:** Para preguntas como "cuánto es 100 Fahrenheit en Celsius", el LLM respondía directamente "37.78°C" en vez de `consultar web ...`.

**Causa raíz:** El SYSTEM_PROMPT no tenía una regla explícita que prohibiera respuestas directas con números. El LLM optaba por responder la pregunta en lugar de traducirla a un comando.

**Solución:** Agregar dos reglas al FORMATO DE RESPUESTA:
- "NUNCA respondas con números solos o respuestas directas"
- "Si puedes responder la pregunta, tradúcela a: consultar web [pregunta]"

Además se agregaron ejemplos específicos de conversiones.

**Archivo:** `src/llm/interpreter.py`

---

## 6. Scheduler no iniciado al arrancar el agente

**Descripción:** Las tareas programadas (alarmas, recordatorios) no se disparaban porque el `BackgroundScheduler` nunca se iniciaba.

**Causa raíz:** `scheduler.iniciar()` no se llamaba en el ciclo de arranque de `main.py`. El scheduler se creaba pero permanecía en estado "not running".

**Solución:** Asegurar que `scheduler.iniciar()` se ejecute después de `config.cargar()` en la inicialización del agente. Agregar verificación `if not _scheduler.running` antes de llamar a `start()`.

**Archivo:** `src/scheduler/scheduler.py`

---

## 7. Logger falla si no existe /logs

**Descripción:** Al intentar escribir en `/logs/agente.log`, el logger lanzaba `FileNotFoundError` si la carpeta `logs/` no existía.

**Causa raíz:** `logging.FileHandler` no crea directorios padres automáticamente. Si es la primera ejecución o se eliminó la carpeta, falla.

**Solución:** Agregar `_LOG_DIR.mkdir(parents=True, exist_ok=True)` antes de crear el `FileHandler`. Esto asegura que el directorio `logs/` exista siempre.

**Archivo:** `src/logger/logger.py`

---

## 8. Ollama no disponible corta toda ejecución

**Descripción:** Si el servicio Ollama no está corriendo, `ollama.chat()` lanza una excepción que se propaga y corta la ejecución del agente completo.

**Causa raíz:** No había `try/except` alrededor de la llamada a `ollama.chat()` en `interpreter.py`.

**Solución:** Envolver toda la llamada en `try/except Exception` y retornar `"desconocido"` si falla, para que el classifier continúe con el flujo normal de error.

**Archivo:** `src/llm/interpreter.py`

---

## 9. Cerrar proceso falla si el proceso termina entre iteraciones

**Descripción:** Al iterar `psutil.process_iter()` y llamar a `terminate()`, el proceso podía desaparecer entre la obtención del PID y la terminación, lanzando `NoSuchProcess`. También podía no responder dentro del timeout, lanzando `TimeoutExpired`.

**Causa raíz:** No se capturaban las excepciones específicas de psutil dentro del loop de procesos.

**Solución:** Agregar `try/except psutil.NoSuchProcess` (continúa) y `try/except psutil.TimeoutExpired` (fuerza con `proc.kill()`) dentro del loop.

**Archivo:** `src/executor/functions.py` (`cerrar_proceso`)

---

## 10. Leve: `touch()` falla si el archivo ya existe

**Descripción:** `pathlib.Path.touch(exist_ok=False)` lanza `FileExistsError` si el archivo ya existe. Esto impedía crear un archivo que ya existía.

**Causa raíz:** `exist_ok=False` es el valor por defecto.

**Solución:** Se captura `FileExistsError` específicamente y se retorna un `ErrorAgente` informativo.

**Archivo:** `src/executor/functions.py` (`crear_archivo`)
