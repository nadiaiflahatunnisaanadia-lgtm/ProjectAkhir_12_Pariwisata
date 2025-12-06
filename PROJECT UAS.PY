import datetime

daftar_wisata = [
    {"nama_tempat": "Pantai Sakura", "destinasi": "Snorkeling & Sunset", "lokasi_wisata": "Bali", "harga_tiket": 50000, "kategori_wisata": "alam", "ketersediaan_tiket": 100},
    {"nama_tempat": "Bukit Pelangi", "destinasi": "Trekking & Viewpoint", "lokasi_wisata": "Lombok", "harga_tiket": 40000, "kategori_wisata": "alam", "ketersediaan_tiket": 60},
    {"nama_tempat": "Museum Angkasa", "destinasi": "Sejarah & Edukasi", "lokasi_wisata": "Jakarta", "harga_tiket": 30000, "kategori_wisata": "budaya", "ketersediaan_tiket": 50},
    {"nama_tempat": "Air Adat Nusantara", "destinasi": "Budaya Tradisional", "lokasi_wisata": "Solo", "harga_tiket": 45000, "kategori_wisata": "budaya", "ketersediaan_tiket": 70},
    {"nama_tempat": "Kota Kreatif", "destinasi": "Festival & Kuliner", "lokasi_wisata": "Yogyakarta", "harga_tiket": 20000, "kategori_wisata": "modern", "ketersediaan_tiket": 80},
    {"nama_tempat": "SkyCity Mall", "destinasi": "Belanja & Hiburan", "lokasi_wisata": "Bandung", "harga_tiket": 25000, "kategori_wisata": "modern", "ketersediaan_tiket": 90}
]

daftar_pesanan = []
booking_ids = []
booking_counter = 1
total_pendapatan = 0

def cek_angka(input_user):
    if input_user == "":
        return False
    for karakter in input_user:
        if karakter not in "0123456789":
            return False
    return True

def input_angka(teks):
    while True:
        input_user = input(teks)
        if input_user == "":
            print("Input tidak boleh kosong.")
        else:
            if cek_angka(input_user):
                return int(input_user)
            else:
                print("Input harus berupa angka.")

def parse_tanggal(teks):
    if len(teks) != 10:
        return None
    if teks[2] != "-" or teks[5] != "-":
        return None
    hari_str = teks[0:2]
    bulan_str = teks[3:5]
    tahun_str = teks[6:10]
    if not (cek_angka(hari_str) and cek_angka(bulan_str) and cek_angka(tahun_str)):
        return None
    hari = int(hari_str)
    bulan = int(bulan_str)
    tahun = int(tahun_str)
    if tahun < 1900 or bulan < 1 or bulan > 12 or hari < 1 or hari > 31:
        return None
    if bulan in [4, 6, 9, 11] and hari > 30:
        return None
    if bulan == 2 and hari > 29:
        return None
    return (hari, bulan, tahun)

def parse_tanggal_waktu(teks):
    if len(teks) != 16:
        return None
    if teks[2] != "-" or teks[5] != "-" or teks[10] != " " or teks[13] != ":":
        return None
    tanggal_part = teks[0:10]
    jam_part = teks[11:16]
    tanggal_parsed = parse_tanggal(tanggal_part)
    if tanggal_parsed is None:
        return None
    hh = jam_part[0:2]
    mm = jam_part[3:5]
    if not (cek_angka(hh) and cek_angka(mm)):
        return None
    hour = int(hh)
    minute = int(mm)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None
    return (tanggal_parsed[0], tanggal_parsed[1], tanggal_parsed[2], hour, minute)

def banding_tanggal(t1, t2):
    if len(t1) == 3 and len(t2) == 3:
        if t1[2] < t2[2]:
            return -1
        if t1[2] > t2[2]:
            return 1
        if t1[1] < t2[1]:
            return -1
        if t1[1] > t2[1]:
            return 1
        if t1[0] < t2[0]:
            return -1
        if t1[0] > t2[0]:
            return 1
        return 0
    if len(t1) == 5 and len(t2) == 5:
        if t1[2] < t2[2]:
            return -1
        if t1[2] > t2[2]:
            return 1
        if t1[1] < t2[1]:
            return -1
        if t1[1] > t2[1]:
            return 1
        if t1[0] < t2[0]:
            return -1
        if t1[0] > t2[0]:
            return 1
        if t1[3] < t2[3]:
            return -1
        if t1[3] > t2[3]:
            return 1
        if t1[4] < t2[4]:
            return -1
        if t1[4] > t2[4]:
            return 1
        return 0
    if len(t1) == 3 and len(t2) == 5:
        return banding_tanggal((t1[0], t1[1], t1[2], 0, 0), t2)
    if len(t1) == 5 and len(t2) == 3:
        return banding_tanggal(t1, (t2[0], t2[1], t2[2], 0, 0))
    return 0

def input_tanggal(teks):
    while True:
        input_user = input(teks)
        hasil = parse_tanggal(input_user)
        if hasil is None:
            print("Format tanggal harus DD-MM-YYYY dan valid.")
        else:
            return hasil

def tampilkan_wisata():
    print("\n=== DAFTAR WISATA ===")
    nomor = 1
    for wisata in daftar_wisata:
        print(str(nomor) + ". " + wisata["nama_tempat"] + " | " + wisata["destinasi"] + " | " + wisata["lokasi_wisata"] +
              " | Rp" + str(wisata["harga_tiket"]) + " | " + wisata["kategori_wisata"] +
              " | Stok:" + str(wisata["ketersediaan_tiket"]))
        nomor += 1

def sorting_wisata():
    print("\n=== SORTING WISATA ===")
    print("1. 3 Harga Termurah")
    print("2. 3 Harga Termahal")
    print("3. 3 Stok Tersedikit")
    print("4. 3 Stok Terbanyak")
    pilihan = input("Pilih sorting: ")
    data_sorted = daftar_wisata.copy()
    if pilihan == "1":
        data_sorted.sort(key=lambda x: x["harga_tiket"])
    elif pilihan == "2":
        data_sorted.sort(key=lambda x: x["harga_tiket"], reverse=True)
    elif pilihan == "3":
        data_sorted.sort(key=lambda x: x["ketersediaan_tiket"])
    elif pilihan == "4":
        data_sorted.sort(key=lambda x: x["ketersediaan_tiket"], reverse=True)
    else:
        print("Pilihan tidak valid.")
        return
    print("\n=== HASIL SORTING (3 TERATAS) ===")
    index = 1
    for wisata in data_sorted[:3]:
        print(f"{index}. {wisata['nama_tempat']} | Harga: {wisata['harga_tiket']} | Stok: {wisata['ketersediaan_tiket']}")
        index += 1

def cari_kategori():
    if len(daftar_wisata) == 0:
        print("Belum ada wisata.")
        return
    tampilkan_wisata()
    while True:
        kategori = input("Masukkan kategori (alam/budaya/modern): ")
        if kategori not in ["alam", "budaya", "modern"]:
            print("Kategori tidak valid.")
        else:
            break
    print("\nHasil pencarian kategori:", kategori)
    nomor = 1
    ada = False
    for wisata in daftar_wisata:
        if wisata["kategori_wisata"] == kategori:
            ada = True
            print(str(nomor) + ". " + wisata["nama_tempat"] + " | " + wisata["destinasi"] + " | " + wisata["lokasi_wisata"] +
                  " | Rp" + str(wisata["harga_tiket"]) + " | Stok:" + str(wisata["ketersediaan_tiket"]))
        nomor += 1
    if not ada:
        print("Tidak ada wisata di kategori tersebut.")

def pesan_tiket(tanggal_hari_ini):
    global booking_counter, total_pendapatan
    tampilkan_wisata()
    while True:
        nomor_wisata = input("Pilih nomor destinasi: ")
        if cek_angka(nomor_wisata):
            nomor_wisata = int(nomor_wisata)
            if 1 <= nomor_wisata <= len(daftar_wisata):
                break
            else:
                print("Nomor tidak tersedia.")
        else:
            print("Harus angka.")
    data = daftar_wisata[nomor_wisata - 1]

    while True:
        jumlah_orang = input("Jumlah tiket (orang): ")
        if cek_angka(jumlah_orang):
            jumlah_orang = int(jumlah_orang)
            if jumlah_orang > 0:
                if jumlah_orang <= data["ketersediaan_tiket"]:
                    break
                else:
                    print("Stok tidak cukup. Sisa:", data["ketersediaan_tiket"])
            else:
                print("Minimal 1.")
        else:
            print("Harus angka.")

    while True:
        layanan = input("Pilih layanan (1=standard, 2=vip, 3=pelayanan khusus): ")
        if layanan in ["1", "2", "3"]:
            if layanan == "1":
                jenis_layanan = "standard"
                persen = 0
            elif layanan == "2":
                jenis_layanan = "vip"
                persen = 50
            else:
                jenis_layanan = "pelayanan_khusus"
                persen = 30
            break
        else:
            print("Pilihan tidak valid.")

    while True:
        nama_pemesan = input("Nama pemesan: ")
        if nama_pemesan == "":
            print("Nama tidak boleh kosong.")
        else:
            break

    while True:
        email = input("Email: ")
        if email == "":
            print("Email tidak boleh kosong.")
        elif "@" not in email or "." not in email:
            print("Format email tidak valid.")
        else:
            break

    while True:
        telp = input("Nomor Telepon: ")
        if telp == "":
            print("Nomor telepon tidak boleh kosong.")
        elif not cek_angka(telp):
            print("Nomor telepon harus angka.")
        elif len(telp) < 9:
            print("Nomor telepon terlalu pendek.")
        else:
            break

    harga_dasar = data["harga_tiket"] * jumlah_orang
    tambahan = (harga_dasar * persen) // 100
    total_bayar = harga_dasar + tambahan

    print("Total bayar: Rp", total_bayar)

    while True:
        print("\n=== METODE PEMBAYARAN ===")
        print("1. Transfer Bank")
        print("2. E-Wallet")
        metode = input("Pilih metode (1/2): ")

        if metode == "1":
            metode_pembayaran = "Transfer Bank"
            print("\nPilih Bank:")
            print("1. BCA")
            print("2. BRI")
            print("3. Mandiri")
            print("4. BNI")
        
            bank = input("Pilih bank (1-4): ")

            if bank == "1":
                bank_tujuan = "BCA"
                norek = "1234567890"
            elif bank == "2":
                bank_tujuan = "BRI"
                norek = "7766554422"
            elif bank == "3":
                bank_tujuan = "Mandiri"
                norek = "9988776655"
            elif bank == "4":
                bank_tujuan = "BNI"
                norek = "1133557799"
            else:
                print("Pilihan bank tidak valid, coba lagi.")
                continue

            print(f"\n=== INFORMASI PEMBAYARAN ===")
            print(f"Bank Tujuan : {bank_tujuan}")
            print(f"No Rekening : {norek}")

            while True:
                try:
                    nominal = int(input(f"Masukkan nominal pembayaran Rp{total_bayar}: "))
                    break
                except ValueError:
                    print("Nominal harus berupa angka!")

            if nominal < total_bayar:
               print("\n Nominal kurang, pembayaran gagal!")
               continue
            elif nominal == total_bayar:
                print("\n Pembayaran berhasil! Terima kasih.")
            else:
                print("\n Pembayaran berhasil!")
                print(f"Kelebihan bayar: Rp {nominal - total_bayar:,}")

            break
        elif metode == "2":
            metode_pembayaran = "E-Wallet"
            print("\nPilih E-Wallet:")
            print("1. Dana")
            print("2. OVO")
            print("3. GoPay")

            ewallet = input("Pilih (1-3): ")

            if ewallet == "1":
               akun = "DANA"
               nomor = "081234567890"
            elif ewallet == "2":
                akun = "OVO"
                nomor = "085612345678"
            elif ewallet == "3":
                akun = "GOPAY"
                nomor = "089912345678"
            else:
                print("Pilihan tidak valid.")
                continue

            print(f"\nSilakan transfer ke {akun}")
            print(f"Nomor: {nomor}")
            
            while True:
                try:
                    nominal = int(input(f"Masukkan nominal pembayaran Rp{total_bayar}: "))
                    break
                except ValueError:
                    print("Nominal harus berupa angka!")

            if nominal < total_bayar:
               print("\n Nominal kurang, pembayaran gagal!")
               continue
            elif nominal == total_bayar:
                print("\n Pembayaran berhasil! Terima kasih.")
            else:
                print("\n Pembayaran berhasil!")
                print(f"Kelebihan bayar: Rp {nominal - total_bayar:,}")
            break
        else:
            print("Pilihan tidak valid. Masukkan 1 atau 2.")

    nomor_pesan = booking_counter
    while nomor_pesan in booking_ids:
        nomor_pesan += 1
    booking_ids.append(nomor_pesan)
    booking_counter += 1

    tanggal_pesan_text = f"{tanggal_hari_ini[0]:02d}-{tanggal_hari_ini[1]:02d}-{tanggal_hari_ini[2]}"
    pesanan = {
        "id_pesanan": "bk" + str(nomor_pesan).zfill(5),
        "nama_customer": nama_pemesan,
        "email": email,
        "telepon": telp,
        "wisata": data["nama_tempat"],
        "destinasi": data["destinasi"],
        "lokasi": data["lokasi_wisata"],
        "kategori": data["kategori_wisata"],
        "jumlah": jumlah_orang,
        "layanan": jenis_layanan,
        "total": total_bayar,
        "metode": metode_pembayaran,
        "tanggal_pesan": tanggal_pesan_text,
        "data_wisata": data,
        "status": "terbayar"
    }
    daftar_pesanan.append(pesanan)
    total_pendapatan += total_bayar
    data["ketersediaan_tiket"] -= jumlah_orang

    print("Tiket berhasil dibuat.")
    print("ID:", pesanan["id_pesanan"])

def lihat_pesanan(waktu_sekarang_dt):
    if len(daftar_pesanan) == 0:
        print("Belum ada pesanan.")
        return
    sekarang_tuple = (waktu_sekarang_dt.day, waktu_sekarang_dt.month, waktu_sekarang_dt.year, waktu_sekarang_dt.hour, waktu_sekarang_dt.minute)
    for p in daftar_pesanan:
        if "parsed_berangkat" in p and banding_tanggal(p["parsed_berangkat"], sekarang_tuple) < 0:
            p["status"] = "hangus"
    nomor = 1
    print("\n=== DAFTAR PESANAN ===")
    for p in daftar_pesanan:
        tanggal_berangkat = p.get("tanggal_berangkat", "-")
        print(str(nomor) + ". ID:" + p["id_pesanan"] + " | " + p["nama_customer"] + " | " +
              p["wisata"] + " | " + str(p["jumlah"]) + " org | Layanan:" + p["layanan"] +
              " | Total:Rp" + str(p["total"]) + " | Berangkat:" +
              tanggal_berangkat + " | Status:" + p["status"])
        nomor += 1

def cetak_tiket():
    if len(daftar_pesanan) == 0:
        print("Belum ada pesanan.")
        return
    print("\nDaftar ID Pesanan:")
    for p in daftar_pesanan:
        print("-", p["id_pesanan"])
    kode = input("Masukkan ID Pesanan: ")
    ada = None
    for p in daftar_pesanan:
        if p["id_pesanan"] == kode:
            ada = p
            break
    if ada is None:
        print("ID tidak ditemukan.")
        return
    
    sekarang = datetime.datetime.now()
    tanggal_sistem = sekarang
    tanggal_resmi = tanggal_sistem + datetime.timedelta(days=10)
    tanggal_resmi_text = tanggal_resmi.strftime("%d-%m-%Y %H:%M")
    parsed_resmi = (
        tanggal_resmi.day,
        tanggal_resmi.month,
        tanggal_resmi.year,
        tanggal_resmi.hour,
        tanggal_resmi.minute
    )
    ada["tanggal_berangkat"] = tanggal_resmi_text
    ada["parsed_berangkat"] = parsed_resmi

    print("\n+----------------------+-------------------------------+")
    print(f"| ID Pesanan           | {ada['id_pesanan']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Nama Pemesan         | {ada['nama_customer']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Wisata               | {ada['wisata']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Destinasi            | {ada['destinasi']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Lokasi               | {ada['lokasi']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Kategori             | {ada['kategori']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Jumlah               | {ada['jumlah']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Layanan              | {ada['layanan']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Total                | Rp {ada['total']:<25} |")
    print("+----------------------+-------------------------------+")
    print(f"| Metode Pembayaran    | {ada['metode']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Tgl Pesan            | {ada['tanggal_pesan']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Tgl Berangkat        | {ada['tanggal_berangkat']:<29} |")
    print("+----------------------+-------------------------------+")
    print(f"| Status               | {ada['status']:<29} |")
    print("+----------------------+-------------------------------+")

def filter_pesanan_nama():
    if len(daftar_pesanan) == 0:
        print("Belum ada pesanan.")
        return
    print("\nDaftar nama pemesan yang ada:")
    nama_list = []
    for p in daftar_pesanan:
        if p["nama_customer"] not in nama_list:
            nama_list.append(p["nama_customer"])
    for n in nama_list:
        print("- " + n)
    nama = input("\nMasukkan nama customer: ")
    ketemu = False
    for p in daftar_pesanan:
        if p["nama_customer"] == nama:
            ketemu = True
            tanggal_berangkat = p.get("tanggal_berangkat", "-")
            print(p["id_pesanan"], "|", p["wisata"], "|", tanggal_berangkat, "|", p["status"])
    if not ketemu:
        print("Tidak ada pesanan dengan nama itu.")

def batalkan_pesanan():
    if len(daftar_pesanan) == 0:
        print("Belum ada pesanan.")
        return
    print("\nDaftar ID pesanan tersedia:")
    for p in daftar_pesanan:
        tanggal_berangkat = p.get("tanggal_berangkat", "-")
        print("- " + p["id_pesanan"] + " | " + p["nama_customer"] + " | " + p["wisata"] + " | " + tanggal_berangkat + " | " + p["status"])
    kode = input("Masukkan ID Pesanan yang ingin dibatalkan: ")
    for p in daftar_pesanan:
        if p["id_pesanan"] == kode:
            if p["status"] == "hangus":
                print("Pesanan sudah hangus, tidak dapat dibatalkan.")
                return
            for w in daftar_wisata:
                if w["nama_tempat"] == p["wisata"]:
                    w["ketersediaan_tiket"] += p["jumlah"]
                    break
            p["status"] = "dibatalkan"
            print("Pesanan berhasil dibatalkan dan stok dikembalikan.")
            return
    print("ID Pesanan tidak ditemukan.")

def statistik():
    print("\n=== STATISTIK SISTEM ===")
    print("Total pesanan:", len(daftar_pesanan))
    print("Total pendapatan: Rp", total_pendapatan)

def verifikasi_keberangkatan():
    if len(daftar_pesanan) == 0:
        print("Belum ada pesanan.")
        return

    while True:
        print("\n=== VERIFIKASI KEBERANGKATAN ===")
        valid_ids = [p["id_pesanan"] for p in daftar_pesanan if p["status"] != "dibatalkan"]
        if len(valid_ids) == 0:
            print("Belum ada pesanan yang valid (semua dibatalkan).")
            return

        print("Daftar ID pesanan yang valid:")
        for vid in valid_ids:
            print("-", vid)

        id_pesan = input("Masukkan ID Pesanan: ")

        pesanan = None
        for p in daftar_pesanan:
            if p["id_pesanan"] == id_pesan and p["status"] != "dibatalkan":
                pesanan = p
                break

        if pesanan is None:
            print("Data tidak terdaftar. Silakan coba lagi.")
            continue 

        print("\nData Pesanan:")
        print("ID Pesanan       :", pesanan["id_pesanan"])
        print("Nama Pemesan     :", pesanan["nama_customer"])
        print("Email            :", pesanan["email"])
        print("No Telepon       :", pesanan["telepon"])
        print("Tanggal & Jam Resmi Berangkat :", pesanan.get("tanggal_berangkat", "-"))

        while True:
            input_tgl = input("Masukkan tanggal & jam untuk verifikasi (DD-MM-YYYY HH:MM): ")
            parsed_input = parse_tanggal_waktu(input_tgl)
            if parsed_input is None:
                print("Format salah, gunakan DD-MM-YYYY HH:MM.")
                continue
            if parsed_input < pesanan["parsed_berangkat"]:
                print("jadwal yang anda masukkan belum waktunya berangkat.")
                continue
            elif parsed_input > pesanan["parsed_berangkat"]:
                print("jadwal yang anda masukkan sudah lewat(hangus!).")
                continue
            else:
                print("Jadwal sesuai, tiket valid.")
                break
        break

while True:
    sekarang = datetime.datetime.now()
    tanggal_hari_ini = (sekarang.day, sekarang.month, sekarang.year)
    waktu_sekarang = sekarang
    print("\n=== SISTEM INFORMASI PARIWISATA ===")
    print("1. Lihat Semua Wisata")
    print("2. Cari Wisata Berdasarkan Kategori")
    print("3. Sorting Wisata")
    print("4. Pesan Tiket")
    print("5. Lihat Pesanan")
    print("6. Cetak Tiket")
    print("7. Cari Pesanan Berdasarkan Nama")
    print("8. Verifikasi Keberangkatan")
    print("9. Statistik Sistem")
    print("10. Batalkan Pesanan")
    print("11. Keluar")

    menu = input("Pilih menu: ")
    if menu == "1":
        tampilkan_wisata()
    elif menu == "2":
        cari_kategori()
    elif menu == "3":
        sorting_wisata()
    elif menu == "4":
        pesan_tiket(tanggal_hari_ini)
    elif menu == "5":
        lihat_pesanan(waktu_sekarang)
    elif menu == "6":
        cetak_tiket()
    elif menu == "7":
        filter_pesanan_nama()
    elif menu == "8":
        verifikasi_keberangkatan()
    elif menu == "9":
        statistik()
    elif menu == "10":
        batalkan_pesanan()
    elif menu == "11":
        print("Program selesai.")
        break
    else:
        print("Menu tidak valid.")
