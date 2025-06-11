# 🎓 Hadirku — Sistem Presensi Mahasiswa Berbasis Face Recognition

**Hadirku** adalah sistem presensi cerdas berbasis pengenalan wajah (face recognition) yang dirancang untuk lingkungan akademik. Dengan teknologi ini, proses presensi menjadi lebih cepat, akurat, dan aman menggantikan metode konvensional yang rawan manipulasi dan ketidakefisienan.

---

## 💡 Filosofi Proyek

Absensi manual sering kali menghadapi kendala seperti pemalsuan kehadiran, antrian panjang, dan rekap data yang memakan waktu. Hadirku memanfaatkan **AI untuk deteksi wajah** sebagai identitas presensi digital, sekaligus menyediakan **dashboard manajemen** untuk admin dan kemudahan akses bagi mahasiswa.

---

## ⚙️ Teknologi yang Digunakan

| Komponen     | Teknologi                              |
|--------------|----------------------------------------|
| Backend      | Flask (Python)                         |
| Database     | SQLAlchemy (SQLite/MySQL)              |
| Frontend     | HTML, CSS, JavaScript                  |
| Face Recognition | DeepFace, OpenCV, SFace, MTCNN     |
| Embedding    | Pickle (serialisasi data wajah)        |

---

## ✨ Fitur Aplikasi

### 👨‍🎓 Mahasiswa (User)
- **Signup** dengan nama lengkap dan NIM (sebagai password awal).
- **Registrasi wajah** langsung melalui webcam.
- **Presensi otomatis** berbasis kecocokan wajah.
- **Pemilihan kelas** saat melakukan presensi.
- **Riwayat presensi** meliputi:
  - Tanggal dan waktu
  - Kelas yang dihadiri
  - Lokasi presensi
  - Bukti foto hasil presensi
- **Logout** untuk mengakhiri sesi dengan aman.

### 🧑‍💼 Admin
- **Login sebagai admin** (melalui script setup awal).
- **Dashboard admin** untuk:
  - Melihat dan mengelola data presensi
  - Mengelola data kelas dan matakuliah
  - Melakukan analisis dan monitoring kehadiran
- **Logout** untuk keluar dari sistem.


## 🧠 Teknologi Face Recognition

Sistem menggunakan DeepFace dan model `SFace` untuk menghasilkan *embedding wajah*, lalu membandingkannya menggunakan **cosine similarity**:

Prosesnya:

1. Tangkap wajah dari webcam.
2. Hasilkan *embedding* dengan DeepFace.
3. Bandingkan dengan database menggunakan cosine similarity.
4. Validasi kehadiran jika skor di atas ambang batas.

---

## 🚀 Cara Menjalankan Hadirku di Komputer Lokal

Ikuti langkah-langkah berikut di terminal atau command prompt:

### 1. Clone Repository

```bash
git clone https://github.com/akbarnurrizqi167/hadirku-project.git
```
```bash
cd hadirku-project
```

### 2. Aktifkan Virtual Environment (Opsional, tapi Disarankan)

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Buat Akun Admin

```bash
python create_admin.py
```
"Ikuti prompt untuk memasukkan username dan password admin"

### 5. Inisialisasi Database

```bash
python seed_db.py
```

### 6. Jalankan Aplikasi

```bash
flask run
```

Akses aplikasi di browser:
📍 `http://localhost:5000`

---

## 📁 Struktur Direktori (Singkat)

```
hadirku-project/
│
├── app/
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JS, image
│   ├── models.py        # Struktur tabel database
│   ├── routes.py        # Routing endpoint
│   ├── face_utils.py    # Fungsi face recognition
│   └── __init__.py      # Setup Flask app
│
├── create_admin.py      # Setup akun admin awal
├── seed_db.py           # Setup awal database
├── requirements.txt     # Dependency
├── README.md            # Dokumentasi ini
└── ...
```

---

## 🔒 Catatan Keamanan

* Gunakan password yang kuat saat membuat akun admin.
* Pastikan kamera aktif saat registrasi wajah dan presensi.
* Disarankan dijalankan di lingkungan jaringan lokal untuk pengujian.

---

## 🤝 Kontribusi

Kami terbuka untuk kolaborasi dan kontribusi dari siapa saja!
Bantu kami mengembangkan Hadirku menjadi sistem presensi berbasis AI yang lebih kuat dan inklusif.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

## 📬 Kontak Pengembang

**Akbar Nur Rizqi**
📧 [akbarnurrizqi167@gmail.com](mailto:akbarnurrizqi167@gmail.com)
🌐 GitHub: [github.com/akbarnurrizqi167](https://github.com/akbarnurrizqi167)

---

> “Presensi bukan hanya soal hadir, tapi bagaimana kita diakui dengan cerdas.”

```
