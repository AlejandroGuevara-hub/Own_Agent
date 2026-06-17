# Troubleshooting

## Error: "No escribiste ningún comando."

**Causa:** Presionaste Enter sin escribir nada.

**Solución:** Escribe un comando válido. Usa `>>> abrir firefox` o `>>> modo estudio`.

## Error: "El comando 'X' no existe."

**Causa:** El verbo o palabra clave no está registrado.

**Soluciones:**
- Revisa los verbos disponibles en `README.md`
- Si es un paquete, verifica que esté definido en `commands/packages.yaml`
- Los comandos son sensibles a mayúsculas/minúsculas (todo minúsculas)

## Error: "La aplicación 'X' no está instalada o la ruta es incorrecta."

**Causa:** El ejecutable no se encuentra en PATH o la ruta es incorrecta.

**Soluciones:**
- Verifica que la app esté instalada
- Usa la ruta completa al ejecutable (ej. `C:\Program Files\Firefox\firefox.exe`)
- Agrega la ubicación al PATH del sistema

## Error: "El nivel debe ser un número entero entre 0 y 100."

**Causa:** El argumento de `ajustar volumen` no es un número válido.

**Solución:** Usa un entero entre 0 y 100. Ejemplo: `ajustar volumen 50`.

## Error: "Parámetros insuficientes para 'esperar'"

**Causa:** No se proporcionó la cantidad de segundos.

**Solución:** Usa `esperar 10` (o cualquier entero positivo).

## Error: "Parámetros insuficientes para 'notificar'"

**Causa:** Faltan argumentos (título, mensaje, duración).

**Solución:** Usa `notificar "Titulo" "Mensaje" 5`.

## La notificación toast no aparece

**Causas posibles:**
- Windows 10/11: las notificaciones toast requieren que la app esté registrada
  (winotify lo maneja automáticamente, pero puede fallar en entornos muy restrictivos)
- Modo "No molestar" activado en Windows
- La aplicación no tiene foco (winotify puede fallar en segundo plano)

## El volumen no se ajusta

**Causas posibles:**
- Los controladores de audio no son compatibles con pycaw
- Ejecutar como administrador puede ser necesario en algunos sistemas
- Puede haber conflictos con apps que monopolizan el dispositivo de audio

## El comando no se reconoce pero existe en YAML

Verifica:
1. Que el archivo YAML tenga codificación UTF-8
2. Que la indentación sea correcta (2 espacios)
3. Que `primitives.yaml` no tenga errores de sintaxis (tipos como `sched ule:` en vez de `schedule:`)
