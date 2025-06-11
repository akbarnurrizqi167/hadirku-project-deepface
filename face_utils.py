import pickle
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
import cv2

# Impor model User dari models.py
from models import User

# --- Konfigurasi ---
EMBEDDING_MODEL_NAME = "SFace"
DETECTOR_BACKEND = "opencv"
SIMILARITY_THRESHOLD = 0.55

def calculate_cosine_similarity(embedding1, embedding2):
    """Menghitung cosine similarity antara dua vector."""
    emb1 = np.array(embedding1, dtype=np.float32).reshape(1, -1)
    emb2 = np.array(embedding2, dtype=np.float32).reshape(1, -1)
    return cosine_similarity(emb1, emb2)[0][0]

def find_best_match_from_db(image_np_array):
    """
    Mendeteksi wajah, lalu mencari kecocokan di database.
    """
    try:
        # 1. Ekstrak embedding dari gambar yang diberikan (dari webcam)
        embedding_objs = DeepFace.represent(
            img_path=image_np_array,
            model_name=EMBEDDING_MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True,
            align=True
        )
        if not embedding_objs:
            return "Unknown", "Tidak ada wajah terdeteksi di kamera."
        
        new_embedding = embedding_objs[0]["embedding"]
        
        # 2. Ambil semua pengguna yang punya data embedding dari database
        users_with_faces = User.query.filter(User.embedding.isnot(None)).all()
        if not users_with_faces:
            return "Unknown", "Tidak ada wajah referensi di database."

        best_match_name = "Unknown"
        highest_sim_score = 0.0

        # 3. Bandingkan embedding baru dengan setiap embedding di database
        for user in users_with_faces:
            # Deserialisasi embedding dari format biner ke list
            stored_embedding = pickle.loads(user.embedding)
            
            similarity = calculate_cosine_similarity(stored_embedding, new_embedding)
            
            if similarity > highest_sim_score:
                highest_sim_score = similarity
                if similarity >= SIMILARITY_THRESHOLD:
                    best_match_name = user.name
        
        if best_match_name != "Unknown":
            return best_match_name, f"Wajah dikenali sebagai {best_match_name}."
        else:
            return "Unknown", "Wajah tidak dikenali."

    except ValueError as e:
        return "Unknown", "Tidak ada wajah terdeteksi."
    except Exception as e:
        print(f"Error di find_best_match_from_db: {e}")
        return "Unknown", "Terjadi kesalahan internal saat pengenalan."

def generate_embedding(image_np_array):
    """Menghasilkan embedding dari sebuah gambar."""
    try:
        embedding_objs = DeepFace.represent(
            img_path=image_np_array,
            model_name=EMBEDDING_MODEL_NAME,
            detector_backend='mtcnn', # Gunakan backend akurat untuk registrasi
            enforce_detection=True,
            align=True
        )
        if embedding_objs:
            return embedding_objs[0]["embedding"]
        else:
            return None
    except Exception:
        return None
