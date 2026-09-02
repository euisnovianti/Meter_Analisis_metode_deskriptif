import streamlit as st
import pandas as pd
from src.data_loader import render_sidebar_uploader
from src.ui import apply_global_filters, render_global_filter_bar
from src.ui import render_material_symbols
from src.metrics_engine import calculate_performance_metrics
from src.visualizer import plot_leaderboard_horizontal

st.set_page_config(
    page_title="Leaderboard - SIPERTI",
    page_icon=":material/emoji_events:",
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

st.title(":material/leaderboard: Leaderboard Kinerja Petugas")

# Kontrol Fleksibel Metode Evaluasi
with st.expander(":material/tune: Konfigurasi Metode Penilaian Kinerja", expanded=False):
    st.caption("Kriteria Pengurutan Langsung")
    default_sort = st.session_state.get("desc_sort_by", "Volume Pembacaan Terbanyak")
    sort_metric = st.selectbox(
        "Urutkan Berdasarkan:",
        ["Volume Pembacaan Terbanyak", "Ketercapaian Target Tertinggi", "Kendala Lapangan Terendah"],
        index=["Volume Pembacaan Terbanyak", "Ketercapaian Target Tertinggi", "Kendala Lapangan Terendah"].index(default_sort)
    )
    st.session_state["desc_sort_by"] = sort_metric

# Calculate data
df_eval = calculate_performance_metrics(df)

if not df_eval.empty:
    sort_col_map = {
        "Volume Pembacaan Terbanyak": ("Volume", False),
        "Ketercapaian Target Tertinggi": ("Ketercapaian", False),
        "Kendala Lapangan Terendah": ("Anomali", True)
    }
    sort_col, ascending = sort_col_map[st.session_state.get("desc_sort_by", "Volume Pembacaan Terbanyak")]
    
    df_eval.sort_values(by=[sort_col, "Volume"], ascending=[ascending, False], inplace=True)
    df_eval["Rank"] = range(1, len(df_eval) + 1)
    df_eval["Status"] = "N/A"

if df_eval.empty:
    st.error("Data tidak mencukupi untuk melakukan evaluasi.")
    st.stop()


# --- PODIUM TOP 3 (Bento Card Style) ---
st.markdown("### :material/looks_one: Top 3 RBM Terbaik")
top_3 = df_eval.head(3).reset_index(drop=True)
podium_colors = ["#F59E0B", "#94A3B8", "#B45309"]

cols = st.columns(3)
for idx, row in top_3.iterrows():
    with cols[idx]:
        score_display = "🏆"
        st.markdown(f"""
            <div style="background-color:white; border:1px solid #c4c5d5; border-radius:12px; padding:20px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1); border-left: 6px solid {podium_colors[idx]};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:24px; font-weight:bold; color:{podium_colors[idx]};">Rank #{int(row['Rank'])}</div>
                    <div style="font-size:20px; font-weight:bold; color:#00288e;">{score_display}</div>
                </div>
                <div style="font-size:18px; font-weight:bold; color:#191c1e; margin-top:10px;">{row['KODE_RBM']}</div>
                <div style="font-size:12px; color:#444653; margin-top:4px;">ULP: {row['ULP']} | Petugas: {row['Petugas_Bertugas']} | Target: {row['Total_Target']} Titik</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- VISUALIZATION / SCATTER PLOT ---
st.info(f"Metrik Historis: Ditampilkan berdasarkan **{st.session_state.get('desc_sort_by', 'Volume Pembacaan Terbanyak')}**. Total RBM Dievaluasi: **{len(df_eval)} rute**")
# --- HORIZONTAL BAR CHART ---
st.markdown("---")
st.subheader(":material/bar_chart: Visualisasi Distribusi Kinerja Petugas")

sort_desc = st.session_state.get("desc_sort_by", "Volume Pembacaan Terbanyak")
if "Volume" in sort_desc:
    val_col = "Volume"
elif "Ketercapaian" in sort_desc:
    val_col = "Ketercapaian"
else:
    val_col = "Anomali"
top_limit = st.slider("Tampilkan Jumlah Petugas:", min_value=5, max_value=50, value=20, step=5)

fig_hbar = plot_leaderboard_horizontal(
    df_ranked=df_eval,
    score_col=val_col,
    name_col="KODE_RBM",
    top_n=top_limit
)
st.plotly_chart(fig_hbar, use_container_width=True)

# --- TABEL PERANGKINGAN LENGKAP ---
st.markdown("---")
st.subheader(":material/table_chart: Detailed Performance Ranking Table")

search_query = st.text_input("Cari Kode RBM / Petugas / ULP", placeholder="Ketik untuk mencari...")
df_display = df_eval.copy()

if search_query:
    df_display = df_display[
        df_display["KODE_RBM"].str.contains(search_query, case=False, na=False) |
        df_display["Petugas_Bertugas"].str.contains(search_query, case=False, na=False) |
        df_display["ULP"].str.contains(search_query, case=False, na=False)
    ]

cols_to_show = [
    "Rank", "KODE_RBM", "Petugas_Bertugas", "ULP", "Total_Target", 
    "Sukses_Normal", "Ketercapaian", "Volume", "Waktu", "Anomali"
]

rename_dict = {
    "KODE_RBM": "Kode RBM",
    "Petugas_Bertugas": "Petugas Bertugas",
    "Total_Target": "Total Target",
    "Sukses_Normal": "Sukses Normal",
    "Ketercapaian": "Ketercapaian (%)",
    "Volume": "Volume Baca",
    "Waktu": "Skor Waktu",
    "Anomali": "Anomali (%)"
}



df_summary = df_display[cols_to_show].rename(columns=rename_dict)

# Format tampilan kolom: "Jumlah SR (Persentase%)"
df_summary["Normal / Berhasil"] = df_summary.apply(
    lambda r: f"{int(r['Sukses Normal'])} ({r['Ketercapaian (%)']:.2f}%)", axis=1
)

df_summary["Kendala / Anomali"] = df_summary.apply(
    lambda r: f"{int(r['Total Target'] - r['Sukses Normal'])} ({r['Anomali (%)']:.2f}%)", axis=1
)

# Pilih dan susun urutan kolom yang ingin ditampilkan ke tabel
display_cols = [
    "Rank",
    "Kode RBM",
    "Petugas Bertugas",
    "ULP",
    "Total Target",
    "Normal / Berhasil",
    "Kendala / Anomali",
    "Volume Baca",
    "Skor Waktu"
]


st.dataframe(
    df_summary[display_cols],
    use_container_width=True,
    hide_index=True
)


