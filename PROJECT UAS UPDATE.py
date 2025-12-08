import datetime

def validasi_jadwal(jadwal_str):
    try:
        datetime.datetime.strptime(jadwal_str, "%d-%m-%Y %H:%M")
        return True
    except:
        return False

daftar_history = []

def tambah_history(pesanan):
    daftar_history.append({
        "nama": pesanan.get("nama_customer","-"),
        "tempat": pesanan.get("wisata","-"),
        "waktu_pesan": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
        "jadwal_berangkat": pesanan.get("tanggal_berangkat","-"),
        "jumlah_tiket": pesanan.get("jumlah",0),
        "total_harga": pesanan.get("total",0)
    })

daftar_wisata = [
    {"id": 1, "nama_tempat": "Pantai Sakura", "destinasi": "Snorkeling & Sunset", "lokasi_wisata": "Bali", "harga_tiket": 50000, "kategori_wisata": "alam", "ketersediaan_tiket": 100, "jadwal_berangkat": "08:00"},
    {"id": 2, "nama_tempat": "Bukit Pelangi", "destinasi": "Trekking & Viewpoint", "lokasi_wisata": "Lombok", "harga_tiket": 40000, "kategori_wisata": "alam", "ketersediaan_tiket": 60, "jadwal_berangkat": "07:00"},
    {"id": 3, "nama_tempat": "Museum Angkasa", "destinasi": "Sejarah & Edukasi", "lokasi_wisata": "Jakarta", "harga_tiket": 30000, "kategori_wisata": "budaya", "ketersediaan_tiket": 50, "jadwal_berangkat": "09:00"},
    {"id": 4, "nama_tempat": "Air Adat Nusantara", "destinasi": "Budaya Tradisional", "lokasi_wisata": "Solo", "harga_tiket": 45000, "kategori_wisata": "budaya", "ketersediaan_tiket": 70, "jadwal_berangkat": "10:00"},
    {"id": 5, "nama_tempat": "Kota Kreatif", "destinasi": "Festival & Kuliner", "lokasi_wisata": "Yogyakarta", "harga_tiket": 20000, "kategori_wisata": "modern", "ketersediaan_tiket": 80, "jadwal_berangkat": "11:00"},
    {"id": 6, "nama_tempat": "SkyCity Mall", "destinasi": "Belanja & Hiburan", "lokasi_wisata": "Bandung", "harga_tiket": 25000, "kategori_wisata": "modern", "ketersediaan_tiket": 90, "jadwal_berangkat": "12:00"}
]

daftar_pesanan = []
booking_counter = 1
user_sessions = {}  

auto_restock_enabled = False
auto_restock_threshold = 10
auto_restock_amount = 50

total_pendapatan = 0

def cek_angka(input_user):
    if input_user == "":
        return False
    for karakter in input_user:
        if karakter not in "0123456789":
            return False
    return True

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
    # t1, t2 can be (d,m,y) or (d,m,y,h,min)
    if len(t1) == 3 and len(t2) == 3:
        if t1[2] < t2[2]: return -1
        if t1[2] > t2[2]: return 1
        if t1[1] < t2[1]: return -1
        if t1[1] > t2[1]: return 1
        if t1[0] < t2[0]: return -1
        if t1[0] > t2[0]: return 1
        return 0
    if len(t1) == 5 and len(t2) == 5:
        for i in range(5):
            if t1[i] < t2[i]: return -1
            if t1[i] > t2[i]: return 1
        return 0
    if len(t1) == 3 and len(t2) == 5:
        return banding_tanggal((t1[0], t1[1], t1[2], 0, 0), t2)
    if len(t1) == 5 and len(t2) == 3:
        return banding_tanggal(t1, (t2[0], t2[1], t2[2], 0, 0))
    return 0

def tampilkan_wisata():
    global daftar_wisata
    if auto_restock_enabled:
        for w in daftar_wisata:
            if w.get("ketersediaan_tiket", 0) <= auto_restock_threshold:
                w["ketersediaan_tiket"] += auto_restock_amount
    header = f"{'ID':<3} {'Nama Tempat':<22} {'Lokasi':<12} {'Harga':<10} {'Stok':<6} {'Kategori':<10} {'Jam'}"
    print("=== DAFTAR WISATA ===")
    print(header)
    print("-" * len(header))
    for w in daftar_wisata:
        print(f"{w['id']:<3} {w['nama_tempat']:<22} {w['lokasi_wisata']:<12} Rp{w['harga_tiket']:<8} {w['ketersediaan_tiket']:<6} {w['kategori_wisata']:<10} {w.get('jadwal_berangkat','-')}")
    print("-" * len(header))

def login_user():
    print("=== LOGIN USER ===")
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
        elif len(telp) != 12:
            print("Nomor telepon jumlahnya harus 12 digit.")
        else:
            break

    if telp in user_sessions:
        print("Login berhasil. (sesi ditemukan)")
        return user_sessions[telp]
    
    user = {"email": email, "telepon": telp}
    user_sessions[telp] = user
    print("Login berhasil. Sesi tersimpan.")
    return user

def login_admin():
    pw = input("Masukkan password admin: ")
    if pw == 'admin123':
        print("Login admin berhasil.")
        return True
    print("Password salah.")
    return False

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

def pesan_tiket(user):
    global booking_counter, total_pendapatan
    tampilkan_wisata()

    while True:
        nomor = input("Pilih nomor/ID destinasi: ").strip()
        if not cek_angka(nomor):
            print("Harus angka.")
            continue
        nomor = int(nomor)
        data = next((w for w in daftar_wisata if w['id'] == nomor), None)
        if data is None:
            print("Nomor tidak tersedia.")
            continue
        break

    while True:
        jumlah_orang = input("Jumlah tiket (orang): ").strip()
        if not cek_angka(jumlah_orang):
            print("Harus angka.")
            continue
        jumlah_orang = int(jumlah_orang)
        if jumlah_orang <= 0:
            print("Minimal 1.")
            continue
        if jumlah_orang > data['ketersediaan_tiket']:
            print("Stok tidak cukup. Sisa:", data['ketersediaan_tiket'])
            continue
        break

    while True:
        print("Pilih layanan (1=standard, 2=vip, 3=pelayanan khusus): ")
        layanan = input("Pilihan: ").strip()
        if layanan in ['1','2','3']:
            if layanan == '1': jenis_layanan = 'standard'; persen = 0
            elif layanan == '2': jenis_layanan = 'vip'; persen = 50
            else: jenis_layanan = 'pelayanan_khusus'; persen = 30
            break
        else:
            print("Pilihan tidak valid.")

    while True:
        nama_pemesan = input("Nama pemesan: ").strip()
        if nama_pemesan == '':
            print("Nama tidak boleh kosong.")
        else:
            break

    harga_dasar = data['harga_tiket'] * jumlah_orang
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
            print("1. BCA\n2. BRI\n3. Mandiri\n4. BNI")
            bank = input("Pilih bank (1-4): ")
            if bank == "1": bank_tujuan, norek = "BCA", "1234567890"
            elif bank == "2": bank_tujuan, norek = "BRI", "7766554422"
            elif bank == "3": bank_tujuan, norek = "Mandiri", "9988776655"
            elif bank == "4": bank_tujuan, norek = "BNI", "1133557799"
            else:
                print("Pilihan bank tidak valid, coba lagi."); continue
            print(f"\nBank Tujuan: {bank_tujuan}\nNo Rekening: {norek}")
            while True:
                try: nominal = int(input(f"Masukkan nominal pembayaran Rp{total_bayar}: "))
                except ValueError: print("Nominal harus berupa angka!"); continue
                if nominal < total_bayar: print("Nominal kurang, pembayaran gagal!"); continue
                elif nominal >= total_bayar:
                    print("Pembayaran berhasil!")
                    if nominal > total_bayar: print(f"Kelebihan bayar: Rp {nominal - total_bayar:,}")
                    break
            break

        elif metode == "2":
            metode_pembayaran = "E-Wallet"
            print("1. Dana\n2. OVO\n3. GoPay")
            ewallet = input("Pilih (1-3): ")
            if ewallet == "1": akun, nomor_akun = "DANA","081234567890"
            elif ewallet == "2": akun, nomor_akun = "OVO","085612345678"
            elif ewallet == "3": akun, nomor_akun = "GOPAY","089912345678"
            else: print("Pilihan tidak valid."); continue
            print(f"Silakan transfer ke {akun}\nNomor: {nomor_akun}")
            while True:
                try: nominal = int(input(f"Masukkan nominal pembayaran Rp{total_bayar}: "))
                except ValueError: print("Nominal harus berupa angka!"); continue
                if nominal < total_bayar: print("Nominal kurang, pembayaran gagal!"); continue
                elif nominal >= total_bayar:
                    print("Pembayaran berhasil!")
                    if nominal > total_bayar: print(f"Kelebihan bayar: Rp {nominal - total_bayar:,}")
                    break
            break
        else:
            print("Pilihan tidak valid. Masukkan 1 atau 2.")

    print("\nPilih tanggal keberangkatan:")
    print("1) Pilih tanggal sendiri")
    print("2) Gunakan default (10 hari dari sekarang)")

    while True:
        tpil = input("Pilihan (1/2): ").strip()
        if tpil not in ['1', '2']:
            print("Pilihan tidak valid! Masukkan 1 atau 2.")
            continue

        if tpil == "1":
            while True:
                tgl_input = input("Masukkan tanggal (DD-MM-YYYY): ").strip()
                tgl_parsed = parse_tanggal(tgl_input)
                if tgl_parsed is None:
                    print("Format tanggal salah atau tanggal tidak valid! Coba lagi.")
                    continue
                try:
                    jam_default = data.get("jadwal_berangkat", "08:00")
                    tanggal_berangkat_dt = datetime.datetime(
                        tgl_parsed[2], tgl_parsed[1], tgl_parsed[0],
                        int(jam_default.split(":")[0]),
                        int(jam_default.split(":")[1])
                    )
                    break 
                except ValueError:
                    print("Tanggal atau jam tidak valid! Coba lagi.")
            break 

        else:
            sekarang = datetime.datetime.now()
            tanggal_default = sekarang + datetime.timedelta(days=10)
            jam_default = data.get("jadwal_berangkat", "08:00")
            tanggal_berangkat_dt = datetime.datetime(
                tanggal_default.year, tanggal_default.month, tanggal_default.day,
                int(jam_default.split(":")[0]),
                int(jam_default.split(":")[1])
            )
            break

    tanggal_berangkat_text = tanggal_berangkat_dt.strftime("%d-%m-%Y %H:%M")
    parsed_berangkat = (tanggal_berangkat_dt.day, tanggal_berangkat_dt.month, tanggal_berangkat_dt.year,
                        tanggal_berangkat_dt.hour, tanggal_berangkat_dt.minute)
    id_pesanan = "BK" + str(booking_counter).zfill(5)
    booking_counter += 1

    pesanan = {
        "id_pesanan": id_pesanan,
        "nama_customer": nama_pemesan,
        "email": user.get("email","-"),
        "telepon": user.get("telepon","-"),
        "wisata": data["nama_tempat"],
        "destinasi": data.get("destinasi","-"),
        "lokasi": data.get("lokasi_wisata","-"),
        "kategori": data.get("kategori_wisata","-"),
        "jumlah": jumlah_orang,
        "layanan": jenis_layanan,
        "total": total_bayar,
        "metode": metode_pembayaran,
        "tanggal_pesan": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
        "tanggal_berangkat": tanggal_berangkat_text,
        "parsed_berangkat": parsed_berangkat,
        "data_wisata": data,
        "status": "terbayar",
        "kontak_wisata": data.get("kontak", {"nama":"-","telepon":"-"}),
        "arah_wisata": data.get("arah","-")
    }

    daftar_pesanan.append(pesanan)
    tambah_history(pesanan)
    total_pendapatan += total_bayar
    data["ketersediaan_tiket"] -= jumlah_orang

    print("\nTiket berhasil dibuat.")
    print("ID:", pesanan["id_pesanan"])
    print("Tgl Berangkat:", tanggal_berangkat_text)

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

def lihat_semua_pesanan():
    if len(daftar_pesanan) == 0:
        print('=== DAFTAR PESANAN ===')
        print('Belum ada pesanan.')
        return

    sekarang = datetime.datetime.now()
    sekarang_tuple = (sekarang.day, sekarang.month, sekarang.year, sekarang.hour, sekarang.minute)

    for p in daftar_pesanan:
        if p.get('parsed_berangkat') and banding_tanggal(p['parsed_berangkat'], sekarang_tuple) < 0:
            p['status'] = 'hangus'

    def sort_key(p):
        if p.get('parsed_berangkat'):
            return p['parsed_berangkat']
        return (9999,99,99,99,99)

    ps = sorted(daftar_pesanan, key=sort_key)

    print('=== DAFTAR PESANAN ===')
    for p in ps:
        print('-----------------------------------------')
        print(f"ID        : {p['id_pesanan']}")
        print(f"Nama      : {p['nama_customer']}")
        print(f"Wisata    : {p['wisata']}")
        print(f"Jumlah    : {p['jumlah']}")
        print(f"Layanan   : {p['layanan']}")
        print(f"Total     : Rp{p['total']}")
        print(f"Berangkat : {p.get('tanggal_berangkat','-')}")
        print(f"Status    : {p['status']}")
    print('-----------------------------------------')

def cetak_tiket():
    if len(daftar_pesanan) == 0:
        print('Belum ada pesanan.')
        return
    print('Daftar ID Pesanan:')
    for p in daftar_pesanan:
        print('-', p['id_pesanan'])
    kode = input('Masukkan ID Pesanan: ').upper()
    ada = next((p for p in daftar_pesanan if p['id_pesanan'] == kode), None)
    if not ada:
        print('ID tidak ditemukan.')
        return

    print('+----------------------+-------------------------------+')
    print(f"| ID Pesanan           | {ada['id_pesanan']:<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Nama Pemesan         | {ada['nama_customer']:<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Wisata               | {ada['wisata']:<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Destinasi            | {ada.get('destinasi',''):<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Lokasi               | {ada.get('lokasi',''):<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Jumlah               | {ada['jumlah']:<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Layanan              | {ada['layanan']:<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Total                | Rp {ada['total']:<25} |")
    print('+----------------------+-------------------------------+')
    print(f"| Metode Pembayaran    | {ada.get('metode',''):<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Tgl Pesan            | {ada.get('tanggal_pesan',''):<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Tgl Berangkat        | {ada.get('tanggal_berangkat','-'):<29} |")
    print('+----------------------+-------------------------------+')
    print(f"| Status               | {ada['status']:<29} |")
    print('+----------------------+-------------------------------+')

    
    while True:
        pilihan = input('Mau langsung verifikasi keberangkatan sekarang? (y/n): ').strip().lower()

        if pilihan in ['y', 'n']:
           break
        else:
           print('Input tidak valid! Masukkan hanya y atau n.')

    if pilihan == 'y':
        verifikasi_keberangkatan()
    else:
        print('Kembali ke menu utama.')

def verifikasi_keberangkatan():
    if len(daftar_pesanan) == 0:
        print('Belum ada pesanan.')
        return
    idp = input('Masukkan ID Pesanan untuk verifikasi: ').upper()
    p = next((x for x in daftar_pesanan if x['id_pesanan'] == idp), None)
    if not p:
        print('Pesanan tidak ditemukan!')
        return

    p['status'] = 'Sudah Berangkat'
    print('Status diperbarui menjadi: Sudah Berangkat')

def tambah_stok_otomatis():
    try:
        idw = int(input('Masukkan ID wisata: ').upper())
        w = next((x for x in daftar_wisata if x['id'] == idw), None)
        if not w:
            print('Wisata tidak ditemukan!')
            return
        tambah = int(input('Tambah stok: ').strip())
        w['ketersediaan_tiket'] += tambah
        print('Stok berhasil diperbarui. Stok sekarang:', w['ketersediaan_tiket'])
    except Exception as e:
        print('Input tidak valid.', e)

def admin_set_auto_restock():
    global auto_restock_enabled, auto_restock_threshold, auto_restock_amount
    pilihan = input('Aktifkan auto-restock? (y/n): ').strip().lower()
    if pilihan == 'y':
        try:
            auto_restock_threshold = int(input('Threshold stok (mis. 10): ').strip())
            auto_restock_amount = int(input('Jumlah restock saat threshold tercapai (mis. 50): ').strip())
            auto_restock_enabled = True
            print('Auto-restock diaktifkan.')
        except:
            print('Input tidak valid, pengaturan dibatalkan.')
    else:
        auto_restock_enabled = False
        print('Auto-restock dinonaktifkan.')

def statistik():
    print('===== STATISTIK SISTEM =====')
    print(f"Total Pesanan: {len(daftar_pesanan)}")
    total = sum(p.get('total',0) for p in daftar_pesanan)
    print(f"Pendapatan: Rp {total}")

def tampilkan_history_tabel():
    if not daftar_history:
        print("Belum ada history pemesanan.")
        return
    header = f"{'No':<3} {'Nama':<20} {'Tempat':<20} {'Waktu Pesan':<17} {'Jadwal':<17} {'Qty':<4} {'Total':<10}"
    print("=== HISTORY PEMESANAN ===")
    print(header)
    print("-" * len(header))
    for i, h in enumerate(daftar_history, start=1):
        print(f"{i:<3} {h['nama']:<20} {h['tempat']:<20} {h['waktu_pesan']:<17} {h['jadwal_berangkat']:<17} {h['jumlah_tiket']:<4} Rp{h['total_harga']:<9}")
    print("-" * len(header))

def menu_user(user):
    while True:
        print('=== MENU USER ===')
        print("1. Lihat Semua Wisata")
        print("2. Cari Wisata Berdasarkan Kategori")
        print("3. Sorting Wisata")
        print("4. Pesan Tiket")
        print("5. Lihat Pesanan")
        print("6. Cetak Tiket")
        print("7. Verifikasi Keberangkatan")
        print("8. Statistik Sistem")
        print('9. Lihat History Pesanan')
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
            pesan_tiket(user)
        elif menu == "5":
            user_pes = [p for p in daftar_pesanan if p.get('telepon') == user.get('telepon')]
            if not user_pes:
                print('Belum ada pesanan untuk akun ini.')
            else:
                for p in user_pes:
                    print('-----------------------------------------')
                    print(f"ID: {p['id_pesanan']} | Wisata: {p['wisata']} | Jumlah: {p['jumlah']} | Berangkat: {p.get('tanggal_berangkat','-')} | Status: {p['status']}")
                print('-----------------------------------------')
        elif menu == "6":
            cetak_tiket()
        elif menu == "7":
            verifikasi_keberangkatan()
        elif menu == "8":
            tampilkan_history_tabel()
        elif menu == "9":
            batalkan_pesanan()
        elif menu == "10":
            print("Program selesai.")
            break
        else:
            print("Menu tidak valid.")
            user_pes = [p for p in daftar_pesanan if p.get('telepon') == user.get('telepon')]
            if not user_pes:
                print('Belum ada pesanan untuk akun ini.')
            else:
                for p in user_pes:
                    print('-----------------------------------------')
                    print(f"ID: {p['id_pesanan']} | Wisata: {p['wisata']} | Jumlah: {p['jumlah']} | Berangkat: {p.get('tanggal_berangkat','-')} | Status: {p['status']}")
                print('-----------------------------------------')
        
def menu_admin():
    while True:
        print('=== MENU ADMIN ===')
        print('1. Tambah Stok Manual')
        print('2. Pengaturan Auto-Restock')
        print('3. Lihat Semua Pesanan')
        print('4. Verifikasi Keberangkatan')
        print('5. Statistik')
        print('0. Logout')
        pilih = input('Pilih: ').strip()
        if pilih == '1': tambah_stok_otomatis()
        elif pilih == '2': admin_set_auto_restock()
        elif pilih == '3': lihat_semua_pesanan()
        elif pilih == '4': verifikasi_keberangkatan()
        elif pilih == '5': statistik()
        elif pilih == '0': break
        else: print('Pilihan tidak valid!')

def login_dan_menu():
    while True:
        print('=== SISTEM PARIWISATA ===')
        print('1. Login Admin')
        print('2. Login User')
        print('0. Keluar')
        pilih = input('Pilih: ').strip()
        if pilih == '1':
            if login_admin(): menu_admin()
        elif pilih == '2':
            user = login_user()
            if user: menu_user(user)
        elif pilih == '0':
            print('Keluar dari program.')
            break
        else:
            print('Pilihan tidak valid.')

if __name__ == '__main__':
    login_dan_menu()

