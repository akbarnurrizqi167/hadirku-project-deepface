import os
import base64
from datetime import date, datetime
import numpy as np
import cv2
import pytz
import pickle

from flask import Blueprint, render_template, jsonify, request, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload

from models import AttendanceRecord, MataKuliah, User, db
from face_utils import find_best_match_from_db, generate_embedding

main = Blueprint('main', __name__)

# --- INI ADALAH RUTE UTAMA / DISPATCHER ---
@main.route('/')
@login_required
def index():
    """
    Halaman ini adalah titik masuk utama setelah login.
    - Mengarahkan admin ke dashboard admin.
    - Menampilkan halaman presensi untuk mahasiswa.
    """
    if current_user.is_admin:
        # Jika admin, kirim ke dashboard admin
        return redirect(url_for('admin.index'))
    else:
        # Untuk mahasiswa, periksa apakah mereka sudah mendaftarkan wajah.
        if current_user.embedding is None:
            flash('Anda belum mendaftarkan wajah. Silakan selesaikan pendaftaran.', 'warning')
            return redirect(url_for('main.register_face'))
        
        # Jika sudah, tampilkan halaman presensi
        courses = MataKuliah.query.order_by(MataKuliah.nama_mk).all()
        return render_template('index.html', name=current_user.name, courses=courses)

@main.route('/records')
@login_required
def records():
    if current_user.is_admin:
        flash("Gunakan panel admin untuk melihat semua riwayat presensi.", "info")
        return redirect(url_for('admin.index'))

    wib = pytz.timezone('Asia/Jakarta')
    user_records = AttendanceRecord.query.options(
        joinedload(AttendanceRecord.matakuliah)
    ).filter_by(user_id=current_user.id).order_by(AttendanceRecord.timestamp.desc()).all()

    for record in user_records:
        record.local_time = record.timestamp.replace(tzinfo=pytz.utc).astimezone(wib)
        
    return render_template('records.html', records=user_records, name=current_user.name)

@main.route('/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    data = request.get_json()
    if not all(k in data for k in ['image_data', 'location', 'matakuliah_id']):
        return jsonify({'status': 'error', 'message': 'Permintaan tidak lengkap.'}), 400

    matakuliah_id = data['matakuliah_id']
    location_data = data['location']
    
    today = date.today()
    existing_record_today = AttendanceRecord.query.filter(
        AttendanceRecord.user_id == current_user.id,
        AttendanceRecord.matakuliah_id == matakuliah_id,
        db.func.date(AttendanceRecord.timestamp) == today
    ).first()
    if existing_record_today:
        return jsonify({'status': 'warning', 'message': f'Anda sudah presensi untuk mata kuliah ini hari ini.'})

    try:
        image_data = data['image_data'].split(',')[1]
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None: raise ValueError("Gagal decode gambar")
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Format data gambar tidak valid: {e}'})

    recognized_name, _ = find_best_match_from_db(frame)

    if recognized_name.lower() == current_user.name.lower():
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{current_user.name}_{timestamp_str}.jpg"
        
        full_image_path = os.path.join(current_app.static_folder, 'captures', image_filename)
        cv2.imwrite(full_image_path, frame)
        
        relative_image_path = f"captures/{image_filename}"

        new_record = AttendanceRecord(
            user_id=current_user.id,
            matakuliah_id=matakuliah_id,
            latitude=location_data.get('latitude'),
            longitude=location_data.get('longitude'),
            location=f"Lat: {location_data.get('latitude')}, Lon: {location_data.get('longitude')}",
            image_path=relative_image_path
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Presensi untuk {current_user.name} berhasil!'})
    
    elif recognized_name != "Unknown":
        return jsonify({'status': 'error', 'message': f'Wajah terdeteksi sebagai {recognized_name}, bukan {current_user.name}. Gagal presensi.'})
    else:
        return jsonify({'status': 'error', 'message': 'Wajah tidak dikenali. Pastikan pencahayaan baik dan wajah terlihat jelas.'})

@main.route('/register_face')
@login_required
def register_face():
    if current_user.is_admin:
        flash("Akun admin tidak perlu mendaftarkan wajah.", "info")
        return redirect(url_for('admin.index'))
    return render_template('register_face.html')

@main.route('/save_face', methods=['POST'])
@login_required
def save_face():
    data = request.get_json()
    if not data or 'image_data' not in data:
        return jsonify({'status': 'error', 'message': 'Data gambar tidak ada.'}), 400

    try:
        image_data = data['image_data'].split(',')[1]
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None: raise ValueError("Gagal decode")
    except Exception:
        return jsonify({'status': 'error', 'message': 'Format gambar tidak valid.'})

    embedding_vector = generate_embedding(frame)
    if embedding_vector is None:
        return jsonify({'status': 'error', 'message': 'Tidak dapat mendeteksi wajah dalam foto. Harap coba lagi.'})

    filename = f"{current_user.name}.jpg"
    reference_path = os.path.join('reference_faces', filename)
    cv2.imwrite(reference_path, frame)
    
    user_to_update = User.query.get(current_user.id)
    user_to_update.embedding = pickle.dumps(embedding_vector)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Wajah Anda berhasil didaftarkan!'})
