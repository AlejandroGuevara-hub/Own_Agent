# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.x (Fase 1) | ✅ |

## Reporting a Vulnerability

Este proyecto se ejecuta localmente en tu máquina y no expone servicios de red.
Sin embargo, si encuentras una vulnerabilidad de seguridad:

1. **No abras un issue público.**
2. Envía un email a [diego@example.com] (reemplazar con email real).
3. Describe el problema, incluyendo pasos para reproducirlo.
4. Recibirás una respuesta en un plazo de 48 horas hábiles.

## Consideraciones de seguridad

- Los comandos `eliminar_archivo` requieren confirmación explícita del usuario
  (guard clause con máximo 3 intentos).
- Los procesos externos se lanzan con `subprocess.Popen` sin shell=True
  para evitar inyección de comandos.
- No se ejecuta código remoto ni se descargan recursos externos
  (excepto futura integración con LLM local).
