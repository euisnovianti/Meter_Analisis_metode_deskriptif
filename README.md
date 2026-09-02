# SIPERTI (Sistem Informasi Performa & Evaluasi Rute Petugas Terintegrasi) deskriptif

SIPERTI adalah platform analitik interaktif berbasis web untuk memantau, mengevaluasi, dan menganalisis performa operasional pembacaan meter listrik pelanggan PLN secara terpusat, akurat, dan adaptif.

---

## 📌 Fitur Utama

- **Executive Overview & Global Control Bar**
  - Pemantauan KPI operasional utama (*Total Target, Total Meter Terbaca, Jumlah Petugas Aktif*).
  - Sistem filter global (*ULP, Hari Baca, Rentang Tanggal, Kode RBM*) yang persisten antar menu.
  - Visualisasi interaktif status verifikasi bacaan lapangan (DLPD) serta analisis anomali kendala.

- **Leaderboard Kinerja (Dual-Engine Evaluation)**
  - **Metode SAW (Simple Additive Weighting):** Pemeringkatan multi-kriteria berbasis kriteria *Benefit* (Target Ketercapaian, Volume Baca) dan *Cost* (Kecepatan/Waktu, Anomali/Kendala).
  - **Historis Deskriptif:** Rekapitulasi murni metrik operasional tanpa pembobotan matematis.
  - KPI dinamis adaptif yang otomatis menyesuaikan konteks metode evaluasi yang dipilih.

- **Analisis Spasial & Distribusi Beban Kerja**
  - Pemetaan titik persebaran pembacaan meter dan jalur RBM pelanggan.
  - Visualisasi beban kerja operasional per unit wilayah layanan (ULP).

- **Rapor Kinerja Petugas (Officer Tracking)**
  - Rekam jejak dan metrik capaian individu petugas pembaca meter.
  - Tabel rincian verifikasi bacaan pelanggan (Normal vs Temuan Kendala).

- **Laporan & Ekspor Data**
  - Ekspor hasil pemrosesan, leaderboard, dan data tabular ke format CSV/Excel.
  - Manajemen unduhan data siap pakai untuk tindak lanjut operasional lapangan.

---

## 🛠️ Tech Stack

- **Core Framework:** Python, Streamlit
- **Data Engineering:** Pandas, NumPy
- **Visual Analytics:** Plotly Express, Plotly Graph Objects
- **Decision Engine:** Simple Additive Weighting (SAW) Algorithm

---

## 📁 Struktur Direktori Proyek

```text
meterops-analytics/
├── pages/
│   ├── 2_Executive_Overview.py   # Ringkasan KPI makro & grafik kontrol global
│   ├── 3_Leaderboard.py          # Peringkat kinerja (Metode SAW & Historis)
│   ├── 4_Analisis_Spasial.py     # Pemetaan rute & beban spasial
│   ├── 5_Rapor_Petugas.py        # Profil performa & tracking individu petugas
│   └── 6_Laporan_Ekspor.py       # Ekspor laporan & manajemen data hasil olah
├── src/
│   ├── __init__.py               # Package initializer
│   ├── data_loader.py            # Modul input data, validasi, & sidebar uploader
│   ├── export_report.py          # Utilitas pembuatan & ekspor berkas laporan
│   ├── preprocessor.py           # Pembersihan, standarisasi, & agregasi data mentah
│   ├── saw_engine.py             # Algoritma normalisasi & kalkulasi nilai preferensi SAW
│   ├── ui.py                     # Komponen UI styling, badge, & kartu metrik
│   └── visualizer.py             # Fungsi render grafik Plotly (Donut, Bar, Spatial)
├── data/                         # Direktori penyimpanan data lokal/sample
├── .streamlit/                   # Konfigurasi tema & server Streamlit
├── app.py                        # Titik masuk utama aplikasi (Landing / Home)
├── requirements.txt              # Daftar pustaka & dependensi Python
├── .gitignore                    # Berkas pengecualian Git
└── README.md                     # Dokumentasi teknis proyek

```
---


## Panduan Mejalanakan Aplikasi
**1. Clone Repository**
- git clone [https://github.com/username/meterops-analytics.git](https://github.com/username/meterops-analytics.git)
- cd meterops-analytics

**2. Buat dan Aktifkan**
- python -m venv .venv
**Windows (PowerShell/CMD):
- .venv\Scripts\activate
**Linux / macOS:
- source .venv/bin/activate

**3. Pasang dependensi**
- pip install -r requirements.txt

**4. jalankan dashboard**
- streamlit run app.py
