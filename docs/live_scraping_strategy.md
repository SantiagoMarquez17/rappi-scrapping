# Estrategia de scraping live

## Objetivo

Extender los collectors actuales para recolectar informacion directamente desde las plataformas, manteniendo el mismo contrato de salida usado por el pipeline analitico.

## Implementacion con Playwright

Flujo por plataforma:

1. Abrir navegador con contexto persistente.
2. Cargar direccion o geolocalizacion.
3. Buscar restaurante/producto.
4. Extraer precio, ETA, delivery fee, service fee, descuentos y disponibilidad.
5. Guardar screenshot como evidencia.
6. Guardar raw HTML o JSON cuando sea posible.
7. Normalizar a las columnas estandar.

## Contrato de salida

Cada collector debe devolver una lista de diccionarios con las columnas esperadas por `src.analysis.clean`:

- `scraped_at`
- `platform`
- `city`
- `zone`
- `zone_type`
- `address_id`
- `address`
- `product`
- `restaurant`
- `available`
- `product_price_mxn`
- `delivery_fee_mxn`
- `service_fee_mxn`
- `discount_mxn`
- `eta_min_minutes`
- `eta_max_minutes`
- `final_total_mxn`
- `evidence_url`
- `notes`

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
