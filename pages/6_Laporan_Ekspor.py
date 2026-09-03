import streamlit as st
import pandas as pd
from src.data_loader import render_sidebar_uploader
from src.ui import apply_global_filters, render_global_filter_bar
from src.ui import render_material_symbols
from src.metrics_engine import calculate_performance_metrics
from src.export_report import generate_excel_report

st.set_page_config(
    page_title="Laporan & Ekspor - SIPERTI",
    page_icon=":material/description:",
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
# Hitung evaluasi
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

st.title(":material/description: Laporan Resmi & Ekspor Hasil Perangkingan")
st.markdown("Unduh rekapitulasi evaluasi kinerja petugas baca meter untuk dokumen pelaporan ULP/UP3.")

if df_eval.empty:
    st.error("Data tidak mencukupi untuk membuat laporan.")
    st.stop()

# --- PREVIEW LAPORAN ---
st.subheader(":material/preview: Preview Laporan Rekapitulasi")
st.info(f"Data yang ditampilkan dan diekspor menggunakan urutan **Statistik Deskriptif ({st.session_state.get('desc_sort_by', 'Volume Pembacaan Terbanyak')})**.")

# Format kolom Jam_Awal dan Jam_Akhir menjadi format HH:MM
for col in ["Jam_Awal", "Jam_Akhir"]:
    if col in df_eval.columns:
        df_eval[col] = pd.to_datetime(df_eval[col], errors="coerce").dt.strftime("%H:%M").fillna("-")

st.dataframe(df_eval, use_container_width=True, hide_index=True)

st.markdown("---")

# --- TOMBOL DOWNLOAD EXCEL ---
st.subheader(":material/download: Unduh Berkas Laporan")
st.markdown("Klik tombol di bawah untuk mengunduh laporan lengkap dalam format Excel (.xlsx) yang siap dilampirkan dalam dokumen sidang KP atau laporan operasional PLN.")

excel_data = generate_excel_report(df_eval)
file_suffix = "Deskriptif"

st.download_button(
    label=f":material/download: Unduh Laporan Rekapitulasi {file_suffix} (Excel)",
    data=excel_data,
    file_name=f"Laporan_Kinerja_Petugas_{file_suffix}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)
