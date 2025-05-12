from flask import Blueprint, request, jsonify
import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.models import load_model

face_detect_bp = Blueprint('face_detect', __name__)


# Xác định đường dẫn tới thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Xây dựng đường dẫn tới model.keras
MODEL_PATH = os.path.join(BASE_DIR, '..', '..', 'model', 'model.keras')
# Tải mô hình
model = load_model(MODEL_PATH)

# Nhãn lớp
class_labels = [
    '21060451_NguyenHungAnh',
    '21073141_LePhuHao',
    '21075071_NguyenHanhBaoAn',
    '21090261_DuongNgocAnh',
    '21094341_ChauTieuLong',
    '21096911_NguyenNhatTung',
    '21105351_TongThanhLoc',
    '21115461_TuanAnhTran',
    '21119631_NguyenMinhLong'
]

# Cascade để phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Hàm xử lý ảnh đầu vào
def extract_face(image_cv2, input_size=(224, 224)):
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return None, "Không tìm thấy khuôn mặt nào."

    # Chọn khuôn mặt đầu tiên
    (x, y, w, h) = faces[0]
    face_img = image_cv2[y:y+h, x:x+w]
    face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    # Resize + chuẩn hóa
    img = Image.fromarray(face_rgb).resize(input_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array, (x, y, w, h), None

@face_detect_bp.route('/api/face-detect', methods=['POST'])
def detect_face():
    if 'image' not in request.files:
        return jsonify({"message": "Không có ảnh trong yêu cầu!"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "Chưa chọn ảnh!"}), 400

    try:
        # Chuyển ảnh sang OpenCV format
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        image_cv2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        img_array, face_coords, error = extract_face(image_cv2)
        if error:
            return jsonify({"message": error}), 400

        # Dự đoán
        predictions = model.predict(img_array)
        confidence = float(np.max(predictions)) * 100
        predicted_index = int(np.argmax(predictions))

        if confidence < 85:
            predicted_name = "Unknown"
        else:
            predicted_name = class_labels[predicted_index]

        response = {
            "predicted_name": predicted_name,
            "confidence": f"{confidence:.2f}%",
            "message": "Nhận diện thành công!" if predicted_name != "Unknown" else "Không đủ tự tin để xác định người."
        }   

        # Nếu có tọa độ khuôn mặt, trả về
        if face_coords:
            x, y, w, h = face_coords
            response["face_box"] = {
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "message": f"Có lỗi xảy ra trong quá trình xử lý: {str(e)}"
        }), 500