# Documentación de Taller MS Getter

Este servicio obtiene datos de licitaciones desde la API de Mercado Público y publica mensajes en Redis.
Encargado de centralizar y distribuir la información para su posterior procesamiento.

## Funcionalidades

- Obtiene datos de licitaciones desde la API de Mercado Público
- Publica mensajes en Redis para procesamiento posterior
- Manejo de errores y registros detallados
- Solicitudes HTTP resilientes con manejo de tiempo de espera (timeout)

## Configuración

Configura las siguientes variables de entorno:

- `REDIS_HOST`: Dirección del servidor Redis
- `REDIS_PORT`: Puerto del servidor Redis
- `API_KEY_MERCADO_PUBLICO`: Clave de API para Mercado Público

## Instalación

```bash
pip install -r requirements.txt
```
## Automatizaciones

Esta plantilla posee automatizaciones en base al uso de archivos Makefile.

Estos archivo automatizan tareas comunes para el desarrollo y mantenimiento del proyecto. Cada comando puede ejecutarse con make <comando> desde la terminal.

### Calidad y seguridad de código
- precommit: ejecuta herramientas de formateo y chequeo de calidad:

    - **black**: formatea el código.
    - **ruff**: verifica estilo y errores, en caso de que encuentre, los corrige


## Uso

```bash
python app.py
```

## Pruebas

### Requisitos previos

Install test dependencies:
```bash
pip install -r requirements.txt
```

### Prueba rápida (sin dependencias adicionales)

Ejecutar una prueba básica de estructura:
```bash
python test_simple.py
```

### Conjunto completo de pruebas (requiere pytest)

Instalar pytest y ejecutar todas las pruebas:
```bash
# Instalar pytest si no está instalado
pip install pytest pytest-mock pytest-cov responses

# Ejecutar todas las pruebas con reporte de cobertura
python run_tests.py

# Ejecutar pruebas en modo rápido (sin cobertura)
python run_tests.py --fast

# Ejecutar directamente con pytest
pytest tests/ -v
```

### Cobertura de pruebas

El conjunto de pruebas incluye:

- Pruebas unitarias para todas las funciones
- Pruebas de integración para flujos completos
- Pruebas de manejo de errores
- Simulación de dependencias externas (mocking)

Consulta `tests/README.md` para documentación detallada de las pruebas.

## Docker

Compilar y ejecutar con Docker:

```bash
docker build -t getter-service .
docker run -e REDIS_HOST=<host-redis> -e API_KEY_MERCADO_PUBLICO=<api-key> getter-service
```

## Registro (Logging)

El servicio genera registros tanto en consola como en archivo (getter_service.log) con información detallada sobre:

- Intentos y respuestas de solicitudes HTTP
- Operaciones con Redis
- Condiciones de error y trazas de pila
- Progreso del procesamiento