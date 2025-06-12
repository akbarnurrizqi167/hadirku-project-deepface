from app import create_app, db
from models import MataKuliah
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Hilangkan info, warning, dan error dari TensorFlow

import warnings
warnings.filterwarnings("ignore")         # Hilangkan warning Python biasa

import tensorflow as tf
tf.get_logger().setLevel('ERROR')         # Hilangkan warning logger dari TensorFlow


app = create_app()

with app.app_context():
    # Hapus data lama jika ada
    MataKuliah.query.delete()

    # Data mata kuliah baru
    courses = [
        MataKuliah(kode_mk="S1076", nama_mk="Kecerdasan Bisnis", dosen_pengampu="Yanuar Wicaksono, S.Kom., M.Kom"),
        MataKuliah(kode_mk="SI079", nama_mk="Sistem Pendukung Keputusan", dosen_pengampu="Dadang Heksaputra, S.Kom., M.Kom."),
        MataKuliah(kode_mk="S1081", nama_mk="Manajemen Proyek", dosen_pengampu="Raden Nur Rachman Dzakiyullah, S.Kom., M.Sc."),
        MataKuliah(kode_mk="S1084", nama_mk="Statistika untuk Bisnis ", dosen_pengampu="Asti Ratnasari, S.Kom., M.Kom")
    ]

    db.session.bulk_save_objects(courses)
    db.session.commit()
    print("Database mata kuliah berhasil diisi!")
