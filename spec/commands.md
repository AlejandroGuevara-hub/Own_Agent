# Catálogo de Comandos

## Contrato de un comando (YAML)

Todo comando, sea primitiva o paquete, sigue esta estructura:

```yaml
id: "string"
tipo: "primitiva | paquete"
ejecucion: "instantanea | programada"
on_error: "stop"               # siempre stop en Fase 1
guard: null                    # null | "confirmar" — solo en primitivas
trigger:
  palabras_clave: []           # lista de formas de invocar el comando
                                # en paquetes, cada elemento puede tener
                                # múltiples palabras separadas por espacio
schedule:
  hora: null                   # "HH:MM" si es programada
  dias: []                     # ["lun", "mar"...] si es recurrente
acciones:
  - tipo: "proceso | funcion"
    objetivo: "string"
    args: []
```

## Verbos primitivos registrados

```python
VERBOS = {
    "es": {
        "abrir", "cerrar", "listar", "ajustar",
        "crear", "mover", "eliminar", "programar",
        "esperar", "notificar", "consultar",
        "subir", "bajar",
    },
    "en": set()  # vacío hasta Fase 3
}
```

## Catálogo de primitivas

### PROCESOS

```yaml
- id: abrir_proceso
  tipo: proceso
  objetivo: nombre del ejecutable (ej: firefox.exe)
  args: [parámetros opcionales como URL o ruta]
  produce: proceso activo | ERROR_APP | APP_NO_ENCONTRADA

- id: cerrar_proceso
  tipo: funcion
  objetivo: cerrar_proceso
  args: [nombre_proceso]
  produce: proceso terminado | APP_NO_ENCONTRADA

- id: listar_procesos
  tipo: funcion
  objetivo: listar_procesos
  args: []
  produce: lista de procesos activos en consola
```

### SISTEMA

```yaml
- id: ajustar_volumen
  tipo: funcion
  objetivo: ajustar_volumen
  args: [nivel: 0-100]
  produce: volumen modificado | PARAM_INVALIDO

- id: ajustar_brillo
  tipo: funcion
  objetivo: ajustar_brillo
  args: [nivel: 0-100]
  produce: brillo modificado | PARAM_INVALIDO

- id: consultar_sistema
  tipo: funcion
  objetivo: consultar_sistema
  args: [tipo: ram | cpu | bateria | red]
  produce: valor actual en consola | PARAM_INVALIDO
```

### ARCHIVOS

```yaml
- id: abrir_archivo
  tipo: proceso
  objetivo: ruta del archivo
  args: []
  produce: archivo abierto con app predeterminada | RUTA_INVALIDA

- id: mover_archivo
  tipo: funcion
  objetivo: mover_archivo
  args: [ruta_origen, ruta_destino]
  produce: archivo movido | RUTA_INVALIDA

- id: crear_archivo
  tipo: funcion
  objetivo: crear_archivo
  args: [ruta_completa]
  produce: archivo vacío creado | RUTA_INVALIDA

- id: eliminar_archivo
  tipo: funcion
  objetivo: eliminar_archivo
  args: [ruta]
  guard: confirmar   # detiene ejecución y espera respuesta del usuario
  produce: archivo eliminado | ACCION_CANCELADA | RUTA_INVALIDA
```

### TIEMPO

```yaml
- id: programar_alarma
  tipo: funcion
  objetivo: programar_alarma
  args: [hora: HH:MM, mensaje]
  produce: notificación en pantalla a la hora dada

- id: programar_recordatorio
  tipo: funcion
  objetivo: programar_recordatorio
  args: [hora: HH:MM, dias[], mensaje]
  produce: notificación recurrente

- id: esperar
  tipo: funcion
  objetivo: esperar
  args: [segundos]
  produce: pausa dentro de un paquete
  nota: solo válido dentro de un paquete, no como comando suelto
```

### NOTIFICACIONES

```yaml
- id: notificar
  tipo: funcion
  objetivo: notificar
  args: [titulo, mensaje, duracion_seg]
  produce: toast de Windows visible al usuario
```

### WEB

```yaml
- id: abrir_url
  tipo: proceso
  objetivo: navegador (firefox | chrome | edge)
  args: [url]
  produce: URL abierta en navegador | APP_NO_ENCONTRADA

- id: consultar_web
  tipo: funcion
  objetivo: consultar_web
  args: [query]
  produce: resultado en consola
  nota: funcionalidad completa en Fase 2 con LLM
```

## Ejemplo de paquete

```yaml
id: "modo_estudio"
tipo: "paquete"
ejecucion: "instantanea"
on_error: "stop"
trigger:
  palabras_clave: ["modo estudio", "estudiar"]
schedule:
  hora: null
  dias: []
acciones:
  - tipo: proceso
    objetivo: firefox.exe
    args: ["https://notion.so"]
  - tipo: proceso
    objetivo: code.exe
    args: ["C:/proyectos/mi_proyecto"]
  - tipo: proceso
    objetivo: spotify.exe
    args: ["spotify:playlist:XYZ"]
```

## Detección de paquetes multi-palabra

Las `palabras_clave` de los paquetes se comparan como frase completa
(`" ".join(tokens)`), lo que permite triggers multi-palabra
como `"modo estudio"` sin necesidad de un solo token.
`classifier` une todos los tokens y verifica primero si la frase
completa coincide con algún nombre de paquete antes de evaluar
`tokens[0]` como verbo primitivo.

## Comandos destructivos

Todo comando con `guard: confirmar` interrumpe el flujo del paquete y espera decisión del usuario antes de ejecutar. Si el usuario cancela, se retorna `ACCION_CANCELADA` y el paquete completo se detiene.

Comandos destructivos en Fase 1:
- `eliminar_archivo`
