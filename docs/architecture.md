# Arquitectura propuesta

## Objetivo

Construir un sistema automatizado y reproducible que recolecte datos competitivos de Rappi, Uber Eats y DiDi Food, normalice la informacion y genere insights accionables para Strategy, Pricing y Operations.

## Principios

1. Pragmatismo: mejor pocas direcciones bien medidas que mucho dato fragil.
2. Reproducibilidad: un comando debe generar datos, analisis y reporte.
3. Resiliencia: el scraping puede fallar; siempre debe existir backup de datos pre-scrapeados.
4. Trazabilidad: conservar raw output, logs y notas de disponibilidad.
5. Accionabilidad: cada insight debe terminar en una recomendacion operacional o comercial.

## Componentes

- `collectors`: un collector por plataforma.
- `raw data`: salida cruda por observacion.
- `analysis`: limpieza, metricas comparativas e indices.
- `reports`: insights y visualizaciones.
- `dashboard`: vista ejecutiva para exploracion.

## Estrategia de scraping live

Para produccion o una segunda iteracion:

- Usar Playwright por plataforma.
- Correr con browser persistente para mantener sesion controlada.
- Aplicar rate limiting y delays.
- Guardar screenshots como evidencia.
- Manejar productos no disponibles como dato, no como error.
- Separar selectores por plataforma.
- Si hay bloqueos, evaluar APIs no oficiales o proveedores como ScraperAPI/Bright Data documentando costos.

## Por que no n8n como core

n8n es bueno para orquestacion, alertas y workflows visibles. Pero el brief evalua calidad de scraping, robustez, manejo de errores, output estructurado y diseno tecnico. Eso se defiende mejor con Python modular. n8n podria ejecutar el pipeline, enviar alertas por Slack o publicar reportes, pero no reemplaza el core tecnico.
