# 🍎 FruitVision AI

FruitVision AI adalah aplikasi berbasis **Streamlit** yang memanfaatkan **Google Gemini AI** untuk menganalisis kondisi buah dari gambar. Pengguna dapat mengambil foto menggunakan kamera atau mengunggah gambar dari perangkat, kemudian AI akan memberikan informasi mengenai kondisi buah.

## Fitur

- 📷 Ambil gambar menggunakan kamera
- 📁 Upload gambar dari perangkat
- 🤖 Analisis gambar menggunakan Google Gemini AI
- 🍎 Identifikasi jenis buah
- 🟢 Menentukan tingkat kematangan buah
- ❤️ Menentukan kelayakan konsumsi
- 🐛 Mendeteksi indikasi hama
- 🍂 Mendeteksi indikasi pembusukan
- 💡 Memberikan deskripsi dan saran

## Teknologi

- Python
- Streamlit
- Google Gemini API (gemini-2.5-flash)
- Pillow

## Instalasi

Clone repository:

```bash
git clone https://github.com/USERNAME/Deteksi_Kematangan_Buah.git
cd Deteksi_Kematangan_Buah
```

Install dependency:

```bash
pip install -r requirements.txt
```

Buat file:

```
.streamlit/secrets.toml
```

Isi dengan:

```toml
GEMINI_API_KEY="API_KEY_ANDA"
```

Jalankan aplikasi:

```bash
streamlit run app.py
```

## Struktur Project

```
Deteksi_Kematangan_Buah/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

## Cara Menggunakan

1. Jalankan aplikasi.
2. Ambil foto menggunakan kamera atau upload gambar buah.
3. Klik tombol **Analisis Buah**.
4. Tunggu beberapa saat hingga AI selesai menganalisis.
5. Hasil analisis akan ditampilkan pada halaman aplikasi.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan tugas kuliah.
