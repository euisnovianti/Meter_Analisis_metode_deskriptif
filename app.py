from html import escape

import streamlit as st

from src.data_loader import render_sidebar_uploader
from src.ui import render_material_symbols


st.set_page_config(
    page_title="SIPERTI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inisialisasi data tetap sama dengan aplikasi sebelumnya.
if "raw_data" not in st.session_state:
    st.session_state["raw_data"] = None
if "raw_data_source" not in st.session_state:
    st.session_state["raw_data_source"] = None
if "data_ready" not in st.session_state:
    st.session_state["data_ready"] = False
if "excluded_users" not in st.session_state:
    st.session_state["excluded_users"] = []

render_material_symbols()
render_sidebar_uploader()

# CSS khusus halaman Informasi dipisahkan dari Markdown.
st.html("""
<style>
    #siperti-info-hero {
        position: relative; isolation: isolate; overflow: hidden;
        padding: 28px 32px 30px; margin: 0 0 8px;
        border-radius: 16px; border: 1px solid #0875A0;
        background: linear-gradient(112deg, #003B73 0%, #005BAC 65%, #00859C 100%);
        box-shadow: 0 9px 24px rgba(0,59,115,.12); color: #FFFFFF;
        animation: siperti-info-enter .32s ease-out;
    }
    #siperti-info-hero::after {
        content: ""; position: absolute; z-index: -1;
        width: 260px; height: 260px; border-radius: 50%;
        background: rgba(255,255,255,.075);
        top: -110px; right: -60px; pointer-events: none;
    }
    #siperti-info-hero .siperti-info-eyebrow {
        font-size: 12px; line-height: 1.6; font-weight: 750;
        letter-spacing: .1em; color: #E4F5FF;
    }
    #siperti-info-hero h1 {
        padding: 0; margin: 10px 0 5px; background: none;
        border: 0; border-radius: 0; box-shadow: none; color: #FFFFFF;
        font-size: clamp(30px,3vw,38px); line-height: 1.25;
        font-weight: 800; animation: none;
    }
    #siperti-info-hero p {
        max-width: 1080px; margin: 0; color: #F6FAFF;
        font-size: 17px; line-height: 1.75;
    }
    .siperti-info-intro {
        display: flex; align-items: center; gap: 22px;
        padding: 20px; margin-bottom: 16px;
        background: #EAF4FC; border: 1px solid #C4DFF3; border-radius: 12px;
    }
    .siperti-info-monogram {
        display: grid; place-items: center; flex: 0 0 46px; height: 46px;
        border-radius: 50%; background: #FFFFFF; border: 1px solid #B5D7EF;
        color: #003B73; font-weight: 800;
    }
    .siperti-info-intro strong {
        display: block; margin-bottom: 5px; color: #003B73; font-size: 16px;
    }
    .siperti-info-intro p, .siperti-info-section p, .siperti-info-step p,
    .siperti-info-scope p, .siperti-info-data-group p, .siperti-info-status p {
        margin: 0; color: #536B83; font-size: 15px; line-height: 1.75;
    }
    .siperti-info-section { margin: 16px 0 18px; }
    .siperti-info-section h2 {
        margin: 0 0 6px !important; padding: 0 0 0 12px !important;
        border-left: 4px solid #008CAA !important; color: #123654;
        font-size: 22px !important; line-height: 1.4 !important;
    }
    .siperti-info-section p { padding-left: 16px; }
    .siperti-info-steps {
        display: grid; grid-template-columns: repeat(3,minmax(0,1fr));
        gap: 24px; margin: 0 0 8px;
    }
    .siperti-info-step {
        background: #FFFFFF; border: 1px solid #CFDEEC;
        border-top: 4px solid #005BAC; border-radius: 12px; padding: 20px;
        box-shadow: 0 4px 14px rgba(0,59,115,.04);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .siperti-info-step:hover {
        transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,59,115,.09);
    }
    .siperti-info-step-number {
        display: grid; place-items: center; width: 34px; height: 34px;
        border-radius: 9px; background: #005BAC; color: #FFFFFF;
        font-size: 14px; font-weight: 800; margin-bottom: 14px;
    }
    .siperti-info-step h3, .siperti-info-scope h3, .siperti-info-data-group h3 {
        border: 0 !important; padding: 0 !important; margin: 0 0 8px !important;
        color: #153854; font-size: 16px !important; line-height: 1.5 !important;
    }
    .siperti-info-scopes, .siperti-info-data-grid {
        display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 20px 28px;
    }
    .siperti-info-scope { border-top: 1px solid #CFDEEC; padding: 18px 0; }
    .siperti-info-data-group code {
        display: inline-block; margin: 3px 3px 3px 0; padding: 3px 6px;
        border-radius: 5px; background: #F0F5FA; color: #245579;
        font-size: 13px; overflow-wrap: anywhere;
    }
    .siperti-info-status {
        border: 1px solid #C4DFF3; border-left: 4px solid #00859C;
        background: #EAF4FC; padding: 18px 22px; border-radius: 10px;
        margin-top: 6px; overflow-wrap: anywhere;
    }
    .siperti-info-status strong { color: #003B73; }
    @keyframes siperti-info-enter {
        from { opacity: .65; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 900px) {
        .siperti-info-steps { grid-template-columns: 1fr; gap: 14px; }
    }
    @media (max-width: 600px) {
        #siperti-info-hero { padding: 24px 20px; }
        .siperti-info-intro { align-items: flex-start; gap: 14px; padding: 18px; }
        .siperti-info-scopes, .siperti-info-data-grid { grid-template-columns: 1fr; }
    }
    @media (prefers-reduced-motion: reduce) {
        #siperti-info-hero, .siperti-info-step { animation: none; transition: none; }
        .siperti-info-step:hover { transform: none; }
    }
</style>
""")

st.html("""
<header id="siperti-info-hero">
    <div class="siperti-info-eyebrow">PLN UP3 GARUT | ANALITIK OPERASIONAL</div>
    <h1>SIPERTI</h1>
    <p>Pantau pembacaan meter, pahami kondisi setiap rute, dan siapkan laporan
    operasional dari satu tempat. SIPERTI membantu Anda mengubah data harian
    menjadi informasi yang lebih terstruktur dan mudah ditelusuri.</p>
</header>
""")

st.html("""
<div class="siperti-info-intro">
    <div class="siperti-info-monogram" aria-hidden="true">SI</div>
    <div>
        <strong>Data lebih terstruktur, pemantauan lebih terarah</strong>
        <p>Dari file Excel atau CSV, SIPERTI menyajikan ringkasan, grafik, peringkat
        RBM, peta, dan rapor rute. Gunakan informasi ini untuk melihat aktivitas
        pembacaan dan menelusuri kondisi yang perlu ditinjau lebih lanjut.</p>
    </div>
</div>
""")

st.html("""
<section class="siperti-info-section" aria-labelledby="siperti-flow-title">
    <h2 id="siperti-flow-title">Mulai dari tiga langkah sederhana</h2>
    <p>Siapkan data, telusuri hasilnya, lalu bawa ringkasannya ke laporan Anda.</p>
</section>
<div class="siperti-info-steps">
    <article class="siperti-info-step">
        <span class="siperti-info-step-number">1</span>
        <h3>Unggah data pembacaan</h3>
        <p>Pilih satu file Excel atau CSV melalui Manajemen File di bawah logo.
        Sistem memeriksa kolom dan menyiapkan data untuk dianalisis.</p>
    </article>
    <article class="siperti-info-step">
        <span class="siperti-info-step-number">2</span>
        <h3>Telusuri kondisi setiap rute</h3>
        <p>Atur filter ULP, hari baca, tanggal, dan RBM. Buka ringkasan,
        peringkat, peta, atau rapor untuk memahami hasil pembacaan lebih dekat.</p>
    </article>
    <article class="siperti-info-step">
        <span class="siperti-info-step-number">3</span>
        <h3>Siapkan laporan operasional</h3>
        <p>Periksa pratinjau pada menu Data Management, lalu unduh rekapitulasi
        Excel sesuai filter aktif sebagai bahan pelaporan dan peninjauan.</p>
    </article>
</div>
""")

st.html("""
<section class="siperti-info-section" aria-labelledby="siperti-data-title">
    <h2 id="siperti-data-title">Siapkan struktur data yang sesuai</h2>
    <p>Gunakan file .xlsx atau .csv dengan kelompok kolom berikut.</p>
</section>
""")

with st.expander("Lihat kelompok kolom yang diperlukan", expanded=False):
    st.html("""
    <div class="siperti-info-data-grid">
        <section class="siperti-info-data-group">
            <h3>Identitas pelanggan dan layanan</h3>
            <p><code>UP3</code> <code>ULP</code> <code>NAMA</code>
            <code>IDPEL</code> <code>TARIF</code> <code>DAYA</code></p>
        </section>
        <section class="siperti-info-data-group">
            <h3>Rute dan periode pembacaan</h3>
            <p><code>KD_PETUGAS</code> <code>KODE_RBM</code> <code>BLTH</code>
            <code>Column1</code> atau <code>HARI_BACA</code></p>
        </section>
        <section class="siperti-info-data-group">
            <h3>Waktu dan kondisi hasil</h3>
            <p><code>TANGGAL_PEMBACAAN</code> <code>JAM_PEMBACAAN</code>
            <code>KODE_PESAN</code> <code>DLPD</code> <code>PEMKWH</code></p>
        </section>
        <section class="siperti-info-data-group">
            <h3>Lokasi pembacaan</h3>
            <p><code>KOORDINAT_X</code> <code>KOORDINAT_Y</code></p>
        </section>
    </div>
    """)
    st.caption(
        "Pastikan nama kolom sesuai. Gunakan format jam HH:MM, misalnya 08:30. "
        "Column1 akan dikenali sebagai HARI_BACA; cukup sediakan salah satunya."
    )

st.html("""
<section class="siperti-info-section" aria-labelledby="siperti-scope-title">
    <h2 id="siperti-scope-title">Dari gambaran umum hingga rincian RBM</h2>
    <p>Pilih kedalaman informasi sesuai kebutuhan pemantauan Anda.</p>
</section>
<div class="siperti-info-scopes">
    <article class="siperti-info-scope">
        <h3>Pahami gambaran operasional</h3>
        <p>Lihat jumlah pembacaan, kondisi hasil, perbandingan antar-ULP,
        dan distribusi jam. Ringkasan ini membantu Anda mengenali pola
        pada periode serta wilayah yang dipilih.</p>
    </article>
    <article class="siperti-info-scope">
        <h3>Telusuri pembacaan per rute</h3>
        <p>Bandingkan RBM berdasarkan indikator pilihan, periksa sebaran titik,
        lalu telusuri histori serta kategori kendala pada rapor rute.
        Setiap rincian memberi konteks untuk peninjauan berikutnya.</p>
    </article>
</div>
""")

st.caption(
    "Analisis menggunakan statistik deskriptif. Peringkat RBM mengikuti "
    "indikator yang dipilih dan data yang tersedia pada filter aktif."
)

# Kondisi status data dipertahankan; hanya penyajian dan teks diperbarui.
if st.session_state.get("raw_data") is None:
    st.session_state["data_ready"] = False
    st.html("""
    <div class="siperti-info-status" role="status">
        <strong>Siap mulai menelusuri data?</strong>
        <p>Belum ada file aktif. Unggah data pembacaan melalui Manajemen File
        pada sidebar, lalu buka menu analisis yang Anda perlukan.</p>
    </div>
    """)
else:
    st.session_state["data_ready"] = True
    file_name = escape(str(st.session_state.get("loaded_file_name", "File aktif")))
    st.html(
        '<div class="siperti-info-status" role="status">'
        '<strong>Data siap ditelusuri</strong>'
        f'<p>File aktif: <b>{file_name}</b>. '
        'Mulai dari Dashboard Overview untuk melihat ringkasan, '
        'atau pilih menu lain untuk meninjau rute secara lebih rinci.</p>'
        '</div>'
    )
