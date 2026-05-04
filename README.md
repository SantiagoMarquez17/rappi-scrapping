# Rappi Competitive Intelligence

Sistema de inteligencia competitiva para comparar Rappi frente a Uber Eats y DiDi Food en Mexico usando productos, direcciones y metricas operativas estandarizadas.

El proyecto genera un dataset estructurado, calcula brechas competitivas, produce visualizaciones y entrega un dashboard ejecutivo para explorar hallazgos por ciudad, zona, producto y plataforma.

## Alcance

- **Plataformas:** Rappi, Uber Eats y DiDi Food.
- **Mercado:** Mexico.
- **Cobertura geografica:** 20 direcciones representativas en CDMX, Guadalajara, Monterrey, Puebla y Queretaro.
- **Tipos de zona:** premium, corporativa, alta demanda, residencial, periferica, turistica y universitaria.
- **Productos comparables:** Big Mac, combo mediano, nuggets, Coca-Cola 500ml y agua 1L.
- **Metricas:** precio del producto, delivery fee, service fee, descuento, disponibilidad, ETA y total estimado.

## Arquitectura

```text
Direcciones + productos de referencia
        |
        v
Collectors por plataforma
        |
        v
Datos raw estandarizados
        |
        v
Limpieza y normalizacion
        |
        v
Indice competitivo vs Rappi
        |
        v
Insights + graficos + dashboard
```

## Estructura del repositorio

```text
.
+-- dashboard/
|   +-- app.py
+-- data/
|   +-- raw/
|   |   +-- competitive_raw.csv
|   +-- processed/
|       +-- competitive_clean.csv
|       +-- competitive_index.csv
+-- docs/
|   +-- architecture.md
|   +-- live_scraping_strategy.md
+-- reports/
|   +-- charts/
|   +-- insights.md
+-- src/
|   +-- analysis.py
|   +-- collectors.py
|   +-- config.py
|   +-- locations.py
|   +-- pipeline.py
|   +-- sample_data.py
+-- requirements.txt
+-- README.md
```

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion del pipeline

El pipeline completo se ejecuta con:

```bash
python -m src.pipeline --mode sample
```

Este comando genera:

- `data/raw/competitive_raw.csv`
- `data/processed/competitive_clean.csv`
- `data/processed/competitive_index.csv`
- `reports/insights.md`
- graficos en `reports/charts/`

## Dashboard

Para abrir el dashboard interactivo:

```bash
streamlit run dashboard/app.py
```

El dashboard permite filtrar por ciudad, tipo de zona y producto. Incluye KPIs principales, comparacion de precio final, fees por zona, distribucion de ETA y tabla competitiva vs Rappi.

## Datos generados

El repositorio incluye un dataset reproducible para validar el flujo end-to-end sin depender de disponibilidad externa de plataformas durante la evaluacion.

Columnas principales:

- `platform`
- `city`
- `zone`
- `zone_type`
- `address_id`
- `product`
- `available`
- `product_price_mxn`
- `delivery_fee_mxn`
- `service_fee_mxn`
- `discount_mxn`
- `eta_min_minutes`
- `eta_max_minutes`
- `final_total_mxn`

## Outputs analiticos

El analisis calcula:

- Total estimado promedio por plataforma.
- Fee total promedio por plataforma y tipo de zona.
- ETA promedio por plataforma.
- Disponibilidad por plataforma.
- Brecha de precio, fee y ETA de competidores contra Rappi por producto y direccion.

Los principales hallazgos se encuentran en:

```text
reports/insights.md
```

## Estrategia de scraping live

La implementacion esta organizada para reemplazar o extender los collectors actuales con flujos live por plataforma usando Playwright, APIs no oficiales o proveedores especializados de scraping.

La estrategia propuesta esta documentada en:

```text
docs/live_scraping_strategy.md
```

## Consideraciones eticas y operativas

- Aplicar rate limiting y delays razonables.
- No sobrecargar servicios externos.
- Registrar errores, bloqueos y datos no disponibles.
- Conservar evidencia cuando sea posible.
- Validar terminos de servicio y consideraciones legales antes de un despliegue productivo.

## Comando rapido

```bash
python -m src.pipeline --mode sample
streamlit run dashboard/app.py
```
