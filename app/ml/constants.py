MODEL_FEATURES = [
    "Umur_bulan",
    "Jenis_Kelamin",
    "Lama_Diare_hari",
    "Frekuensi_BAB_per_hari",
    "Konsistensi_Feses",
    "Warna_Feses",
    "Ada_Lendir",
    "Ada_Darah",
    "Demam",
    "Suhu_Tubuh_C",
    "Muntah",
    "Tanda_Dehidrasi",
]

TARGET_COLUMN = "Tingkat_Keparahan_Diare"

EXCLUDED_COLUMNS = [
    "ID_Pasien",
    "Diagnosis_Klinis_Awal",
    "Tingkat_Keparahan_Diare", # excluded from features
]

NUMERIC_FEATURES = [
    "Umur_bulan",
    "Lama_Diare_hari",
    "Frekuensi_BAB_per_hari",
    "Suhu_Tubuh_C",
]

CATEGORICAL_FEATURES = [
    "Jenis_Kelamin",
    "Konsistensi_Feses",
    "Warna_Feses",
    "Ada_Lendir",
    "Ada_Darah",
    "Demam",
    "Muntah",
    "Tanda_Dehidrasi",
]

# Urutan yang diekspektasikan dari categories (berdasarkan deskripsi prompt)
EXPECTED_CATEGORIES = {
    "Jenis_Kelamin": ["Laki-laki", "Perempuan"],
    "Konsistensi_Feses": ["Cair", "Lembek"],
    "Warna_Feses": ["Kuning", "Kecoklatan", "Kehijauan", "Kemerahan"],
    "Ada_Lendir": ["Ya", "Tidak"],
    "Ada_Darah": ["Ya", "Tidak"],
    "Demam": ["Ya", "Tidak"],
    "Muntah": ["Ya", "Tidak"],
    "Tanda_Dehidrasi": ["Tidak Ada", "Ringan", "Sedang", "Berat"]
}
