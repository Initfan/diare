import pandas as pd
from app.ml.constants import MODEL_FEATURES, TARGET_COLUMN, EXPECTED_CATEGORIES, NUMERIC_FEATURES

def validate_dataset(df: pd.DataFrame):
    """
    Validates the dataset before training.
    """
    errors = []
    
    if df.empty:
        errors.append("Dataset kosong.")
        return False, errors
        
    # Periksa kolom target
    if TARGET_COLUMN not in df.columns:
        errors.append(f"Kolom target '{TARGET_COLUMN}' tidak ditemukan dalam dataset.")
        
    # Periksa fitur wajib
    for feature in MODEL_FEATURES:
        if feature not in df.columns:
            errors.append(f"Fitur wajib '{feature}' tidak ditemukan dalam dataset.")
            
    if errors:
        return False, errors
        
    # Periksa kelas target (hanya boleh Ringan, Sedang, Berat)
    valid_classes = {"Ringan", "Sedang", "Berat"}
    actual_classes = set(df[TARGET_COLUMN].dropna().unique())
    if not actual_classes.issubset(valid_classes):
        errors.append(f"Target memiliki kelas tidak dikenal: {actual_classes - valid_classes}. Hanya boleh: {valid_classes}")
        
    if len(actual_classes) <= 1:
        errors.append("Hanya terdapat satu atau kurang kelas target. Model membutuhkan minimal dua kelas.")
        
    # Periksa nilai kategorikal di dataset
    for col, categories in EXPECTED_CATEGORIES.items():
        if col in df.columns:
            actual_cats = set(df[col].dropna().unique())
            valid_cats = set(categories)
            if not actual_cats.issubset(valid_cats):
                errors.append(f"Kolom '{col}' memiliki kategori tidak dikenal: {actual_cats - valid_cats}.")
                
    # Periksa apakah data numerik bisa dikonversi ke float
    for col in NUMERIC_FEATURES:
        if col in df.columns:
            try:
                pd.to_numeric(df[col])
            except ValueError:
                errors.append(f"Kolom numerik '{col}' mengandung data yang tidak bisa dikonversi menjadi angka.")

    # Periksa baris duplikat semua (exclude ID if exists to check real duplicates)
    df_no_id = df.drop(columns=['ID_Pasien'], errors='ignore')
    if df_no_id.duplicated().sum() == len(df_no_id) and len(df_no_id) > 1:
         errors.append("Semua baris dalam dataset adalah duplikat.")

    if errors:
        return False, errors
        
    return True, []
