# Sistem Deteksi Dini Tingkat Keparahan Diare Anak

Sistem Pendukung Keputusan Klinis (CDSS) untuk deteksi dini tingkat keparahan penyakit diare pada anak menggunakan algoritma **Naïve Bayes (CategoricalNB)**. Dibangun khusus untuk **Klinik Islamic Village**.

## 🌟 Fitur Utama
1. **Multi-Role Authentication**: Mendukung role Administrator, Dokter, Perawat, dan Petugas Administrasi.
2. **Manajemen Pasien**: Registrasi, pencarian, dan pengelolaan riwayat pasien.
3. **Form Skrining Klinis**: Pengisian 12 fitur klinis pasien.
4. **Prediksi Real-time**: Model Naïve Bayes memprediksi tingkat keparahan (Ringan, Sedang, Berat) dengan probabilitas masing-masing kelas.
5. **Validasi Dokter**: Fitur khusus Dokter untuk menyetujui, menolak, atau mengubah hasil prediksi.
6. **Manajemen Model**: Kemampuan melatih ulang model dengan dataset terbaru dan mengaktifkan versi model yang berbeda.
7. **Audit Log**: Pencatatan aktivitas pengguna (login, input pasien, prediksi, validasi) untuk keamanan data.

## 🛠 Teknologi yang Digunakan
- **Backend**: Python 3.13, Flask (Factory Pattern)
- **Database**: MySQL (Production) / SQLite (Development), SQLAlchemy ORM, Flask-Migrate
- **Machine Learning**: Scikit-Learn (CategoricalNB), KBinsDiscretizer, Joblib, Pandas
- **Frontend**: Jinja2 Templates, Tailwind CSS (CDN), Vanilla JS, Chart.js, Lucide Icons

## 🚀 Panduan Instalasi (Development)

### 1. Persiapan Environment
Pastikan Anda menggunakan Python 3.11 atau yang lebih baru.
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Environment
Salin `.env.example` ke `.env` dan sesuaikan nilainya:
```bash
copy .env.example .env
```
Pastikan `FLASK_ENV=development` untuk menggunakan SQLite, atau isi `DATABASE_URL` jika ingin menggunakan MySQL.

### 4. Inisialisasi Database
```bash
flask db upgrade
```

### 5. Generate Data Awal & Latih Model
Jalankan script seed untuk membuat role, user default, dan melatih model dengan mock dataset (atau dataset asli jika sudah ada di folder `datasets/`):
```bash
python scripts/generate_mock_dataset.py
python scripts/seed.py
python scripts/train_model.py
```

### 6. Menjalankan Aplikasi
```bash
python run.py
```
Aplikasi dapat diakses di `http://127.0.0.1:5000`.

## 🔐 Akun Default
Setelah menjalankan seed, Anda bisa login menggunakan akun berikut:
- **Admin**: `admin` / `Admin1234!`
- **Dokter**: `dokter1` / `Dokter1234!`
- **Perawat**: `perawat1` / `Perawat1234!`
- **Administrasi**: `admin_rina` / `Rina1234!`

## 🧪 Evaluasi Model
Model Naïve Bayes dievaluasi menggunakan macro-averaged F1-Score karena dataset seringkali *imbalanced* pada kelas target penyakit. Model disimpan dalam bentuk file `pipeline.joblib` yang mencakup preprocessing (discretization numerik) dan model CategoricalNB.

## 📄 Struktur Direktori
```
diarrhea-detection-app/
├── app/
│   ├── audit/             # Modul audit log
│   ├── auth/              # Autentikasi pengguna
│   ├── dashboard/         # Tampilan ringkasan dashboard
│   ├── examinations/      # Modul pemeriksaan klinis & prediksi
│   ├── ml/                # Logika machine learning, training, preprocessing
│   ├── models/            # SQLAlchemy Database Models
│   ├── patients/          # Modul manajemen data pasien
│   ├── static/            # CSS/JS tambahan
│   ├── templates/         # UI templates (Jinja2)
│   ├── validations/       # Fitur validasi oleh dokter
│   ├── __init__.py        # App Factory configuration
│   ├── config.py          # Class-based configurations
│   └── extensions.py      # Flask extensions
├── datasets/              # Folder penyimpanan dataset CSV
├── migrations/            # Alembic DB migrations
├── scripts/               # Scripts untuk seeding, training, mock data
├── tests/                 # Unit tests (Pytest)
├── requirements.txt       # Dependencies
└── run.py                 # Entry point Flask
```
