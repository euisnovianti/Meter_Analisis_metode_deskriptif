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
        Petugas_Bertugas=("KD_PETUGAS", lambda x: ", ".join(sorted(x.dropna().astype(str).unique()))),
        Total_Target=("IDPEL", "count"),
        Sukses_Normal=("DLPD", lambda x: (x.astype(str).str.upper() == "NORMAL").sum()),
        Kendala_Anomali=("DLPD", lambda x: (x.astype(str).str.upper() != "NORMAL").sum()),
        Bacaan_Tepat_Waktu=("JAM_PEMBACAAN", lambda x: pd.to_datetime(x, format="%H:%M", errors="coerce").dt.hour.between(6, 17, inclusive="both").sum()),
        Jam_Awal=("JAM_PEMBACAAN", lambda x: pd.to_datetime(x, format="%H:%M", errors="coerce").min()),
        Jam_Akhir=("JAM_PEMBACAAN", lambda x: pd.to_datetime(x, format="%H:%M", errors="coerce").max())
    ).reset_index()
    
    durasi_detik = (df_summary["Jam_Akhir"] - df_summary["Jam_Awal"]).dt.total_seconds().fillna(0)
    durasi_menit = (durasi_detik // 60).astype(int).clip(lower=0)
    df_summary["Durasi_Display"] = (durasi_menit // 60).astype(str) + "j " + (durasi_menit % 60).astype(str) + "m"
    
    # Hitung metrik C1, C2, C3, C4
    df_summary["Ketercapaian"] = (df_summary["Sukses_Normal"] / df_summary["Total_Target"]) * 100
    df_summary["Volume"] = df_summary["Total_Target"] # Menggunakan total target sebagai volume
    df_summary["Waktu_Kepatuhan"] = (df_summary["Bacaan_Tepat_Waktu"] / df_summary["Total_Target"]) * 100 # Skor kepatuhan jam 06.00-17.00
    df_summary["Waktu"] = (durasi_menit / 60.0).round(2) # Durasi desimal untuk perhitungan
    df_summary["Anomali"] = 100.0 - df_summary["Ketercapaian"]
    
    return df_summary
