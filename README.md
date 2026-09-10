# SIPERTI

**Dashboard Analitik Pembacaan Meter | PLN UP3 Garut**

SIPERTI merupakan aplikasi berbasis web untuk mengolah data pembacaan meter dari file Excel atau CSV menjadi ringkasan operasional, grafik interaktif, peringkat Rute Baca Meter (RBM), peta sebaran pembacaan, dan laporan Excel.

Aplikasi ini mendukung kegiatan monitoring pembacaan meter di PLN UP3 Garut melalui statistik deskriptif. Pengguna dapat meninjau data menurut ULP, hari baca, tanggal, dan kode RBM tanpa melakukan pengelompokan serta perhitungan ringkasan secara manual di setiap tampilan.

## Tujuan dan ruang lingkup

SIPERTI membantu pengguna memahami jumlah pembacaan yang tercatat, kondisi hasil pembacaan, distribusi waktu, dan sebaran titik pelanggan pada data yang diunggah. Informasi tersebut dapat digunakan sebagai bahan peninjauan operasional dan penelusuran kendala per rute.

Objek pengelompokan untuk peringkat dan rapor adalah **RBM**, berdasarkan kolom `KODE_RBM`. Identitas petugas ditampilkan sebagai informasi pelaksana pembacaan pada rute tersebut. Beberapa nama menu dan berkas masih menggunakan istilah petugas; penjelasan dalam dokumentasi ini mengikuti proses pengolahan data pada kode aplikasi.

## Fitur dan menu

| Menu pada sidebar | Fungsi |
| --- | --- |
| **Information** | Menampilkan pengantar aplikasi, format data, panduan penggunaan, dan status ketersediaan data. |
| **Dashboard Overview** | Menampilkan metrik utama, perbandingan pembacaan antar-ULP, status verifikasi, distribusi kendala, tren jam pembacaan, dan tabel rekapitulasi per ULP. |
| **Leaderboard** | Mengurutkan RBM berdasarkan indikator yang dipilih, menampilkan tiga RBM teratas, grafik peringkat, serta tabel dengan pencarian kode RBM, petugas, atau ULP. |
| **Workforce & Spatial** | Menampilkan titik pembacaan pada peta, filter kondisi hasil pembacaan, ringkasan titik terpetakan, dan rincian data. |
| **Officer Tracking** | Menampilkan rapor RBM terpilih, petugas yang tercatat, ringkasan capaian, progres hari baca, histori pembacaan, dan rincian kendala. |
| **Data Management** | Menampilkan pratinjau rekapitulasi dan menyediakan unduhan laporan Excel berdasarkan data yang telah difilter. |

### Filter bersama

Halaman analisis menyediakan filter **ULP**, **hari baca**, **rentang tanggal**, dan **kode RBM**. Nilai filter disimpan dalam sesi aplikasi dan digunakan pada halaman yang menerapkan filter bersama. Hasil metrik, grafik, peringkat, dan laporan mengikuti pilihan filter yang berlaku pada halaman tersebut.

### Pengelolaan file

Bagian **Manajemen File** berada tepat di bawah logo, sebelum navigasi. Versi ini menerima **satu file aktif** dalam format `.xlsx` atau `.csv`. Setelah file berhasil diproses, sidebar menampilkan nama file aktif dan tombol **Reset File** untuk mengganti sumber data.

### Tampilan antarmuka

Tema biru-putih diterapkan melalui komponen UI bersama: banner judul bergradasi, sidebar putih, area metrik dan grafik, filter, serta tombol. Efek hover dan animasi kemunculan judul dibuat ringan. Animasi mengikuti pengaturan pengurangan gerakan pada perangkat pengguna.

## Statistik deskriptif dan peringkat RBM

Pengolahan menggunakan jumlah, frekuensi, persentase, pengelompokan kategori, dan rentang waktu yang tercatat. Peringkat diperoleh dengan mengurutkan nilai indikator pilihan pengguna secara langsung.

| Pilihan pengurutan | Arah urutan |
| --- | --- |
| Volume Pembacaan Terbanyak | Volume terbesar ke terkecil. |
| Ketercapaian Target Tertinggi | Persentase ketercapaian terbesar ke terkecil. |
| Kendala Lapangan Terendah | Persentase kendala terkecil ke terbesar. |

Jika nilai indikator sama, kode menggunakan volume pembacaan sebagai pengurutan tambahan secara menurun. Nomor peringkat diberikan berurutan pada hasil pengurutan.

### Arti indikator pada rekapitulasi RBM

| Indikator | Definisi pada implementasi |
| --- | --- |
| Total target | Jumlah entri `IDPEL` yang dihitung dalam kelompok RBM pada data aktif. |
| Volume pembacaan | Menggunakan nilai total target pada kelompok RBM tersebut. |
| Sukses normal | Jumlah baris dengan `DLPD` sama dengan `NORMAL` setelah diubah menjadi huruf besar. |
| Kendala/anomali | Jumlah baris dengan `DLPD` selain `NORMAL` pada agregasi RBM. |
| Ketercapaian (%) | Sukses normal dibagi total target, dikalikan 100. |
| Anomali (%) | 100 dikurangi ketercapaian. |
| Kepatuhan waktu (%) | Proporsi pembacaan dengan komponen jam 06 sampai 17, terhadap total target. |
| Durasi waktu | Selisih jam pembacaan paling akhir dan paling awal dalam kelompok RBM, ditampilkan sebagai jam dan menit. |

**Catatan interpretasi:** total target berasal dari catatan yang diunggah, bukan dari daftar target eksternal. Entri pelanggan berulang dapat ikut menambah hitungan karena agregasi tidak menghitung pelanggan unik. Durasi dihitung dari kolom jam, sehingga tidak mewakili akumulasi jam kerja atau selisih tanggal untuk data lintas hari.

Klasifikasi normal belum seragam di semua tampilan: KPI Overview mencari teks yang mengandung `NORMAL`, agregasi RBM memakai kecocokan tepat `NORMAL`, sedangkan rincian kendala pada rapor juga mengenali `Z - NORMAL` dan `Z`. Gunakan nilai kondisi yang konsisten dan perhatikan perbedaan ini saat membandingkan hasil antarhalaman.

## Format data masukan

Siapkan file dengan nama kolom berikut. Nama kolom harus sesuai, termasuk huruf besar dan tanda garis bawah.

| Kolom | Keterangan dan format yang disarankan |
| --- | --- |
| `UP3` | Identitas unit pelaksana pelayanan pelanggan. |
| `ULP` | Identitas unit layanan pelanggan. |
| `NAMA` | Nama pelanggan pada catatan sumber. |
| `IDPEL` | Identitas pelanggan; gunakan format teks untuk menjaga digit awal. |
| `TARIF` | Kode tarif pelanggan. |
| `DAYA` | Daya pelanggan. |
| `BLTH` | Periode bulan dan tahun pada sumber data. |
| `KD_PETUGAS` | Kode pelaksana atau akun pencatat pembacaan. |
| `KODE_RBM` | Kode Rute Baca Meter sebagai dasar pengelompokan. |
| `TANGGAL_PEMBACAAN` | Tanggal pembacaan; gunakan tanggal Excel yang valid atau teks `YYYY-MM-DD`. |
| `JAM_PEMBACAAN` | Jam pembacaan dalam format `HH:MM`, misalnya `08:30`. |
| `KODE_PESAN` | Kode atau status verifikasi pembacaan. |
| `KOORDINAT_X` | Pada halaman spasial mula-mula digunakan sebagai bujur. |
| `KOORDINAT_Y` | Pada halaman spasial mula-mula digunakan sebagai lintang. |
| `DLPD` | Kategori kondisi hasil pembacaan. |
| `PEMKWH` | Pemakaian energi dalam kWh, berupa angka. |
| `Column1` atau `HARI_BACA` | Penanda hari baca. `Column1` otomatis diganti namanya menjadi `HARI_BACA`. Cukup gunakan salah satu. |

Kode hari `A`, `B`, `C`, `D`, dan `E` dipetakan menjadi Hari 1 sampai Hari 5. Untuk CSV, gunakan pemisah koma. Letakkan nama kolom pada baris pertama; pembacaan Excel menggunakan lembar pertama secara bawaan.

Halaman spasial memiliki pemeriksaan sederhana untuk menukar sumbu koordinat jika dideteksi terbalik. Tetap periksa kesesuaian posisi titik dengan sumber data. Peta menampilkan hingga 5.000 baris pertama dengan koordinat numerik yang tersedia setelah filter, sehingga jumlah titik pada peta dapat lebih kecil daripada keseluruhan catatan.

Kode `SWACAMMOB` tetap berada dalam kelompok RBM sesuai `KODE_RBM`. Pada pengaturan awal, daftar pengecualian akun kosong sehingga catatan tersebut tetap masuk pengolahan. Daftar akun yang ditampilkan dapat mencakup kode ini sebagaimana tercatat dalam sumber data.

## Alur penggunaan

1. Jalankan aplikasi dan buka alamat yang ditampilkan di terminal.
2. Unggah Excel atau CSV melalui **Manajemen File** pada sidebar.
3. Tunggu validasi kolom dan pengolahan data selesai. Jika muncul pesan kolom hilang, sesuaikan berkas sumber sebelum mengunggah ulang.
4. Buka **Dashboard Overview** untuk meninjau ringkasan dan mengatur filter.
5. Gunakan **Leaderboard** untuk memilih indikator pengurutan dan mencari RBM yang ingin ditinjau.
6. Buka **Workforce & Spatial** atau **Officer Tracking** untuk menelusuri sebaran pembacaan dan rincian rute.
7. Buka **Data Management**, periksa pratinjau, lalu unduh rekapitulasi dalam format Excel.
8. Untuk mengganti dataset, klik **Reset File**, unggah file baru, lalu periksa kembali pilihan filter.

Otomatisasi dimulai setelah pengguna mengunggah file: aplikasi melakukan validasi, penyesuaian format, perhitungan, dan penyajian informasi. Data aktif dikelola dalam sesi Streamlit, sehingga pengguna perlu mengunggah kembali file ketika sesi baru dimulai.

## Instalasi dan menjalankan aplikasi

Panduan Windows berikut menggunakan Python 3.11 dan virtual environment proyek. Komponen tema telah diperiksa menggunakan Streamlit 1.63.0.

### Windows PowerShell

Unduh atau clone repository, lalu masuk ke folder yang berisi `app.py` dan `requirements.txt`. Contoh lokasi:

```powershell
cd D:\Meter_Analisis_metode_deskriptif
```

Jika belum ada virtual environment, buat dengan:

```powershell
py -3.11 -m venv .venv
```

Pasang dependensi dan jalankan aplikasi menggunakan Python dari lingkungan tersebut:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Perintah di atas tidak memerlukan aktivasi virtual environment. Buka alamat lokal yang ditampilkan terminal. Untuk menghentikan aplikasi, tekan `Ctrl + C`.

### Linux atau macOS

Dari folder utama proyek:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

### Pemeriksaan lingkungan Python

Jika VS Code menampilkan peringatan impor, pilih interpreter proyek melalui **Python: Select Interpreter**. Pada Windows, arahkan ke `.venv\Scripts\python.exe` di folder proyek yang sedang digunakan.

```powershell
.\.venv\Scripts\python.exe -c "import streamlit, pandas; print(streamlit.__version__); print(streamlit.__file__)"
```

Gunakan interpreter yang sama untuk memasang dependensi dan menjalankan aplikasi.

## Struktur proyek

| Lokasi | Peran |
| --- | --- |
| `app.py` | Titik masuk aplikasi dan halaman informasi. |
| `pages/2_Executive_Overview.py` | Ringkasan metrik, grafik, dan rekapitulasi ULP. |
| `pages/3_Leaderboard.py` | Pengurutan RBM dan pencarian pada tabel peringkat. |
| `pages/4_Analisis_Spasial.py` | Pemetaan pembacaan dan penelusuran kendala. |
| `pages/5_Rapor_Petugas.py` | Rapor dan histori pembacaan untuk RBM terpilih. |
| `pages/6_Laporan_Ekspor.py` | Pratinjau dan unduhan laporan. |
| `src/data_loader.py` | Pembacaan file, validasi kolom, dan sidebar. |
| `src/preprocessor.py` | Penyesuaian hari baca, kode RBM, koordinat, dan jam. |
| `src/metrics_engine.py` | Agregasi indikator deskriptif per RBM. |
| `src/visualizer.py` | Pembuatan grafik dan peta menggunakan Plotly. |
| `src/export_report.py` | Pembuatan laporan Excel. |
| `src/ui.py` | Tema bersama, komponen filter, dan penerapan filter. |
| `assets/Logo_PLN.png` | Aset logo yang tersedia dalam repository. |
| `.streamlit/config.toml` | Konfigurasi tema, navigasi, dan server. |
| `requirements.txt` | Daftar dependensi aplikasi. |

## Teknologi

| Teknologi | Penggunaan |
| --- | --- |
| Python | Bahasa pemrograman aplikasi. |
| Streamlit | Antarmuka web, navigasi, widget, dan sesi pengguna. |
| pandas dan NumPy | Pengolahan data dan operasi numerik. |
| Plotly | Grafik interaktif dan peta. |
| python-calamine dan openpyxl | Pembacaan file Excel. |
| XlsxWriter | Pembuatan berkas laporan Excel. |

Dependensi lengkap mengikuti `requirements.txt`. Ekspor yang tersedia melalui tombol laporan pada versi ini adalah `.xlsx`.

## Pemecahan masalah

| Kendala | Langkah pemeriksaan |
| --- | --- |
| `ModuleNotFoundError` | Pasang `requirements.txt` menggunakan Python dari `.venv` proyek. |
| File ditolak karena kolom hilang | Cocokkan nama kolom dengan tabel format data, termasuk `Column1` atau `HARI_BACA`. |
| Data tidak muncul setelah filter | Periksa ULP, hari, tanggal, dan RBM yang dipilih, terutama setelah mengganti file. |
| Analisis jam kosong atau tidak sesuai | Pastikan `JAM_PEMBACAAN` berupa `HH:MM`. |
| Titik tidak tampil di peta | Periksa koordinat numerik, urutan lintang/bujur, serta koneksi untuk memuat peta dasar. |
| Tampilan berbeda antarlingkungan | Pastikan `src/ui.py` dan `.streamlit/config.toml` yang digunakan adalah versi yang sama, lalu jalankan ulang aplikasi. |
| CSS tampil sebagai teks | Gunakan versi `src/ui.py` yang menyisipkan CSS melalui `st.html()`. |

## Memperbarui dokumentasi di GitHub

Simpan dokumen ini sebagai `README.md` di folder utama, sejajar dengan `app.py`. Jika sedang berada di branch `master`, periksa lalu kirim perubahan dokumentasi saja:

```powershell
git branch --show-current
git --no-pager diff -- README.md
git add README.md
git --no-pager diff --cached --stat
git commit -m "docs: perbarui panduan SIPERTI dan statistik deskriptif"
git push origin master
```

Pastikan daftar staged hanya memuat perubahan yang ingin dikirim. Jika Git melaporkan konflik atau menolak push, selesaikan pesan tersebut sebelum melanjutkan.
