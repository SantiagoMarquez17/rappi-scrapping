from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT_DIR / "data" / "processed" / "competitive_clean.csv"
INDEX_PATH = ROOT_DIR / "data" / "processed" / "competitive_index.csv"

st.set_page_config(page_title="Rappi Competitive Intelligence", layout="wide")
st.title("Competitive Intelligence")

if not CLEAN_PATH.exists():
    st.warning("Ejecuta primero: python -m src.pipeline --mode sample")
    st.stop()

# The dashboard reads generated artifacts instead of recomputing metrics so it
# stays aligned with the reproducible pipeline outputs.
df = pd.read_csv(CLEAN_PATH)
index_df = pd.read_csv(INDEX_PATH)

city = st.sidebar.multiselect("Ciudad", sorted(df["city"].unique()), default=sorted(df["city"].unique()))
zone_type = st.sidebar.multiselect("Tipo de zona", sorted(df["zone_type"].unique()), default=sorted(df["zone_type"].unique()))
product = st.sidebar.multiselect("Producto", sorted(df["product"].unique()), default=sorted(df["product"].unique()))

filtered = df[df["city"].isin(city) & df["zone_type"].isin(zone_type) & df["product"].isin(product)]

# Executive KPIs summarize coverage and the commercial/operational baseline for
# the selected filters.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Observaciones", f"{len(filtered):,}")
col2.metric("Direcciones", filtered["address_id"].nunique())
col3.metric("Total promedio", f"${filtered['final_total_mxn'].mean():.0f} MXN")
col4.metric("ETA promedio", f"{filtered['eta_avg_minutes'].mean():.1f} min")

st.subheader("Precio final promedio")
fig_price = px.bar(
    filtered.groupby("platform", as_index=False)["final_total_mxn"].mean(),
    x="platform",
    y="final_total_mxn",
    color="platform",
    text_auto=".0f",
)
st.plotly_chart(fig_price, use_container_width=True)

st.subheader("Fees por tipo de zona")
fig_fees = px.bar(
    filtered.groupby(["zone_type", "platform"], as_index=False)["fee_total_mxn"].mean(),
    x="zone_type",
    y="fee_total_mxn",
    color="platform",
    barmode="group",
)
st.plotly_chart(fig_fees, use_container_width=True)

st.subheader("ETA promedio por plataforma")
fig_eta = px.box(filtered, x="platform", y="eta_avg_minutes", color="platform")
st.plotly_chart(fig_eta, use_container_width=True)

st.subheader("Rappi vs competidores")
st.dataframe(index_df, use_container_width=True)
