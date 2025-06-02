# MSSQL Coding Case - BNL Base

Este repositorio contiene la base del proyecto para el coding case de MSSQL.

## Requisitos previos

- Python 3.x instalado  
- [Poetry](https://python-poetry.org/docs/#installation) instalado para la gestión de dependencias

## Cómo ejecutar el servidor

1. Clona este repositorio y navega a la raíz del proyecto.  
2. Instala las dependencias utilizando Poetry:

    ```bash
    poetry install
    ```

3. Activa el entorno virtual de Poetry (opcional si no se activa automáticamente):

    ```bash
    poetry shell
    ```

4. Ejecuta el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```

5. Accede a la documentación de los endpoints en tu navegador en:

    ```text
    http://localhost:8000/schema/swagger
    ```

## Estructura del proyecto

- `bnl/base/` - Contiene la configuración base y módulos principales del proyecto.
- `manage.py` - Script para tareas administrativas de Django.

## Notas

- Asegúrate de tener configurada la base de datos correctamente en `settings.py`.
- Para más información sobre los endpoints, consulta la documentación Swagger en la ruta mencionada arriba.
