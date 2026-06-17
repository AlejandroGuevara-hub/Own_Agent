# Deployment Guide

## Requisitos del sistema

- Windows 10 u 11 (64-bit)
- Python 3.11 o superior
- Conexión a internet (solo para instalación de paquetes)
- Permisos de administrador (para control de audio y notificaciones)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd agente-personal
```

### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar

```bash
python main.py
```

## Uso como servicio de Windows (opcional)

Para que el agente se ejecute al iniciar sesión:

1. Crear un acceso directo a `python main.py` en:
   `shell:startup`

2. O usar el Programador de tareas de Windows:
   - Crear tarea básica
   - Disparador: "Al iniciar sesión"
   - Acción: Iniciar programa → `python` con argumento `main.py`

## Despliegue como ejecutable (opcional)

```bash
pip install pyinstaller
pyinstaller --onefile --console main.py
```

El ejecutable estará en `dist/main.exe`.

## Configuración de paquetes personalizados

Editar `commands/packages.yaml` con la estructura documentada. No requiere
modificar código ni reiniciar el agente (la recarga en caliente estará en Fase 2).

## Logs

Actualmente no hay sistema de logs implementado. Los eventos se muestran
en consola. Planeado para completitud de Fase 1.
