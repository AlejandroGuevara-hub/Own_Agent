# ADR-001: Arquitectura de Capas con Orquestador

## Estado

Aceptado

## Contexto

El proyecto necesita separar responsabilidades para permitir escalabilidad
desde comandos fijos hasta lenguaje natural y voz sin reescribir componentes.

## Decisión

Usar una arquitectura de capas con un orquestador central (`main.py`):

```
[Entrada] → [Interpreter] → [Executor] → [OS]
               ↕                ↕
          [Config / Models]  [Scheduler / Notifier]
```

- **Orquestador:** coordina el flujo pero no contiene lógica de negocio.
- **Contratos:** `Intencion`, `Accion`, `ErrorAgente` como dataclasses compartidas.
- **Fail-fast:** ante el primer error se detiene todo.
- **Salida centralizada:** solo `notifier` produce output.

## Consecuencias

- Positivas: módulos reemplazables, testing aislado, escalabilidad por módulo.
- Negativas: overhead de indirección para tareas simples.
- Riesgo: el orquestador puede convertirse en bottleneck si crece sin control.

## Referencias

- `spec/modules.md` — definición de cada módulo
- `spec/architecture.md` — diagramas y contratos
