# Pruebas para el Servicio Getter

Este directorio contiene pruebas completas para el archivo `app.py` del servicio getter.

---

## Estructura de Pruebas

- `test_app.py` – Archivo principal de pruebas con tests unitarios e integrados
- `conftest.py` – Configuración de Pytest y *fixtures*
- `README.md` – Este archivo de documentación

---

## Categorías de Pruebas

### Pruebas Unitarias

- **TestSendFunction**: Pruebas para la función `send()`
  - Caso exitoso
  - Manejo de errores de Redis
  - Manejo de errores inesperados

- **TestMakeRequestFunction**: Pruebas para la función `make_request()`
  - Solicitudes HTTP exitosas
  - Manejo de errores HTTP
  - Manejo de errores de decodificación JSON
  - Manejo de errores inesperados

- **TestMainFunction**: Pruebas para la función `main()`
  - Ejecución exitosa
  - Manejo de respuestas inválidas
  - Lista de licitaciones vacía
  - Manejo de errores en licitaciones individuales
  - Manejo de errores críticos

---

### Pruebas de Integración

- **TestIntegration**: Pruebas de flujo de trabajo de extremo a extremo
  - Flujo completo desde llamadas a la API hasta publicación en Redis

---

## Ejecución de Pruebas

### Requisitos Previos

Instalar las dependencias de prueba:

```bash
pip install -r requirements.txt
```

### Ejecutar todas las pruebas con cobertura
```bash
python run_tests.py
```

### Ejecutar en modo rápido (sin cobertura)
```bash
python run_tests.py --fast
```

### Ejecutar con `pytest` directamente
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con reporte de cobertura
pytest --cov=app --cov-report=html

# Ejecutar una clase de prueba específica
pytest tests/test_app.py::TestSendFunction

# Ejecutar un método de prueba específico
pytest tests/test_app.py::TestSendFunction::test_send_success
```

###  Ejecutar pruebas por categoría
```bash
# Solo pruebas unitarias
pytest -m unit

# Solo pruebas de integración
pytest -m integration
```

## Cobertura de Pruebas

Las pruebas cubren:
- ✅ Todas las funciones públicas (`send`, `make_request`, `main`)
- ✅ Escenarios exitosos
- ✅ Manejo de errores para todos los tipos principales
- ✅ Casos límite (respuestas vacías, datos inválidos)
- ✅ Flujos de integración completos
- ✅  Comportamiento del registro (logging, deshabilitado durante las pruebas)

## Datos de Prueba

Las pruebas utilizan datos simulados que imitan las respuestas reales de la API:

-Lista de licitaciones con múltiples entradas
-Detalles individuales de licitaciones
-Estructura de mensajes esperada para la publicación en Redis

## Estrategia de Mocking

- **Redis**: Simulado para evitar requerir una instancia real
- **Solicitudes HTTP**: Simuladas para evitar llamadas reales a la API externa
- **Configuración**: Variables de entorno configuradas para testing
- **Logging**: Desactivado durante las pruebas para evitar ruido en la salida

## Agregar Nuevas Pruebas

Cuando se agregue nueva funcionalidad en `app.py`:

1. Agregar métodos de prueba correspondientes en la clase adecuada
2. Usar fixtures existentes desde conftest.py
3. Seguir el patrón Arrange–Act–Assert
4. Probar tanto escenarios exitosos como fallidos
5. Actualizar este README si se agregan nuevas categorías de pruebas