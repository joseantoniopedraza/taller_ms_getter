# Taller MS Getter

Microservicio que obtiene licitaciones de la API de Mercado Público y las publica en Redis.

## Docker

### Construir la imagen

```bash
docker build -t taller_ms_getter .
```

### Ejecutar el contenedor

```bash
docker run --rm -e REDIS_HOST=redis -e REDIS_PORT=6379 taller_ms_getter
```

### Usar con Docker Compose

El servicio ya está configurado en el `docker-compose.yml` principal. Para ejecutarlo:

```bash
docker-compose up taller_ms_getter
```

## Variables de entorno

- `REDIS_HOST`: Host de Redis (por defecto: localhost)
- `REDIS_PORT`: Puerto de Redis (por defecto: 6379)

## Dependencias

- Python 3.11
- redis[hiredis]
- requests 