import streamlit as st
from src.data_loader import render_sidebar_uploader
from src.ui import render_material_symbols

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="SIPERTI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State Global
if "raw_data" not in st.session_state:
    st.session_state["raw_data"] = None

if "raw_data_source" not in st.session_state:
    st.session_state["raw_data_source"] = None

if "data_ready" not in st.session_state:
    st.session_state["data_ready"] = False

if "excluded_users" not in st.session_state:
    # Daftar ini dikelola manual melalui halaman Pengaturan Model.
    st.session_state["excluded_users"] = []

render_material_symbols()
render_sidebar_uploader()

# Tampilan Landing Page
st.title(":material/electric_bolt: SIPERTI")
st.markdown("### Sistem Pendukung Keputusan Kinerja Petugas Baca Meter")

st.info("👋 Selamat datang di **SIPERTI**! Sistem otomatisasi visualisasi dan evaluasi kinerja petugas baca meter menggunakan metode **statistik deskriptif**.")

st.markdown("""
---
Format data yang diterima: **Excel (.xlsx)** dengan kolom wajib:
UP3, ULP, NAMA, TARIF, DAYA, KD_PETUGAS, KODE_RBM, TANGGAL_PEMBACAAN, JAM_PEMBACAAN, KODE_PESAN, KOORDINAT_X, KOORDINAT_Y, DLPD, PEMKWH

#### **Panduan Alur Penggunaan Dashboard:**
1. **:material/upload_file: Upload Data:** Unggah file Excel log baca meter (.xlsx). Sistem akan otomatis membersihkan data.
2. **:material/bar_chart: Dashboard Overview:** Pantau ringkasan metrik KPI, perbandingan target vs realisasi, dan status harian.
3. **:material/emoji_events: Leaderboard:** Lihat pemeringkatan kinerja petugas secara fleksibel.
4. **:material/map: Workforce & Spatial:** Periksa sebaran geografis koordinat pelanggan dan pemetaan wilayah kendala (anomali).
5. **:material/person: Officer Tracking (Rapor):** Analisis mendalam performa perorangan via Radar Chart dan log kendala.
6. **:material/description: Data Management (Ekspor):** Unduh hasil akhir penilaian ke format Excel/PDF untuk pencairan bonus/evaluasi.
---
""")

# Cek status data
if st.session_state.get("raw_data") is None:
    st.session_state["data_ready"] = False
    st.warning(":material/warning: **Status Data:** Belum ada data aktif. Silakan unggah file melalui uploader di sidebar kiri untuk memulai.")
else:
    st.session_state["data_ready"] = True
    st.success(":material/check_circle: **Status Data:** Data siap dianalisis. Silakan pilih menu analisis di sidebar.")