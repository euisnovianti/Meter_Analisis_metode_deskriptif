import streamlit as st
import pandas as pd
from src.data_loader import render_sidebar_uploader
from src.visualizer import (
    plot_target_vs_realisasi_ulp,
    plot_reading_verification_donut,
    plot_hourly_distribution
)

st.set_page_config(
    page_title="Dashboard Overview - SIPERTI-UP3 GARUT",
    page_icon=":material/dashboard:",
    layout="wide"
)

from src.ui import render_material_symbols, render_global_filter_bar, apply_global_filters

render_material_symbols()
render_sidebar_uploader()

if not st.session_state.get("data_ready", False) or st.session_state.get("raw_data") is None:
    st.info("Silakan unggah file Excel melalui menu di sidebar sebelah kiri.")
    st.stop()

st.title(":material/dashboard: Executive Overview & Global Filter")
st.markdown("Ringkasan metrik operasional dan pemantauan real-time pembacaan meter listrik.")

render_global_filter_bar(st.session_state["raw_data"])
df_filtered = apply_global_filters(st.session_state["raw_data"])

st.markdown("---")

# --- 2. KARTU KPI GLOBAL UTAMA ---
st.markdown("### :material/monitoring: Ringkasan Kinerja Global")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

total_target = len(df_filtered)
total_normal = len(df_filtered[df_filtered["DLPD"].str.contains("NORMAL", case=False, na=False)])
pct_normal = (total_normal / total_target * 100) if total_target > 0 else 0
total_petugas = df_filtered["KD_PETUGAS"].nunique()

with col_kpi1:
    st.metric(label="Total Target Pelanggan", value=f"{total_target:,}")
with col_kpi2:
    st.metric(label="Total Meter Terbaca (%)", value=f"{pct_normal:.2f}%")
with col_kpi3:
    st.metric(label="Jumlah Petugas Aktif", value=f"{total_petugas:,}")

st.markdown("---")

# --- 3. TATA LETAK GRAFIK SECARA VERTIKAL BERURUTAN ---

# 1. Bar Chart: Target vs Realisasi ULP
st.subheader(":material/bar_chart: Target vs Realisasi Pembacaan per ULP")
fig_bar = plot_target_vs_realisasi_ulp(df_filtered)
st.plotly_chart(fig_bar, use_container_width=True)


# 2. Donut Chart: Status Verifikasi Bacaan
st.subheader(":material/pie_chart: Status Verifikasi Bacaan Lapangan")
fig_donut = plot_reading_verification_donut(df_filtered)
st.plotly_chart(fig_donut, use_container_width=True)

# 3. Line/Histogram Chart: Tren Jam Pembacaan (Hourly)
st.subheader(":material/schedule: Tren Jam Pembacaan (Hourly Distribution)")
fig_hour = plot_hourly_distribution(df_filtered)
st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")

# --- 4. TABEL RINGKASAN REKAPITULASI OPERASIONAL ---
st.subheader(":material/table_chart: Ringkasan Kinerja Operasional per ULP")

df_summary = df_filtered.groupby("ULP").agg(
    Target_Pelanggan=("IDPEL", "count"),
    Sukses_Normal=("DLPD", lambda x: (x.str.upper() == "NORMAL").sum()),
    Kendala_Anomali=("DLPD", lambda x: (x.str.upper() != "NORMAL").sum()),
    Petugas_Aktif=("KD_PETUGAS", "nunique"),
    Total_Pemakaian_kWh=("PEMKWH", "sum")
).reset_index()

df_summary["% Keberhasilan"] = (df_summary["Sukses_Normal"] / df_summary["Target_Pelanggan"] * 100).round(2).astype(str) + "%"

st.dataframe(
    df_summary[[
        "ULP", "Target_Pelanggan", "Sukses_Normal", 
        "Kendala_Anomali", "% Keberhasilan", "Petugas_Aktif", "Total_Pemakaian_kWh"
    ]].rename(columns={
        "Target_Pelanggan": "Target",
        "Sukses_Normal": "Normal",
        "Kendala_Anomali": "Anomali",
        "Petugas_Aktif": "Petugas Aktif",
        "Total_Pemakaian_kWh": "Total kWh"
    }),
    use_container_width=True,
    hide_index=True
)