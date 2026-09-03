import pandas as pd
import streamlit as st
from typing import Tuple, Optional
from src.preprocessor import clean_and_preprocess_data

# Kolom-kolom utama yang dibutuhkan
REQUIRED_COLUMNS = [
    "UP3", "ULP", "NAMA", "IDPEL", "TARIF", "DAYA", "BLTH",
    "KD_PETUGAS", "KODE_RBM", "TANGGAL_PEMBACAAN", "JAM_PEMBACAAN",
    "KODE_PESAN", "KOORDINAT_X", "KOORDINAT_Y", "DLPD", "PEMKWH"
]

@st.cache_data(show_spinner="Memuat dataset operasional...", max_entries=2)
def load_and_validate_excel(file_buffer) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    """
    Membaca file buffer Excel/CSV dan melakukan validasi struktur kolom.
    """
    try:
        if file_buffer.name.endswith('.csv'):
            df = pd.read_csv(file_buffer)
        else:
            try:
                df = pd.read_excel(file_buffer, engine="calamine")
            except Exception:
                df = pd.read_excel(file_buffer, engine="openpyxl")
            
        # Normalisasi nama kolom penanda hari jika bernama 'Column1'
        if "Column1" in df.columns:
            df.rename(columns={"Column1": "HARI_BACA"}, inplace=True)
            
        # Cek kolom wajib
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            return False, f"Format tidak sesuai. Kolom hilang: {', '.join(missing_cols)}", None
            
        # Pastikan kolom HARI_BACA tersedia
        if "HARI_BACA" not in df.columns:
            return False, "Kolom penanda hari (Column1 / HARI_BACA) tidak ditemukan dalam data.", None

        str_cols = ["IDPEL", "ULP", "KD_PETUGAS", "KODE_RBM", "DLPD"]
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return True, f"Data berhasil dimuat! Ditemukan {len(df):,} baris data.", df

    except Exception as e:
        return False, f"Terjadi kesalahan saat membaca file: {str(e)}", None

def render_sidebar_uploader():
    """Sidebar kustom bersih ala Stitch tanpa duplikasi menu."""
    
    #   logo dari assets/Logo_PLN.png)
    import base64
    import os

    try:
        with open("assets/Logo_PLN.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 40px; height: 40px; border-radius: 8px; object-fit: contain; background-color: white; padding: 2px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
    except Exception:
        # Fallback ke icon default jika gagal load gambar
        logo_html = '<div style="background-color: #00288e; color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><span class="material-symbols-outlined" style="font-size: 24px;">analytics</span></div>'

    st.sidebar.markdown(f"""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1" rel="stylesheet">
        <style>
        .material-symbols-outlined {{ font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; vertical-align: middle; }}
        </style>
        <div style="display: flex; align-items: center; gap: 12px; padding: 5px 0 15px 0;">
            {logo_html} <!-- DISINI LOGO KITA DISISIPKAN -->
            <div>
                <div style="font-weight: 700; font-size: 16px; color: #191c1e; line-height: 1.2;">SIPERTI</div>
                <div style="font-size: 11px; color: #444653;">Enterprise Analytics</div>
            </div>
        </div>
        <hr style="margin: 0 0 15px 0; border-color: #c4c5d5;">
    """, unsafe_allow_html=True)

    
    # 2. Menu Navigasi Kustom (Hanya muncul di sini)
    st.sidebar.markdown("### Navigasi Menu")
    st.sidebar.page_link("app.py", label="Information", icon=":material/info:")
    st.sidebar.page_link("pages/2_Executive_Overview.py", label="Dashboard Overview", icon=":material/dashboard:")
    st.sidebar.page_link("pages/3_Leaderboard.py", label="Leaderboard", icon=":material/leaderboard:")
    st.sidebar.page_link("pages/4_Analisis_Spasial.py", label="Workforce & Spatial", icon=":material/map:")
    st.sidebar.page_link("pages/5_Rapor_Petugas.py", label="Officer Tracking", icon=":material/badge:")
    st.sidebar.page_link("pages/6_Laporan_Ekspor.py", label="Data Management", icon=":material/cloud_download:")

    
    st.sidebar.markdown("<hr style='margin: 15px 0; border-color: #c4c5d5;'>", unsafe_allow_html=True)
    
    # 3. Manajemen File / Uploader di Bagian Bawah
    st.sidebar.markdown("### Manajemen File")
    is_ready = st.session_state.get("data_ready", False)
    
    if not is_ready:
        uploaded_file = st.sidebar.file_uploader(
            "Upload file Excel / CSV", 
            type=["xlsx", "csv"],
            key="global_file_uploader",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            with st.spinner("Memproses file..."):
                success, msg, df_raw = load_and_validate_excel(uploaded_file)
                if success:
                    excluded_users = st.session_state.get("excluded_users", [])
                    df_cleaned = clean_and_preprocess_data(df_raw, excluded_users)
                    
                    st.session_state["raw_data"] = df_cleaned
                    st.session_state["data_ready"] = True
                    st.session_state["loaded_file_name"] = uploaded_file.name
                    st.sidebar.success(f"Berhasil: {uploaded_file.name}")
                    st.rerun()
                else:
                    st.sidebar.error(msg)
    else:
        file_name = st.session_state.get('loaded_file_name', 'File Aktif')
        st.sidebar.info(f"📂 **Aktif:** {file_name}")
        
        if st.sidebar.button("🔄 Ganti / Reset File", use_container_width=True):
            st.session_state["data_ready"] = False
            st.session_state["raw_data"] = None
            if "loaded_file_name" in st.session_state:
                del st.session_state["loaded_file_name"]
            st.rerun()
            st.rerun()