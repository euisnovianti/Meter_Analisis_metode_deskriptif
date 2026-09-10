import streamlit as st
from datetime import date
import pandas as pd


def render_material_symbols() -> None:
    """Load icons and the shared visual theme on every page (no data changes)."""
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    # CSS must bypass Markdown parsing so blank lines cannot expose it as text.
    st.html(
        """
        <style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            vertical-align: middle;
        }

        /* SIPERTI shared theme. Keep widgets, tables and page order intact. */
        .stApp {
            --siperti-blue: #005BAC;
            --siperti-navy: #003B73;
            --siperti-text: #152D45;
            --siperti-muted: #536B83;
            --siperti-line: #CFDEEC;
            --siperti-surface: #FFFFFF;
            background: #F3F7FB;
            color: var(--siperti-text);
        }
        [data-testid="stHeader"] {
            background: rgba(243, 247, 251, 0.97);
        }
        [data-testid="stMainBlockContainer"],
        section.main > .block-container {
            max-width: 1550px;
            padding-top: 5rem;
            padding-bottom: 3rem;
        }
        [data-testid="stMain"] p,
        [data-testid="stMain"] li {
            line-height: 1.65;
        }
        [data-testid="stCaptionContainer"] {
            color: var(--siperti-muted);
        }

        /* Existing page titles become blue banners without replacing text. */
        [data-testid="stMain"] h1,
        section.main h1 {
            color: #FFFFFF;
            background:
                radial-gradient(circle at 96% 4%, rgba(255,255,255,.08) 0 105px, transparent 106px),
                linear-gradient(112deg, #003B73 0%, #005BAC 65%, #00859C 100%);
            border: 1px solid #0875A0;
            border-radius: 16px;
            padding: 1.65rem 2rem;
            margin: .25rem 0 .65rem;
            font-size: clamp(1.65rem, 2.4vw, 2.2rem);
            font-weight: 750;
            line-height: 1.35;
            overflow-wrap: anywhere;
            box-shadow: 0 9px 24px rgba(0,59,115,.11);
            animation: siperti-enter .32s ease-out;
        }
        [data-testid="stMain"] h1 a,
        [data-testid="stMain"] h1 span {
            color: inherit;
        }
        [data-testid="stMain"] h2,
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4 {
            color: #123654;
            border-left: 4px solid #008CAA;
            padding-left: .8rem;
            margin-top: .5rem;
            line-height: 1.45;
            font-weight: 700;
        }
        [data-testid="stMain"] h2 { font-size: 1.45rem; }
        [data-testid="stMain"] h3 { font-size: 1.25rem; }
        [data-testid="stMain"] h4 { font-size: 1.1rem; }
        .stApp hr { border-color: var(--siperti-line); }

        /* Plain sidebar, unchanged logo and uploader placement. */
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E3EDF5;
        }
        [data-testid="stSidebarUserContent"] { padding-top: 2.25rem; }
        [data-testid="stSidebar"] h3 {
            color: var(--siperti-navy);
            font-size: 1.12rem;
            margin-top: .5rem;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            padding: .75rem .7rem;
            border-radius: 10px;
            min-height: 46px;
            transition: background-color .18s ease, box-shadow .18s ease;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background: #F0F6FC;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-selected="true"] {
            background: #EAF3FB;
            color: #003B73;
            box-shadow: inset 3px 0 #005BAC;
        }

        /* Metrics, charts and existing HTML cards share one surface style. */
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid var(--siperti-line);
            border-top: 3px solid var(--siperti-blue);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            box-shadow: 0 4px 14px rgba(0,59,115,.04);
            transition: box-shadow .18s ease, border-color .18s ease;
        }
        [data-testid="stMetric"]:hover {
            box-shadow: 0 7px 20px rgba(0,59,115,.09);
            border-color: #98BDDF;
        }
        [data-testid="stMetricValue"] {
            color: #003B73;
            font-size: clamp(1.65rem, 2vw, 2.1rem);
        }
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid var(--siperti-line);
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0,59,115,.035);
        }
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] > div[style*="background-color:white"] {
            border-top-color: #CFDEEC !important;
            border-right-color: #CFDEEC !important;
            border-bottom-color: #CFDEEC !important;
            box-shadow: 0 4px 14px rgba(0,59,115,.055) !important;
            transition: box-shadow .18s ease;
            overflow-wrap: anywhere;
        }
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] > div[style*="background-color:white"] div[style*="font-size:12px"],
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] > div[style*="background-color:white"] div[style*="font-size:11px"] {
            font-size: .875rem !important;
            line-height: 1.6;
        }
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] > div[style*="background-color:white"]:hover {
            box-shadow: 0 7px 20px rgba(0,59,115,.10) !important;
        }

        /* No table-cell overrides: sorting, scrolling and values stay native. */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid var(--siperti-line);
            border-radius: 10px;
        }
        [data-testid="stExpander"] {
            background: #FFFFFF;
            border-radius: 10px;
        }
        [data-testid="stExpander"] details {
            border-color: var(--siperti-line);
            border-radius: 10px;
        }
        [data-testid="stExpander"] summary {
            color: var(--siperti-navy);
            transition: background-color .18s ease;
        }
        [data-testid="stExpander"] summary:hover { background: #F0F6FC; }
        [data-testid="stAlert"] { border-radius: 10px; }
        [data-testid="stAlert"][data-baseweb="notification"] { line-height: 1.6; }

        /* Small, accessible interactions. No timers, JS or rerun loops. */
        [data-testid="stButton"] button,
        [data-testid="stDownloadButton"] button,
        [data-testid="stFileUploader"] button {
            min-height: 42px;
            border-radius: 9px;
            transition: background-color .18s ease, border-color .18s ease, box-shadow .18s ease;
        }
        [data-testid="stButton"] button:not(:disabled):hover,
        [data-testid="stDownloadButton"] button:not(:disabled):hover,
        [data-testid="stFileUploader"] button:not(:disabled):hover {
            border-color: #005BAC;
            box-shadow: 0 3px 10px rgba(0,91,172,.12);
        }
        .stApp button:focus-visible,
        .stApp a:focus-visible,
        .stApp summary:focus-visible {
            outline: 3px solid #00859C;
            outline-offset: 3px;
        }
        [data-testid="stFileUploaderDropzone"] {
            background: #F3F7FC;
            border: 1px dashed #ACC6DD;
            border-radius: 11px;
        }
        [data-baseweb="select"] > div,
        [data-baseweb="input"],
        [data-baseweb="textarea"] {
            border-radius: 8px;
        }
        [data-baseweb="tab-list"] { gap: .45rem; }
        [data-baseweb="tab"] {
            padding: .65rem 1rem;
            border-radius: 8px 8px 0 0;
            transition: background-color .18s ease;
        }
        [data-baseweb="tab"]:hover,
        [data-baseweb="tab"][aria-selected="true"] { background: #EAF3FB; }
        @keyframes siperti-enter {
            from { opacity: .65; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"],
            section.main > .block-container {
                padding-top: 4.5rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            [data-testid="stMain"] h1,
            section.main h1 { padding: 1.25rem; }
            [data-testid="stMain"] [data-testid="stMarkdownContainer"] > div[style*="background-color:white"][style*="display:flex"] {
                flex-wrap: wrap;
                gap: 1rem;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            .stApp *, .stApp *::before, .stApp *::after {
                animation: none !important;
                transition: none !important;
                scroll-behavior: auto !important;
            }
        }
        </style>
        """,
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
