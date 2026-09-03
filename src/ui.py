import streamlit as st
from datetime import date
import pandas as pd


def render_material_symbols() -> None:
    """Load Material Symbols for custom HTML labels and cards."""
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1" rel="stylesheet">
        <style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            vertical-align: middle;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_global_filter_bar(df: pd.DataFrame) -> None:
    """Render shared global filters in the page content area."""
    st.markdown("### :material/filter_alt: Filter Data")
    filter_col_ulp, filter_col_hari, filter_col_date, filter_col_rbm = st.columns(
        [1.3, 1.3, 1.5, 1.3]
    )

    all_ulp = sorted(df["ULP"].dropna().unique().tolist())
    selected_ulp = st.session_state.get("global_selected_ulp", all_ulp)
    selected_ulp = [value for value in selected_ulp if value in all_ulp]
    st.session_state["global_selected_ulp"] = selected_ulp
    with filter_col_ulp:
        st.multiselect("Filter ULP", options=all_ulp, key="global_selected_ulp")

    all_hari = sorted(df["HARI_BACA_LABEL"].dropna().unique().tolist())
    selected_hari = st.session_state.get("global_selected_hari", all_hari)
    selected_hari = [value for value in selected_hari if value in all_hari]
    st.session_state["global_selected_hari"] = selected_hari
    with filter_col_hari:
        st.multiselect("Filter Hari Baca", options=all_hari, key="global_selected_hari")

    if "TANGGAL_PEMBACAAN" in df.columns:
        parsed_dates = pd.to_datetime(df["TANGGAL_PEMBACAAN"], errors="coerce").dt.date
        valid_dates = parsed_dates.dropna()
    else:
        valid_dates = pd.Series(dtype='object')
        
    with filter_col_date:
        if not valid_dates.empty:
            minimum_date = valid_dates.min()
            maximum_date = valid_dates.max()
            current_dates = st.session_state.get(
                "global_selected_dates", (minimum_date, maximum_date)
            )
            if not isinstance(current_dates, (tuple, list)) or not current_dates:
                current_dates = (minimum_date, maximum_date)
            current_dates = tuple(
                max(minimum_date, min(maximum_date, value))
                for value in current_dates
            )
            if len(current_dates) == 1:
                date_value = current_dates[0]
            else:
                date_value = (current_dates[0], current_dates[-1])
            st.session_state["global_selected_dates"] = date_value
            st.date_input(
                "Rentang Tanggal",
                min_value=minimum_date,
                max_value=maximum_date,
                key="global_selected_dates",
            )
        else:
            st.session_state["global_selected_dates"] = ()
            st.text_input("Rentang Tanggal", value="-", disabled=True)

    with filter_col_rbm:
        all_rbm = ["Semua"] + sorted(df["KODE_RBM"].dropna().astype(str).unique().tolist()) if "KODE_RBM" in df.columns else ["Semua"]

        if "global_selected_rbm" not in st.session_state:
            st.session_state["global_selected_rbm"] = "Semua"

        current_index = all_rbm.index(st.session_state["global_selected_rbm"]) if st.session_state["global_selected_rbm"] in all_rbm else 0

        selected_rbm = st.selectbox(
            "Pilih Kode RBM",
            options=all_rbm,
            index=current_index,
            key="select_global_rbm"
        )
        st.session_state["global_selected_rbm"] = selected_rbm


def apply_global_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply global filter values stored in Streamlit session state."""
    filtered = df.copy()

    selected_ulp = st.session_state.get("global_selected_ulp")
    if selected_ulp:
        filtered = filtered[filtered["ULP"].isin(selected_ulp)]

    selected_hari = st.session_state.get("global_selected_hari")
    if selected_hari:
        filtered = filtered[filtered["HARI_BACA_LABEL"].isin(selected_hari)]

    selected_dates = st.session_state.get("global_selected_dates")
    if selected_dates and "TANGGAL_PEMBACAAN" in filtered.columns:
        parsed_dates = pd.to_datetime(
            filtered["TANGGAL_PEMBACAAN"], errors="coerce"
        ).dt.date
        if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
            filtered = filtered[parsed_dates.between(*selected_dates)]
        elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
            filtered = filtered[parsed_dates == selected_dates[0]]
        elif isinstance(selected_dates, date):
            filtered = filtered[parsed_dates == selected_dates]

    rbm_query = str(st.session_state.get("global_selected_rbm", "Semua")).strip()
    if rbm_query != "Semua":
        if "KODE_RBM_CLEAN" in filtered.columns:
            filtered = filtered[filtered["KODE_RBM_CLEAN"].astype(str) == rbm_query]
        elif "KODE_RBM" in filtered.columns:
            filtered = filtered[filtered["KODE_RBM"].astype(str) == rbm_query]

    return filtered
