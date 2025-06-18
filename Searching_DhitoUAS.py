import collections

def cari_jalur_bfs_sederhana(peta, mulai, tujuan):

    baris_max = len(peta)
    kolom_max = len(peta[0])

    arah_gerak = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def apakah_valid(r, c):
        return 0 <= r < baris_max and 0 <= c < kolom_max and peta[r][c] == 0

    if not apakah_valid(mulai[0], mulai[1]):
        print(f"ERROR: Posisi mulai {mulai} tidak valid (di luar peta atau rintangan).")
        return None
    if not apakah_valid(tujuan[0], tujuan[1]):
        print(f"ERROR: Posisi tujuan {tujuan} tidak valid (di luar peta atau rintangan).")
        return None
    
    if mulai == tujuan:
        return [mulai]

    antrean = collections.deque([(mulai)])
    sudah_dikunjungi = {mulai}
    peta_parent = {mulai: None}

    while antrean:
        baris_skrg, kolom_skrg = antrean.popleft()

        if (baris_skrg, kolom_skrg) == tujuan:
            print(f"Jalur ditemukan dari {mulai} ke {tujuan}!")
            jalur = []
            node_saat_ini = tujuan
            while node_saat_ini != mulai:
                jalur.append(node_saat_ini)
                node_saat_ini = peta_parent[node_saat_ini]
            jalur.append(mulai)
            return jalur[::-1]

        for dr, dc in arah_gerak:
            baris_berikut, kolom_berikut = baris_skrg + dr, kolom_skrg + dc
            node_berikut = (baris_berikut, kolom_berikut)

            if apakah_valid(baris_berikut, kolom_berikut) and node_berikut not in sudah_dikunjungi:
                sudah_dikunjungi.add(node_berikut)
                antrean.append(node_berikut)
                peta_parent[node_berikut] = (baris_skrg, kolom_skrg)
    
    print(f"Tidak ada jalur yang ditemukan dari {mulai} ke {tujuan}.")
    return None

def tampilkan_peta_dan_jalur(peta, jalur, mulai, tujuan):
    if jalur is None:
        print("\nTidak ada jalur untuk divisualisasikan.")
        return

    jalur_set = set(jalur)

    print("\nVisualisasi Jalur:")
    for r in range(len(peta)):
        for c in range(len(peta[0])):
            pos_saat_ini = (r, c)
            if pos_saat_ini == mulai:
                print(" S ", end="")
            elif pos_saat_ini == tujuan:
                print(" G ", end="")
            elif pos_saat_ini in jalur_set:
                print(" * ", end="")
            elif peta[r][c] == 1:
                print(" # ", end="")
            else:
                print(" . ", end="")
        print()

def dapatkan_input_koordinat(baris_maks, kolom_maks, nama_posisi):
    while True:
        try:
            input_pengguna = input(f"Masukkan koordinat {nama_posisi} (baris,kolom, dimulai dari 0): ")
            r, c = map(int, input_pengguna.split(','))
            if 0 <= r < baris_maks and 0 <= c < kolom_maks:
                return (r, c)
            else:
                print(f"Koordinat di luar batas. Baris antara 0-{baris_maks-1}, Kolom antara 0-{kolom_maks-1}.")
        except ValueError:
            print("Input tidak valid. Harap masukkan dua angka dipisahkan koma (contoh: 0,0).")

if __name__ == "__main__":
    peta_gogobus = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    jumlah_baris = len(peta_gogobus)
    jumlah_kolom = len(peta_gogobus[0])

    print("--- SELAMAT DATANG DI NAVIGATOR GOGOBUS ---")
    print("Menggunakan Peta Sederhana (5x5) berikut:")
    for baris_peta in peta_gogobus:
        print(baris_peta)

    posisi_mulai = dapatkan_input_koordinat(jumlah_baris, jumlah_kolom, "MULAI")
    posisi_tujuan = dapatkan_input_koordinat(jumlah_baris, jumlah_kolom, "TUJUAN")

    print(f"\nMencari jalur dari {posisi_mulai} ke {posisi_tujuan}...")
    
    jalur_ditemukan = cari_jalur_bfs_sederhana(peta_gogobus, posisi_mulai, posisi_tujuan)

    if jalur_ditemukan:
        print("\nJalur terpendek GogoBus:")
        for langkah in jalur_ditemukan:
            print(langkah, end=" -> ")
        print("TUJUAN TERCAPAI!")
        tampilkan_peta_dan_jalur(peta_gogobus, jalur_ditemukan, posisi_mulai, posisi_tujuan)
    else:
        print("\nGogoBus tidak dapat mencapai tujuan pada peta ini.")
        tampilkan_peta_dan_jalur(peta_gogobus, None, posisi_mulai, posisi_tujuan)