# Glosario Técnico

| Término | Definición |
|---|---|
| **Accion** | Unidad mínima ejecutable. Puede ser un proceso externo o una función interna. |
| **APScheduler** | Librería Python para programación de tareas (cron, intervalos, fechas). |
| **Builder** | Componente del intérprete que construye objetos `Intencion` a partir de tokens. |
| **Classifier** | Componente del intérprete que determina si un comando es primitiva o paquete. |
| **Dispatcher** | Diccionario que mapea nombres de funciones a sus implementaciones en `executor`. |
| **ErrorAgente** | Objeto de error uniforme que encapsula código, origen, detalle y acción fallida. |
| **Fail-fast** | Política por la cual ante el primer error se detiene toda la ejecución del paquete. |
| **Guard clause** | Mecanismo de seguridad que requiere confirmación del usuario antes de ejecutar comandos destructivos. |
| **Intencion** | Contrato de datos entre intérprete y ejecutor. Representa un comando parseado. |
| **Notifier** | Módulo centralizado para toda salida al usuario (consola rich + notificaciones toast). |
| **Paquete** | Secuencia de acciones definida en YAML que se ejecuta en orden. |
| **Primitiva** | Comando atómico que ejecuta una sola acción (proceso o función). |
| **Scheduler** | Gestor de tareas programadas (basado en APScheduler). |
| **Tokenizer** | Componente que divide el texto crudo en tokens por espacios. |
| **Toast** | Notificación nativa de Windows (esquina inferior derecha). |
| **Verbos ambiguos** | Verbos que pueden corresponder a múltiples primitivas (ej. `consultar` → sistema o web). |
| **YAML** | Formato de serialización usado para definir comandos y paquetes. |
