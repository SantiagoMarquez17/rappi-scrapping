from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.config import CHARTS_DIR, REPORTS_DIR


def clean(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize raw collector output and add metrics used downstream."""
    df = raw_df.copy()
    numeric_cols = [
        "product_price_mxn",
        "delivery_fee_mxn",
        "service_fee_mxn",
        "discount_mxn",
        "eta_min_minutes",
        "eta_max_minutes",
        "final_total_mxn",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ETA and fees are modeled as explicit derived fields because they are
    # central to pricing, operations and strategy comparisons.
    df["eta_avg_minutes"] = (df["eta_min_minutes"] + df["eta_max_minutes"]) / 2
    df["fee_total_mxn"] = df["delivery_fee_mxn"] + df["service_fee_mxn"]
    df["is_rappi"] = df["platform"].eq("Rappi")
    return df


def build_competitive_index(df: pd.DataFrame) -> pd.DataFrame:
    """Compare each competitor against Rappi for the same product and address."""
    keys = ["city", "zone", "address_id", "product"]
    rappi = (
        df[df["platform"] == "Rappi"][keys + ["final_total_mxn", "eta_avg_minutes", "fee_total_mxn"]]
        .rename(
            columns={
                "final_total_mxn": "rappi_total",
                "eta_avg_minutes": "rappi_eta",
                "fee_total_mxn": "rappi_fees",
            }
        )
    )
    competitors = df[df["platform"] != "Rappi"].copy()
    out = competitors.merge(rappi, on=keys, how="left")
    # Positive values mean Rappi is higher than the competitor for that metric.
    out["total_gap_vs_rappi_pct"] = (out["rappi_total"] - out["final_total_mxn"]) / out["final_total_mxn"]
    out["eta_gap_vs_rappi_min"] = out["rappi_eta"] - out["eta_avg_minutes"]
    out["fee_gap_vs_rappi_pct"] = (out["rappi_fees"] - out["fee_total_mxn"]) / out["fee_total_mxn"]
    return out


def generate_charts(df: pd.DataFrame, competitive: pd.DataFrame) -> None:
    """Create static charts that can be embedded in a report or presentation."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    price = df.groupby("platform", as_index=False)["final_total_mxn"].mean().dropna()
    price.plot(kind="bar", x="platform", y="final_total_mxn", legend=False, color="#ff6b35")
    plt.title("Total estimado promedio por plataforma")
    plt.ylabel("MXN")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "avg_total_by_platform.png")
    plt.close()

    eta = df.groupby("platform", as_index=False)["eta_avg_minutes"].mean().dropna()
    eta.plot(kind="bar", x="platform", y="eta_avg_minutes", legend=False, color="#2f80ed")
    plt.title("ETA promedio por plataforma")
    plt.ylabel("Minutos")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "avg_eta_by_platform.png")
    plt.close()

    fees = df.groupby(["zone_type", "platform"], as_index=False)["fee_total_mxn"].mean().dropna()
    pivot = fees.pivot(index="zone_type", columns="platform", values="fee_total_mxn")
    pivot.plot(kind="bar")
    plt.title("Fees promedio por tipo de zona")
    plt.ylabel("MXN")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "fees_by_zone_type.png")
    plt.close()


def write_insights(df: pd.DataFrame, competitive: pd.DataFrame, output_path: Path | None = None) -> Path:
    """Write an executive markdown report with findings, impact and actions."""
    output_path = output_path or REPORTS_DIR / "insights.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    avg_total = df.groupby("platform")["final_total_mxn"].mean().sort_values()
    avg_eta = df.groupby("platform")["eta_avg_minutes"].mean().sort_values()
    avg_fee = df.groupby("platform")["fee_total_mxn"].mean().sort_values()
    availability = df.groupby("platform")["available"].mean().sort_values(ascending=False)
    rappi_vs_comp = competitive.groupby("platform")[["total_gap_vs_rappi_pct", "eta_gap_vs_rappi_min", "fee_gap_vs_rappi_pct"]].mean()

    # Build the markdown table without optional pandas dependencies.
    table_rows = [
        "| Competidor | Brecha total vs Rappi | Brecha ETA vs Rappi | Brecha fees vs Rappi |",
        "| --- | ---: | ---: | ---: |",
    ]
    for platform, row in rappi_vs_comp.iterrows():
        table_rows.append(
            f"| {platform} | {row['total_gap_vs_rappi_pct'] * 100:.1f}% | "
            f"{row['eta_gap_vs_rappi_min']:.1f} min | {row['fee_gap_vs_rappi_pct'] * 100:.1f}% |"
        )
    rappi_vs_comp_table = "\n".join(table_rows)

    most_expensive_zone = (
        competitive.groupby("zone_type")["total_gap_vs_rappi_pct"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )

    content = f"""# Competitive Intelligence - Top Insights

## Resumen ejecutivo

Dataset con {len(df):,} observaciones, {df['address_id'].nunique()} direcciones, {df['product'].nunique()} productos y {df['platform'].nunique()} plataformas.

## Insight 1: Posicionamiento de precio total

Finding: La plataforma con menor total estimado promedio es **{avg_total.index[0]}** (${avg_total.iloc[0]:.0f} MXN), mientras Rappi promedia ${avg_total.get('Rappi', 0):.0f} MXN.

Impacto: El precio final es la metrica que el usuario percibe al checkout; pequenas diferencias repetidas pueden mover conversion.

Recomendacion: Priorizar ajustes de precio total en productos comparables de alta frecuencia, no solo en precio base.

## Insight 2: Fees como palanca competitiva

Finding: La plataforma con fees promedio mas bajos es **{avg_fee.index[0]}** (${avg_fee.iloc[0]:.0f} MXN).

Impacto: Delivery fee y service fee pueden explicar por que una plataforma parece competitiva aunque el producto base no sea mas barato.

Recomendacion: Separar diagnostico entre precio producto y fees para decidir si conviene subsidio logistico o promocion comercial.

## Insight 3: Tiempo estimado de entrega

Finding: La mejor ETA promedio aparece en **{avg_eta.index[0]}** ({avg_eta.iloc[0]:.1f} min).

Impacto: En quick commerce y food delivery, ETA compite directamente contra precio cuando el usuario tiene urgencia.

Recomendacion: Usar zonas con brecha de ETA como input para balanceo de repartidores y disponibilidad de tiendas.

## Insight 4: Variabilidad geografica

Finding: La mayor brecha contra competidores aparece en zonas tipo **{most_expensive_zone}**.

Impacto: Una estrategia nacional promedio puede esconder problemas locales fuertes.

Recomendacion: Crear reglas por zona: premium, periferica, residencial y corporativa deben tener thresholds distintos.

## Insight 5: Disponibilidad

Finding: La mejor disponibilidad observada es **{availability.index[0]}** ({availability.iloc[0] * 100:.1f}%).

Impacto: Si el restaurante/producto no esta disponible, precio y promociones dejan de importar.

Recomendacion: Incluir disponibilidad como metrica primaria del tablero competitivo y alertar caidas por zona.

## Tabla: Rappi vs competidores

{rappi_vs_comp_table}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
