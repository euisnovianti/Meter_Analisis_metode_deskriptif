import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Template Styling Konsisten
CHART_FONT = dict(family="Inter, sans-serif", color="#191c1e")
COLOR_PALETTE = {
    "primary": "#00288e",
    "primary_container": "#1e40af",
    "tertiary": "#00563a",
    "warning": "#F59E0B",
    "danger": "#ba1a1a",
    "surface_variant": "#e0e3e5"
}

def plot_target_vs_realisasi_ulp(df: pd.DataFrame) -> go.Figure:
    """Diagram batang komparasi target vs realisasi per ULP."""
    df_plot = df.copy()
    df_plot["ULP"] = df_plot["ULP"].astype(str)
    
    summary = df_plot.groupby(["ULP", "DLPD"]).size().reset_index(name="Jumlah")
    
    fig = px.bar(
        summary,
        x="ULP",
        y="Jumlah",
        color="DLPD",
        barmode="group",
        color_discrete_map={
            "NORMAL": COLOR_PALETTE["primary_container"],
            "KWH Nol": COLOR_PALETTE["warning"],
            "Jam Nyala < 40 Jam Nyala": "#8b5cf6"
        }
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(type="category", showgrid=False, title="Unit Layanan Pelanggan (ULP)"),
        yaxis=dict(gridcolor="#e0e3e5", title="Jumlah Pelanggan")
    )
    return fig



def plot_hourly_distribution(df: pd.DataFrame) -> go.Figure:
    """Line chart tren jam pembacaan meter."""
    df_hours = df.dropna(subset=["JAM_ONLY"]).copy()

    hourly_counts = df_hours.groupby("JAM_ONLY").size().reset_index(name="Frekuensi")
    full_hours = pd.DataFrame({"JAM_ONLY": list(range(24))})
    hourly_counts = full_hours.merge(hourly_counts, on="JAM_ONLY", how="left").fillna(0)

    fig = px.line(
        hourly_counts,
        x="JAM_ONLY",
        y="Frekuensi",
        markers=True,
        color_discrete_sequence=[COLOR_PALETTE["primary_container"]]
    )
    fig.update_traces(
        line=dict(width=3),
        mode="lines+markers"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=1,
            title="Jam Pembacaan (WIB)"
        ),
        yaxis=dict(gridcolor="#e0e3e5", title="Frekuensi Bacaan")
    )
    return fig

def plot_reading_verification_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart status verifikasi bacaan."""
    status_counts = df["KODE_PESAN"].value_counts().reset_index()
    status_counts.columns = ["Status", "Jumlah"]
    
    fig = px.pie(
        status_counts,
        names="Status",
        values="Jumlah",
        hole=0.6,
        color_discrete_sequence=[
            COLOR_PALETTE["primary_container"],
            COLOR_PALETTE["warning"],
            COLOR_PALETTE["danger"],
            "#8b5cf6"
        ]
    )
    
    fig.update_traces(
        textinfo='percent',
        textposition='auto',
        insidetextorientation='radial',
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,} SR<br>Proporsi: %{percent}<extra></extra>"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True
    )
    return fig

def plot_spatial_map(df: pd.DataFrame) -> go.Figure:
    """Peta sebaran koordinat pembacaan meter pelanggan."""
    df_geo = df.dropna(subset=["KOORDINAT_X", "KOORDINAT_Y"]).copy()
    
    # Koordinat Garut / Jawa Barat sebagai default center jika data valid
    lat_center = df_geo["KOORDINAT_X"].mean() if not df_geo.empty else -7.2278
    lon_center = df_geo["KOORDINAT_Y"].mean() if not df_geo.empty else 107.9087
    
    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(
            df_geo,
            lat="KOORDINAT_X",
            lon="KOORDINAT_Y",
            color="DLPD",
            hover_name="IDPEL",
            hover_data={"NAMA": True, "KD_PETUGAS": True, "JAM_PEMBACAAN": True, "PEMKWH": True},
            zoom=11,
            center={"lat": lat_center, "lon": lon_center},
            map_style="carto-positron",
            color_discrete_map={
                "NORMAL": COLOR_PALETTE["tertiary"],
                "KWH Nol": COLOR_PALETTE["warning"],
                "Jam Nyala < 40 Jam Nyala": COLOR_PALETTE["danger"]
            }
        )
    else:
        fig = px.scatter_mapbox(
            df_geo,
            lat="KOORDINAT_X",
            lon="KOORDINAT_Y",
            color="DLPD",
            hover_name="IDPEL",
            hover_data={"NAMA": True, "KD_PETUGAS": True, "JAM_PEMBACAAN": True, "PEMKWH": True},
            zoom=11,
            center={"lat": lat_center, "lon": lon_center},
            mapbox_style="carto-positron",
            color_discrete_map={
                "NORMAL": COLOR_PALETTE["tertiary"],
                "KWH Nol": COLOR_PALETTE["warning"],
                "Jam Nyala < 40 Jam Nyala": COLOR_PALETTE["danger"]
            }
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT
    )
    return fig



def plot_daily_progression_bar(df_officer: pd.DataFrame) -> go.Figure:
    """Bar chart progres pembacaan harian per hari baca (A - E)."""
    prog = df_officer.groupby("HARI_BACA_LABEL").size().reset_index(name="Realisasi")
    
    fig = px.bar(
        prog,
        x="HARI_BACA_LABEL",
        y="Realisasi",
        color_discrete_sequence=[COLOR_PALETTE["primary_container"]]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="Hari Baca"),
        yaxis=dict(gridcolor="#e0e3e5", title="Jumlah Meter Terbaca")
    )
    return fig

def plot_leaderboard_horizontal(df_ranked, score_col="Total_Bacaan", name_col="KD_PETUGAS", top_n=20):
    """
    Menampilkan Bar Chart Horizontal untuk ranking petugas.
    Menampilkan Top N petugas terbaik secara terurut dari atas ke bawah.
    """
    # Ambil Top N data dan urutkan menaik agar di grafik batang tertinggi muncul paling atas
    df_plot = df_ranked.head(top_n).sort_values(by=score_col, ascending=True).copy()
    
    # Pastikan label kode/nama petugas berupa teks string
    df_plot[name_col] = df_plot[name_col].astype(str)
    
    fig = px.bar(
        df_plot,
        x=score_col,
        y=name_col,
        orientation='h',
        text=score_col,
        color=score_col,
        color_continuous_scale="Blues",
        labels={score_col: "Skor / Nilai Kinerja", name_col: "Petugas"},
        title=f"Top {min(top_n, len(df_plot))} Peringkat Petugas"
    )
    
    # Format teks pada batang bar dan tata letak
    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        cliponaxis=False
    )
    
    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(type='category'),
        height=max(400, len(df_plot) * 28), # Tinggi grafik otomatis adaptif dengan jumlah petugas
        margin=dict(l=20, r=40, t=40, b=20),
        coloraxis_showscale=False
    )
    
    return fig

def plot_anomali_breakdown(df):
    """
    Menampilkan visualisasi distribusi jenis kendala/anomali (Tidak Normal).
    """
    # Filter hanya data yang statusnya BUKAN 'NORMAL'
    df_anomali = df[df["DLPD"].astype(str).str.upper() != "NORMAL"].copy()
    
    if df_anomali.empty:
        return None
        
    # Hitung jumlah per kategori kendala
    agg_anomali = df_anomali.groupby("DLPD").size().reset_index(name="Jumlah Kasus")
    agg_anomali = agg_anomali.sort_values(by="Jumlah Kasus", ascending=True)
    
    fig = px.bar(
        agg_anomali,
        x="Jumlah Kasus",
        y="DLPD",
        orientation="h",
        text="Jumlah Kasus",
        color="Jumlah Kasus",
        color_continuous_scale="Reds",
        labels={"DLPD": "Jenis Kendala / Anomali", "Jumlah Kasus": "Total Temuan (SR)"},
        title="Distribusi Temuan Kendala / Bacaan Tidak Normal"
    )
    
    fig.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
        cliponaxis=False
    )
    
    fig.update_layout(
        yaxis=dict(type='category'),
        xaxis=dict(showgrid=True),
        height=max(350, len(agg_anomali) * 35),
        margin=dict(l=20, r=40, t=40, b=20),
        coloraxis_showscale=False
    )
    
    return fig