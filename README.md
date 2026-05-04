# Rappi Competitive Intelligence MVP

Sistema tecnico para recolectar, estructurar y analizar senales competitivas de Rappi, Uber Eats y DiDi Food en Mexico.

## Decision de arquitectura

El brief pesa 70% en scraping, por eso el core esta en Python y no en n8n. n8n puede orquestar ejecuciones, alertas o webhooks, pero el scraping, normalizacion, trazabilidad y analisis quedan en codigo para demostrar robustez tecnica.

```text
Direcciones + productos
        |
        v
Collectors por plataforma
        |
        v
Raw JSON/CSV con evidencia
        |
        v
Normalizacion ETL
        |
        v
Dataset analitico
        |
        v
Insights + visualizaciones + dashboard
```

## Scope del MVP

- Plataformas: Rappi, Uber Eats, DiDi Food.
- Mercado: Mexico.
- Direcciones: 20 direcciones representativas, agrupadas por tipo de zona.
- Productos comparables: Big Mac, combo mediano, nuggets, Coca-Cola 500ml, agua 1L.
- Metricas: precio producto, delivery fee, service fee, tiempo estimado, descuentos, disponibilidad y total estimado.
- Plan B de demo: modo `sample`, con datos pre-scrapeados reproducibles.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar pipeline

Modo seguro para demo:

```bash
python -m src.pipeline --mode sample
```

Modo live placeholder:

```bash
python -m src.pipeline --mode live
```

El modo `live` esta preparado para integrar Playwright o APIs no oficiales. En 2 dias, la recomendacion es entregar el modo `sample` completo y documentar la estrategia live con capturas/evidencia si se alcanza.

## Dashboard

```bash
streamlit run dashboard/app.py
```

## Outputs

- `data/raw/competitive_raw.csv`: datos recolectados o sample.
- `data/processed/competitive_clean.csv`: datos normalizados.
- `reports/insights.md`: top insights accionables.
- `reports/charts/`: graficos generados.

## Consideraciones eticas

- Rate limiting entre requests.
- No bypass agresivo de controles.
- No sobrecargar servidores.
- Documentar bloqueos y datos no disponibles.
- Consultar Legal antes de un despliegue sistematico real.

## Como presentar

1. Approach y scope: mostrar que se priorizo robustez sobre cantidad.
2. Demo: ejecutar `python -m src.pipeline --mode sample`.
3. Datos: abrir CSV raw y clean.
4. Insights: mostrar `reports/insights.md` y dashboard.
5. Decisiones tecnicas: collectors modulares, retries, logs, fallback.
6. Limitaciones: scraping dinamico, bloqueos, ToS, necesidad de proxies/cuentas controladas.
