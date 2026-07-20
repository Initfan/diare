from app.ml.constants import MODEL_FEATURES, EXPECTED_CATEGORIES, NUMERIC_FEATURES

NUMERIC_RANGES = {
    "Umur_bulan": (1, 57),
    "Lama_Diare_hari": (1, 30),
    "Frekuensi_BAB_per_hari": (3, 15),
    "Suhu_Tubuh_C": (36.2, 39.8),
}


def validate_prediction_input(input_data: dict) -> tuple[bool, list, list]:
    """
    Validates input for prediction.
    Returns: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Periksa kelengkapan fitur
    for feature in MODEL_FEATURES:
        if feature not in input_data or input_data[feature] is None or input_data[feature] == '':
            errors.append(f"Fitur '{feature}' wajib diisi.")
    
    if errors:
        return False, errors, warnings
    
    # Validasi kategorikal
    for col, valid_cats in EXPECTED_CATEGORIES.items():
        if col in input_data:
            val = input_data[col]
            if val not in valid_cats:
                errors.append(
                    f"Nilai '{val}' pada kolom '{col}' tidak valid. "
                    f"Pilihan yang tersedia: {', '.join(valid_cats)}"
                )
    
    # Validasi numerik
    try:
        umur = int(input_data.get("Umur_bulan", 0))
        if umur < 1:
            errors.append("Umur harus bilangan bulat positif (minimal 1 bulan).")
    except (ValueError, TypeError):
        errors.append("Umur harus berupa bilangan bulat.")
    
    try:
        lama = int(input_data.get("Lama_Diare_hari", 0))
        if lama < 1:
            errors.append("Lama diare harus bilangan bulat positif (minimal 1 hari).")
    except (ValueError, TypeError):
        errors.append("Lama diare harus berupa bilangan bulat.")
    
    try:
        frek = int(input_data.get("Frekuensi_BAB_per_hari", 0))
        if frek < 1:
            errors.append("Frekuensi BAB harus bilangan bulat positif.")
    except (ValueError, TypeError):
        errors.append("Frekuensi BAB harus berupa bilangan bulat.")
    
    try:
        suhu = float(input_data.get("Suhu_Tubuh_C", 0))
        if suhu <= 0:
            errors.append("Suhu tubuh harus berupa angka desimal positif.")
    except (ValueError, TypeError):
        errors.append("Suhu tubuh harus berupa angka desimal.")
    
    if errors:
        return False, errors, warnings
    
    # Peringatan rentang di luar data pelatihan
    numeric_values = {
        "Umur_bulan": int(input_data["Umur_bulan"]),
        "Lama_Diare_hari": int(input_data["Lama_Diare_hari"]),
        "Frekuensi_BAB_per_hari": int(input_data["Frekuensi_BAB_per_hari"]),
        "Suhu_Tubuh_C": float(input_data["Suhu_Tubuh_C"]),
    }
    
    for col, value in numeric_values.items():
        min_val, max_val = NUMERIC_RANGES[col]
        if value < min_val or value > max_val:
            warnings.append(
                f"Nilai '{col}' ({value}) berada di luar rentang data pelatihan "
                f"({min_val} - {max_val}). Prediksi mungkin kurang akurat."
            )
    
    return True, [], warnings
