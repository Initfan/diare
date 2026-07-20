import pandas as pd
import os

def load_dataset(dataset_path):
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset tidak ditemukan di path: {dataset_path}")
    
    # Dataset menggunakan format: separator ; dan decimal ,
    dataset = pd.read_csv(
        dataset_path,
        sep=";",
        decimal=",",
        encoding="utf-8-sig"
    )
    return dataset
