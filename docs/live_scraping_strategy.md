# Estrategia para scraping live

## Camino recomendado

En dos dias, no conviene prometer scraping perfecto de apps complejas. Conviene mostrar arquitectura, un MVP reproducible y un plan claro para live scraping.

## Implementacion con Playwright

Flujo por plataforma:

1. Abrir navegador con contexto persistente.
2. Cargar direccion o geolocalizacion.
3. Buscar restaurante/producto.
4. Extraer precio, ETA, delivery fee, service fee, descuentos y disponibilidad.
5. Guardar screenshot como evidencia.
6. Guardar raw HTML o JSON cuando sea posible.
7. Normalizar a las columnas estandar.

## Manejo de errores

- Producto no disponible: registrar `available=False`.
- Fee no visible antes de checkout: registrar `null` y nota.
- Sitio bloquea: registrar error, screenshot y continuar con otra plataforma.
- Timeout temporal: retry con backoff.
- Cambios de selector: aislar selectores por plataforma.

## Rate limiting

- Delay entre acciones.
- No paralelizar agresivamente.
- Limitar direcciones por corrida.
- Ejecutar en horarios definidos.

## Evidencia

Guardar por observacion:

- timestamp
- plataforma
- direccion
- producto
- screenshot path
- URL o estado
- notas de bloqueo

## Donde entra n8n

n8n puede:

- disparar el pipeline cada hora;
- enviar alertas a Slack;
- guardar outputs en Google Drive;
- notificar cambios grandes de precio;
- crear tickets para Strategy/Pricing.

Pero el scraping y analisis deben quedar en Python para mantener control, testabilidad y versionamiento.
