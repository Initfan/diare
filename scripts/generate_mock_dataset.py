import csv
import random
import os

def generate_mock_dataset(filepath, num_rows=500):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    headers = [
        'ID_Pasien', 'Umur_bulan', 'Jenis_Kelamin', 'Lama_Diare_hari', 
        'Frekuensi_BAB_per_hari', 'Konsistensi_Feses', 'Warna_Feses', 'Ada_Lendir', 
        'Ada_Darah', 'Demam', 'Suhu_Tubuh_C', 'Muntah', 'Tanda_Dehidrasi', 
        'Diagnosis_Klinis_Awal', 'Tingkat_Keparahan_Diare'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        
        for i in range(1, num_rows + 1):
            id_pasien = f'P{i:04d}'
            umur = random.randint(1, 60)
            jk = random.choice(['Laki-laki', 'Perempuan'])
            
            # Simulate different severity profiles
            severity_rand = random.random()
            if severity_rand < 0.5:
                keparahan = 'Ringan'
                lama = random.randint(1, 3)
                frek = random.randint(3, 5)
                konsistensi = random.choice(['Lembek', 'Cair'])
                warna = random.choice(['Kuning', 'Kehijauan'])
                lendir = random.choice(['Ya', 'Tidak'])
                darah = 'Tidak'
                demam = 'Tidak'
                suhu = round(random.uniform(36.5, 37.5), 1)
                muntah = 'Tidak'
                dehidrasi = 'Tidak Ada'
                diagnosis = 'Diare Akut Tanpa Dehidrasi'
            elif severity_rand < 0.8:
                keparahan = 'Sedang'
                lama = random.randint(3, 7)
                frek = random.randint(5, 8)
                konsistensi = 'Cair'
                warna = random.choice(['Kehijauan', 'Kecoklatan'])
                lendir = 'Ya'
                darah = random.choice(['Ya', 'Tidak'])
                demam = random.choice(['Ya', 'Tidak'])
                suhu = round(random.uniform(37.5, 38.5), 1)
                muntah = random.choice(['Ya', 'Tidak'])
                dehidrasi = random.choice(['Ringan', 'Sedang'])
                diagnosis = 'Diare Akut Dehidrasi Ringan-Sedang'
            else:
                keparahan = 'Berat'
                lama = random.randint(5, 14)
                frek = random.randint(8, 15)
                konsistensi = 'Cair'
                warna = random.choice(['Kecoklatan', 'Kemerahan'])
                lendir = 'Ya'
                darah = 'Ya'
                demam = 'Ya'
                suhu = round(random.uniform(38.5, 40.0), 1)
                muntah = 'Ya'
                dehidrasi = 'Berat'
                diagnosis = 'Diare Akut Dehidrasi Berat'
                
            # Convert decimal separator to comma if needed based on loader logic
            # The loader handles comma or dot, so dot is fine.
            writer.writerow([
                id_pasien, umur, jk, lama, frek, konsistensi, warna, lendir, darah, 
                demam, str(suhu).replace('.', ','), muntah, dehidrasi, diagnosis, keparahan
            ])

if __name__ == '__main__':
    generate_mock_dataset('datasets/dataset_pasien_diare_anak_revisi.csv')
    print("Mock dataset generated at datasets/dataset_pasien_diare_anak_revisi.csv")
