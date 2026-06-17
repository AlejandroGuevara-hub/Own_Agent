# Changelog

## [Unreleased]

### Added
- Proyecto inicial — Agente Personal de Automatización
- Módulo interpreter: tokenizer, classifier, builder
- Módulo executor: processes, functions, dispatcher
- Módulo scheduler (stub — implementación pendiente)
- Módulo notifier con rich y winotify
- Módulo config con carga de YAML
- Comandos primitivos: abrir_proceso, ajustar_volumen, esperar, notificar
- Paquetes predefinidos: modo_estudio, iniciar_jornada, apagar_todo
- Sistema de errores uniforme con ErrorAgente
- Especificaciones completas en spec/

### Pending (Fase 1)
- Implementación de scheduler con APScheduler
- Implementación de: ajustar_brillo, consultar_sistema, cerrar_proceso,
  listar_procesos, mover_archivo, crear_archivo, eliminar_archivo,
  programar_alarma, programar_recordatorio
- Sistema de logging a archivos
