import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import render_sidebar_uploader
from src.ui import render_material_symbols, apply_global_filters, render_global_filter_bar

st.set_page_config(
    page_title="Workforce & Spatial - SIPERTI",
    page_icon=":material/map:",
    layout="wide"
)

render_material_symbols()
render_sidebar_uploader()

if not st.session_state.get("data_ready", False) or st.session_state.get("raw_data") is None:
    st.info("Silakan unggah file Excel melalui menu di sidebar sebelah kiri.")
    st.stop()

df = st.session_state["raw_data"]

st.title(":material/map: Workforce & Spatial Anomaly Analysis")
st.markdown("Pemetaan koordinat geografis pembacaan meter dan isolasi sebaran kendala anomali lapangan.")

render_global_filter_bar(df)
df_filtered = apply_global_filters(df)

# --- 2. FILTER LOKAL: KODE KENDALA DLPD ---
st.markdown("### :material/tune: Filter Status Kendala Lapangan")
all_dlpd = sorted(df_filtered["DLPD"].dropna().unique().tolist())
default_dlpd = [d for d in all_dlpd if "NORMAL" in str(d).upper()] or all_dlpd[:2]

selected_dlpd = st.multiselect(
    "Pilih Status DLPD / Kategori Kendala", 
    options=all_dlpd, 
    default=default_dlpd,
    placeholder="Pilih status..."
)

if selected_dlpd:
    df_filtered_map = df_filtered[df_filtered["DLPD"].isin(selected_dlpd)].copy()
else:
    st.warning("Silakan pilih minimal satu status DLPD pada filter di atas.")
    st.stop()

st.markdown("---")

# --- 3. LAYOUT SPASIAL: STATISTIK MINI DI KIRI, PETA BESAR DI KANAN ---
col_stats, col_map = st.columns([1, 3])

total_titik_terpilih = len(df_filtered_map)
total_anomali_terpilih = len(df_filtered_map[~df_filtered_map["DLPD"].str.contains("NORMAL", case=False, na=False)])
pct_anomali = (total_anomali_terpilih / total_titik_terpilih * 100) if total_titik_terpilih > 0 else 0

with col_stats:
    st.markdown("#### :material/analytics: Ringkasan Klaster")
    st.markdown(f"""
        <div style="background-color:white; border:1px solid #c4c5d5; border-radius:10px; padding:16px; margin-bottom:12px;">
            <div style="font-size:12px; color:#444653; font-weight:600;">TITIK TERPETAKAN</div>
            <div style="font-size:24px; color:#191c1e; font-weight:700;">{total_titik_terpilih:,}</div>
        </div>
        <div style="background-color:white; border:1px solid #c4c5d5; border-radius:10px; padding:16px; margin-bottom:12px;">
            <div style="font-size:12px; color:#ba1a1a; font-weight:600;">TEMUAN KENDALA / ANOMALI</div>
            <div style="font-size:24px; color:#ba1a1a; font-weight:700;">{total_anomali_terpilih:,}</div>
            <div style="font-size:11px; color:#444653;">({pct_anomali:.1f}% dari total titik aktif)</div>
        </div>
    """, unsafe_allow_html=True)

with col_map:
    st.markdown("#### :material/location_on: Sebaran Titik Lapangan (Geospatial Map)")
    
    df_filtered_map["KOORDINAT_X"] = df_filtered_map["KOORDINAT_X"].astype(str).str.replace(",", ".").str.strip()
    df_filtered_map["KOORDINAT_Y"] = df_filtered_map["KOORDINAT_Y"].astype(str).str.replace(",", ".").str.strip()
    
    df_filtered_map["_LAT"] = pd.to_numeric(df_filtered_map["KOORDINAT_Y"], errors="coerce")
    df_filtered_map["_LON"] = pd.to_numeric(df_filtered_map["KOORDINAT_X"], errors="coerce")
    
    if (df_filtered_map["_LAT"] > 20).any() and (df_filtered_map["_LON"] < 0).any():
        df_filtered_map["_LAT"], df_filtered_map["_LON"] = df_filtered_map["_LON"], df_filtered_map["_LAT"]
    
    df_valid_map = df_filtered_map.dropna(subset=["_LAT", "_LON"]).head(5000)

    if not df_valid_map.empty:
        lat_center = df_valid_map["_LAT"].mean()
        lon_center = df_valid_map["_LON"].mean()
        
        if hasattr(px, "scatter_map"):
            fig_map = px.scatter_map(
                df_valid_map,
                lat="_LAT",
                lon="_LON",
                color="DLPD",
                hover_name="IDPEL",
                hover_data=["NAMA", "KD_PETUGAS", "JAM_PEMBACAAN", "PEMKWH"],
                zoom=11,
                center={"lat": lat_center, "lon": lon_center},
                height=480
            )
            fig_map.update_layout(
                map_style="carto-positron",
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )
        else:
            fig_map = px.scatter_mapbox(
                df_valid_map,
                lat="_LAT",
                lon="_LON",
                color="DLPD",
                hover_name="IDPEL",
                hover_data=["NAMA", "KD_PETUGAS", "JAM_PEMBACAAN", "PEMKWH"],
                zoom=11,
                center={"lat": lat_center, "lon": lon_center},
                height=480
            )
            fig_map.update_layout(
                mapbox_style="carto-positron",
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )
        fig_map.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Data koordinat kosong atau format angka koordinat tidak valid.")

st.markdown("---")

# --- 4. TABEL INSPEKSI & DRILL-DOWN ANOMALI ---
st.subheader(":material/warning: Detail Temuan Kendala Lapangan")
df_anomaly = df_filtered_map[~df_filtered_map["DLPD"].str.contains("NORMAL", case=False, na=False)]

st.dataframe(
    df_anomaly[[
        "IDPEL", "NAMA", "ULP", "KD_PETUGAS", 
        "TANGGAL_PEMBACAAN", "JAM_PEMBACAAN", "DLPD", "PEMKWH"
    ]].rename(columns={
        "KD_PETUGAS": "Petugas", "TANGGAL_PEMBACAAN": "Tanggal",
        "JAM_PEMBACAAN": "Jam", "PEMKWH": "Pemakaian (kWh)"
    }),
    use_container_width=True, hide_index=True
)