# Arquitectura

## Objetivo

Construir un sistema automatizado y reproducible que recolecte datos competitivos de Rappi, Uber Eats y DiDi Food, normalice la informacion y genere insights accionables para Strategy, Pricing y Operations.

## Principios

1. Pragmatismo: mejor pocas direcciones bien medidas que mucho dato fragil.
2. Reproducibilidad: un comando debe generar datos, analisis y reporte.
3. Resiliencia: el scraping puede fallar; siempre debe existir backup de datos pre-scrapeados.
4. Trazabilidad: conservar raw output, logs y notas de disponibilidad.
5. Accionabilidad: cada insight debe terminar en una recomendacion operacional o comercial.

## Componentes

- `locations`: catalogo de direcciones representativas y justificacion geografica.
- `collectors`: interfaz comun para recolectar datos por plataforma.
- `raw data`: salida cruda estandarizada por observacion.
- `analysis`: limpieza, metricas comparativas e indice competitivo.
- `reports`: insights y visualizaciones.
- `dashboard`: vista ejecutiva para exploracion.

## Flujo de datos

1. Se define una matriz de direcciones, plataformas y productos comparables.
2. Cada collector devuelve filas con el mismo contrato de datos.
3. El pipeline guarda la salida raw para trazabilidad.
4. El modulo de analisis normaliza tipos numericos y calcula metricas derivadas.
5. El indice competitivo compara competidores contra Rappi al mismo nivel de producto y direccion.
6. Se generan graficos, reporte de insights y dashboard.

## Estrategia de scraping live

Para una version productiva:

- Usar Playwright por plataforma.
- Correr con browser persistente para mantener sesion controlada.
- Aplicar rate limiting y delays.
- Guardar screenshots como evidencia.
- Manejar productos no disponibles como dato, no como error.
- Separar selectores por plataforma.
- Si hay bloqueos, evaluar APIs no oficiales o proveedores como ScraperAPI/Bright Data documentando costos.
