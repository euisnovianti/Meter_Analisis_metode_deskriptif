import pandas as pd

def calculate_performance_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menghitung metrik performa deskriptif untuk tiap RBM.
    """
    if df.empty:
        return pd.DataFrame()
        
    # Agregasi data per RBM
    df_summary = df.groupby("KODE_RBM").agg(
        ULP=("ULP", "first"),
        Petugas_Bertugas=("KD_PETUGAS", "first"),
        Total_Target=("IDPEL", "count"),
        Sukses_Normal=("DLPD", lambda x: (x.astype(str).str.upper() == "NORMAL").sum())
    ).reset_index()
    
    # Hitung metrik C1, C2, C3, C4
    df_summary["Ketercapaian"] = (df_summary["Sukses_Normal"] / df_summary["Total_Target"]) * 100
    df_summary["Volume"] = df_summary["Total_Target"] # Menggunakan total target sebagai volume
    df_summary["Waktu"] = 100.0 # Metrik waktu disederhanakan
    df_summary["Anomali"] = 100.0 - df_summary["Ketercapaian"]
    
    return df_summary
