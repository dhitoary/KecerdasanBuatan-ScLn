import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def muat_data_diabetes(jalur_data):

    print(f"Memuat data dari: {jalur_data}")
    try:
        data = pd.read_csv(jalur_data)
        print("Data berhasil dimuat. Beberapa baris pertama:")
        print(data.head())
        print("\nStatistik deskriptif data:")
        print(data.describe())

        kolom_cek_nol = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        
        for kol in kolom_cek_nol:
            data[kol] = data[kol].replace(0, pd.NA)
        
        print("\nJumlah nilai hilang (NaN) setelah penggantian 0:")
        print(data.isnull().sum())

        for kol in kolom_cek_nol:
            if data[kol].isnull().any():
                data[kol] = data[kol].fillna(data[kol].mean())
        
        print("\nJumlah nilai hilang setelah diisi dengan rata-rata:")
        print(data.isnull().sum())
        return data

    except FileNotFoundError:
        print(f"ERROR: File tidak ditemukan di {jalur_data}. Pastikan 'diabetes.csv' ada di folder yang sama.")
        return None
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat memuat atau pra-pemrosesan data: {e}")
        return None

def pra_proses_data(data):
    
    if data is None:
        print("Data belum dimuat. Pra-pemrosesan tidak bisa dilakukan.")
        return None, None, None, None, None

    print("\nMemulai pra-pemrosesan data...")
    fitur = data.drop('Outcome', axis=1)
    target = data['Outcome']

    fitur_train, fitur_test, target_train, target_test = train_test_split(
        fitur, target, test_size=0.2, random_state=42, stratify=target
    )
    print(f"Ukuran data pelatihan: {fitur_train.shape}")
    print(f"Ukuran data pengujian: {fitur_test.shape}")

    scaler = StandardScaler()
    fitur_train_skala = scaler.fit_transform(fitur_train)
    fitur_test_skala = scaler.transform(fitur_test)
    print("Fitur berhasil distandardisasi (diskalakan).")

    return fitur_train_skala, fitur_test_skala, target_train, target_test, scaler

def latih_model_svm(fitur_train_skala, target_train):

    if fitur_train_skala is None or target_train is None:
        print("Data pelatihan belum siap. Model tidak bisa dilatih.")
        return None

    print("\nMelatih model Support Vector Machine (SVM)...")
    model_svm = SVC(kernel='rbf', random_state=42) 
    model_svm.fit(fitur_train_skala, target_train)
    print("Model SVM berhasil dilatih.")
    return model_svm

def evaluasi_model(model, fitur_test_skala, target_test, nama_target):

    if model is None or fitur_test_skala is None or target_test is None:
        print("Model atau data pengujian belum siap. Evaluasi tidak bisa dilakukan.")
        return

    print("\nMengevaluasi kinerja model...")
    prediksi_y = model.predict(fitur_test_skala)

    akurasi = accuracy_score(target_test, prediksi_y)
    print(f"Akurasi Model: {akurasi:.4f}")

    print("\nLaporan Klasifikasi:")
    print(classification_report(target_test, prediksi_y, target_names=nama_target))

    matriks_konfusi = confusion_matrix(target_test, prediksi_y)
    print("\nMatriks Konfusi:")
    print(matriks_konfusi)

    plt.figure(figsize=(8, 6))
    sns.heatmap(matriks_konfusi, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=nama_target,
                yticklabels=nama_target)
    plt.xlabel('Prediksi')
    plt.ylabel('Aktual')
    plt.title('Matriks Konfusi Prediksi Risiko Diabetes')
    plt.show()

def prediksi_pasien_baru(model, scaler, fitur_mentah_pasien, nama_target):
    
    if model is None or scaler is None:
        print("Model atau scaler belum siap. Prediksi tidak bisa dilakukan.")
        return "ERROR: Model belum dilatih atau scaler belum disiapkan."

    nama_fitur = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    data_pasien_df = pd.DataFrame([fitur_mentah_pasien], columns=nama_fitur)

    fitur_pasien_skala = scaler.transform(data_pasien_df)

    prediksi_numerik = model.predict(fitur_pasien_skala)
    
    hasil_prediksi_label = nama_target[prediksi_numerik[0]]
    
    return hasil_prediksi_label

if __name__ == "__main__":
    lokasi_data = 'diabetes.csv' 

    nama_kelas_target = ['Tidak Diabetes', 'Diabetes']

    data_diabetes = muat_data_diabetes(lokasi_data)
    
    if data_diabetes is not None:
        fitur_train_skala, fitur_test_skala, target_train, target_test, scaler_data = \
            pra_proses_data(data_diabetes)

        if fitur_train_skala is not None:
            model_svm_final = latih_model_svm(fitur_train_skala, target_train)

            if model_svm_final is not None:
                evaluasi_model(model_svm_final, fitur_test_skala, target_test, nama_kelas_target)

                print("\n--- Contoh Prediksi untuk Pasien Baru ---")
                
                pasien_baru_1 = [6, 148, 72, 35, 0, 33.6, 0.627, 50] 
                print(f"\nParameter Pasien 1: {pasien_baru_1}")
                prediksi_1 = prediksi_pasien_baru(model_svm_final, scaler_data, pasien_baru_1, nama_kelas_target)
                print(f"PREDIKSI RISIKO DIABETES PASIEN 1: {prediksi_1}")

                pasien_baru_2 = [1, 85, 66, 29, 0, 26.6, 0.351, 31] 
                print(f"\nParameter Pasien 2: {pasien_baru_2}")
                prediksi_2 = prediksi_pasien_baru(model_svm_final, scaler_data, pasien_baru_2, nama_kelas_target)
                print(f"PREDIKSI RISIKO DIABETES PASIEN 2: {prediksi_2}")

                print("\n--- COBA INPUT PARAMETER PASIEN SENDIRI ---")
                print("Masukkan 8 parameter klinis sesuai urutan ini:")
                print("Kehamilan (jumlah), Glukosa (mg/dL), Tekanan Darah (mmHg), Ketebalan Kulit (mm), Insulin (muU/ml), BMI, Fungsi Silsilah Diabetes, Usia")
                try:
                    p_input = float(input("Kehamilan: "))
                    g_input = float(input("Glukosa: "))
                    bp_input = float(input("Tekanan Darah: "))
                    st_input = float(input("Ketebalan Kulit: "))
                    ins_input = float(input("Insulin: "))
                    bmi_input = float(input("BMI: "))
                    dpf_input = float(input("Fungsi Silsilah Diabetes: "))
                    age_input = float(input("Usia: "))
                    
                    parameter_input_pengguna = [p_input, g_input, bp_input, st_input, ins_input, bmi_input, dpf_input, age_input]
                    print(f"\nParameter Anda: {parameter_input_pengguna}")
                    prediksi_pengguna = prediksi_pasien_baru(model_svm_final, scaler_data, parameter_input_pengguna, nama_kelas_target)
                    print(f"PREDIKSI RISIKO DIABETES ANDA: {prediksi_pengguna}")
                except ValueError:
                    print("Input tidak valid. Harap masukkan angka untuk setiap parameter.")
