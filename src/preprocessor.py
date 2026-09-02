import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def clean_and_preprocess_data(df: pd.DataFrame, excluded_users: list) -> pd.DataFrame:
    """
    Membersihkan data log meter, memetakan hari baca, dan mengecualikan akun yang diinput manual.
    """
    df_clean = df.copy()

    # 1. Pengecualian akun berdasarkan input manual
    if excluded_users:
        # Menghapus spasi ekstra pada list input
        clean_excluded = [str(user).strip().lower() for user in excluded_users]
        df_clean = df_clean[~df_clean["KD_PETUGAS"].astype(str).str.strip().str.lower().isin(clean_excluded)]

    # 2. Pemetaan Hari Baca (A -> Hari 1, B -> Hari 2, dst.)
    hari_mapping = {
        "A": "Hari 1 (A)",
        "B": "Hari 2 (B)",
        "C": "Hari 3 (C)",
        "D": "Hari 4 (D)",
        "E": "Hari 5 (E)"
    }
    df_clean["HARI_BACA_CLEAN"] = df_clean["HARI_BACA"].astype(str).str.strip().str.upper()
    df_clean["HARI_BACA_LABEL"] = df_clean["HARI_BACA_CLEAN"].map(hari_mapping).fillna(df_clean["HARI_BACA_CLEAN"])

    # 3. Pembersihan Kode RBM (6 digit murni)
    df_clean["KODE_RBM_CLEAN"] = df_clean["KODE_RBM"].astype(str).str.strip().str.upper()

    # 4. Parsing Koordinat ke tipe Numerik
    df_clean["KOORDINAT_X"] = pd.to_numeric(df_clean["KOORDINAT_X"], errors="coerce")
    df_clean["KOORDINAT_Y"] = pd.to_numeric(df_clean["KOORDINAT_Y"], errors="coerce")

    # 5. Parsing Jam Pembacaan untuk analisis kecepatan
    df_clean["JAM_PEMBACAAN_STR"] = df_clean["JAM_PEMBACAAN"].astype(str).str.strip()
    df_clean["JAM_ONLY"] = pd.to_datetime(df_clean["JAM_PEMBACAAN_STR"], format="%H:%M", errors="coerce").dt.hour

    return df_clean