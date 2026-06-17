# ADR-002: Manejo de Errores Uniforme con ErrorAgente

## Estado

Aceptado

## Contexto

Diferentes módulos necesitan reportar errores de forma consistente.
Evitar `print()` directo y excepciones sin contexto.

## Decisión

Todo error se representa como `ErrorAgente` (dataclass con `codigo`,
`origen`, `detalle`, `accion`). El módulo que detecta la falla construye
el objeto y lo retorna. `notifier` lo muestra al usuario.

- Nunca se usan excepciones para control de flujo.
- Nunca se imprime directamente desde los módulos.
- El catálogo de errores está documentado en `spec/cases.md`.

## Consecuencias

- Positivas: mensajes de error uniformes, fácil localizar origen, testing simplificado.
- Negativas: cada función debe retornar `str | ErrorAgente` en vez de lanzar excepción.
- Riesgo: olvidar construir ErrorAgente y dejar que una excepción CRUCE capas.
