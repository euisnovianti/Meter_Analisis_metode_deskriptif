import streamlit as st
import pandas as pd
from src.data_loader import render_sidebar_uploader
from src.ui import apply_global_filters, render_global_filter_bar
from src.ui import render_material_symbols
from src.metrics_engine import calculate_performance_metrics
from src.visualizer import plot_daily_progression_bar

st.set_page_config(
    page_title="Rapor Petugas - SIPERTI",
    page_icon=":material/person:",
    layout="wide"
)

render_material_symbols()
render_sidebar_uploader()

# Guardrail: Cek data
if not st.session_state.get("data_ready", False) or st.session_state.get("raw_data") is None:
    st.info(":material/upload_file: Silakan unggah file Excel atau CSV melalui uploader di sidebar kiri.")
    st.stop()

render_global_filter_bar(st.session_state["raw_data"])
df = apply_global_filters(st.session_state["raw_data"])
if df.empty:
    st.warning(":material/warning: Tidak ada data yang cocok dengan filter global.")
    st.stop()

# Hitung metrik deskriptif
df_eval = calculate_performance_metrics(df)
if not df_eval.empty:
    sort_metric = st.session_state.get("desc_sort_by", "Volume Pembacaan Terbanyak")
    sort_col_map = {
        "Volume Pembacaan Terbanyak": ("Volume", False),
        "Ketercapaian Target Tertinggi": ("Ketercapaian", False),
        "Kendala Lapangan Terendah": ("Anomali", True)
    }
    sort_col, ascending = sort_col_map.get(sort_metric, ("Volume", False))
    
    df_eval.sort_values(by=[sort_col, "Volume"], ascending=[ascending, False], inplace=True)
    df_eval["Rank"] = range(1, len(df_eval) + 1)
    df_eval["Status"] = "N/A"

st.title(":material/person: RBM Performance Report (Rapor Rute)")
st.markdown("Evaluasi mendalam rekam jejak dan histori pembacaan meter per rute RBM menggunakan Metrik Historis.")

if df_eval.empty:
    st.error("Data tidak mencukupi untuk evaluasi rapor petugas.")
    st.stop()

# --- SELECTOR RBM ---
rbm_list = sorted(df_eval["KODE_RBM"].unique().tolist())
selected_rbm = st.selectbox("Pilih Kode RBM", options=rbm_list)

# Ambil data spesifik rute terpilih
officer_row = df_eval[df_eval["KODE_RBM"] == selected_rbm].iloc[0]
df_officer_logs = df[df["KODE_RBM_CLEAN"] == selected_rbm]

# --- PROFILE BANNER (Bento Style) ---
score_html = f"""
<div style="text-align:right;">
    <div style="font-size:12px; color:#444653; text-transform:uppercase;">Total Bacaan / Anomali</div>
    <div style="font-size:32px; font-weight:bold; color:#00288e;">{int(officer_row['Volume'])} / {int(officer_row['Volume'] * officer_row['Anomali'] / 100)}</div>
    <div style="font-size:14px; color:#00563a; font-weight:bold;">Rangking #{int(officer_row['Rank'])}</div>
</div>
"""

st.markdown(f"""
<div style="background-color:white; border:1px solid #c4c5d5; border-radius:12px; padding:24px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1); display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
    <div>
        <div style="font-size:12px; font-weight:bold; color:#1e40af; text-transform:uppercase;">Kode RBM: {selected_rbm}</div>
        <div style="font-size:24px; font-weight:bold; color:#191c1e; margin-top:4px;">ULP: {officer_row['ULP']}</div>
        <div style="font-size:14px; color:#444653; margin-top:4px;">Petugas: <b>{officer_row['Petugas_Bertugas']}</b> | Total Penugasan: <b>{officer_row['Total_Target']} Titik</b> | Ketercapaian: <b>{officer_row['Ketercapaian']:.1f}%</b></div>
    </div>
    {score_html}
</div>
""", unsafe_allow_html=True)

# --- RADAR CHART & DAILY PROGRESSION ---
st.subheader("Progres Pembacaan Harian (Hari A - E)")
fig_prog = plot_daily_progression_bar(df_officer_logs)
st.plotly_chart(fig_prog, use_container_width=True)

# --- CHRONOLOGICAL LOG TABLE ---
st.markdown("---")
st.subheader(f":material/history: Histori Log Pembacaan Lapangan — {selected_rbm}")

st.dataframe(
    df_officer_logs[[
        "IDPEL", "NAMA", "HARI_BACA_LABEL", 
        "TANGGAL_PEMBACAAN", "JAM_PEMBACAAN", "DLPD", "PEMKWH"
    ]].rename(columns={
        "HARI_BACA_LABEL": "Hari Baca",
        "TANGGAL_PEMBACAAN": "Tanggal",
        "JAM_PEMBACAAN": "Jam",
        "PEMKWH": "Pemakaian (kWh)"
    }),
    use_container_width=True,
    hide_index=True
)

# --- DEEP-DIVE KASUS (ANOMALI) ---
st.markdown("---")
st.subheader(f":material/troubleshoot: Rincian Kategori Kendala Lapangan")

df_anomali = df_officer_logs[~df_officer_logs["DLPD"].astype(str).str.upper().isin(["NORMAL", "Z - NORMAL", "Z"])]

if df_anomali.empty:
    st.success("Tidak ada kendala lapangan yang tercatat. Semua pembacaan normal.")
else:
    rekap_anomali = df_anomali["DLPD"].value_counts().reset_index()
    rekap_anomali.columns = ["Jenis Kendala (DLPD)", "Jumlah SR"]
    total_anomali = len(df_anomali)
    rekap_anomali["Proporsi dari Total Masalah"] = (rekap_anomali["Jumlah SR"] / total_anomali * 100).map("{:.2f}%".format)
    
    st.info(f"Ditemukan **{total_anomali} SR** dengan status tidak normal / kendala.")
    st.dataframe(rekap_anomali, use_container_width=True, hide_index=True)
