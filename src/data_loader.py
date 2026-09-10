import pandas as pd
import streamlit as st
from base64 import b64encode
from pathlib import Path
from typing import Tuple, Optional
from src.preprocessor import clean_and_preprocess_data

# Kolom-kolom utama yang dibutuhkan
REQUIRED_COLUMNS = [
    "UP3", "ULP", "NAMA", "IDPEL", "TARIF", "DAYA", "BLTH",
    "KD_PETUGAS", "KODE_RBM", "TANGGAL_PEMBACAAN", "JAM_PEMBACAAN",
    "KODE_PESAN", "KOORDINAT_X", "KOORDINAT_Y", "DLPD", "PEMKWH"
]

# Matikan show_spinner di cache agar tidak dobel dengan spinner pemanggil
@st.cache_data(show_spinner=False, max_entries=2)
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
    
    # Logo lokal tetap ditemukan dari direktori mana pun Streamlit dijalankan.
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "Logo_PLN.png"
    try:
        logo_base64 = b64encode(logo_path.read_bytes()).decode("ascii")
        logo_html = (
            f'<img src="data:image/png;base64,{logo_base64}" '
            'class="siperti-sidebar-logo" alt="Logo PLN">'
        )
    except OSError:
        logo_html = '<span class="siperti-sidebar-logo-fallback">PLN</span>'

    st.sidebar.html("""
        <style>
        .siperti-sidebar-brand {
            display: flex; align-items: center; gap: 20px;
            padding: 12px 0 24px; margin-bottom: 10px;
            background: transparent; border: 0; border-bottom: 1px solid #CFDEEC;
            border-radius: 0; box-shadow: none;
        }
        .siperti-sidebar-logo {
            display: block; width: 34px; height: auto; flex: 0 0 34px;
            object-fit: contain; border: 0; border-radius: 0;
            background: transparent; padding: 0; box-shadow: none;
        }
        .siperti-sidebar-logo-fallback { color: #008FB6; font-size: 14px; font-weight: 800; }
        .siperti-sidebar-copy { min-width: 0; }
        .siperti-sidebar-name {
            color: #003B73; font-size: 20px; font-weight: 800;
            line-height: 1.3; letter-spacing: .025em;
        }
        .siperti-sidebar-subtitle {
            color: #244B70; font-size: 12.5px; line-height: 1.55;
            margin-top: 5px; overflow-wrap: anywhere;
        }
        .siperti-sidebar-unit {
            color: #005BAC; font-size: 12px; font-weight: 750;
            line-height: 1.5; margin-top: 7px; background: transparent;
        }
        </style>
    """)
    st.sidebar.html(
        '<div class="siperti-sidebar-brand">'
        f'{logo_html}'
        '<div class="siperti-sidebar-copy">'
        '<div class="siperti-sidebar-name">SIPERTI</div>'
        '<div class="siperti-sidebar-subtitle">Dashboard Analitik Operasional</div>'
        '<div class="siperti-sidebar-unit">PLN UP3 Garut</div>'
        '</div></div>'
    )

    
    # 2. Manajemen File / Uploader tepat di bawah logo
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
            # Menggunakan satu spinner tunggal
            with st.spinner("Memproses dataset operasional..."):
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
        st.sidebar.info(f"**File Aktif:** {file_name}")
        
        if st.sidebar.button("Reset File", use_container_width=True):
            st.session_state["data_ready"] = False
            st.session_state["raw_data"] = None
            if "loaded_file_name" in st.session_state:
                del st.session_state["loaded_file_name"]
            st.rerun()

    st.sidebar.markdown("<hr style='margin: 15px 0; border-color: #c4c5d5;'>", unsafe_allow_html=True)

    # 3. Menu Navigasi Kustom (Hanya muncul di sini)
    st.sidebar.markdown("### Navigasi Menu")
    st.sidebar.page_link("app.py", label="Information", icon=":material/info:")
    st.sidebar.page_link("pages/2_Executive_Overview.py", label="Dashboard Overview", icon=":material/dashboard:")
    st.sidebar.page_link("pages/3_Leaderboard.py", label="Leaderboard", icon=":material/leaderboard:")
    st.sidebar.page_link("pages/4_Analisis_Spasial.py", label="Workforce & Spatial", icon=":material/map:")
    st.sidebar.page_link("pages/5_Rapor_Petugas.py", label="Officer Tracking", icon=":material/badge:")
    st.sidebar.page_link("pages/6_Laporan_Ekspor.py", label="Data Management", icon=":material/cloud_download:")
