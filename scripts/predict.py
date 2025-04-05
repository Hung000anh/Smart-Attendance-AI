import cv2
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet_v2 import preprocess_input
# Lấy danh sách nhãn
student_ids = {
    '21060451_NguyenHungAnh': 0,
    '21090261_DuongNgocAnh': 1,
    '21094341_ChauTieuLong': 2,
    '21096911_NguyenNhatTung': 3,
    '21105351_TongThanhLoc': 4,
    '21119631_NguyenMinhLong': 5
}

# Load the saved model
model = load_model('model/restnet50v2.keras')  

g_dict = student_ids 
classes = list(g_dict.keys())

# Load bộ phát hiện khuôn mặt Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Mở webcam
cap = cv2.VideoCapture(0)  # 0 là webcam mặc định

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển ảnh sang grayscale để tăng hiệu suất phát hiện khuôn mặt
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Cắt vùng khuôn mặt
        face = frame[y:y+h, x:x+w]

        # Tiền xử lý ảnh khuôn mặt
        face_resized = cv2.resize(face, (224, 224))  # Resize về 224x224
        img_array = tf.keras.preprocessing.image.img_to_array(face_resized)
        img_array = tf.expand_dims(img_array, axis=0)  # Thêm batch dimension
        img_array = preprocess_input(img_array)

        
        # Dự đoán
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # Lấy nhãn dự đoán
        predicted_label = classes[np.argmax(score)]
        confidence = 100 * np.max(score)

        # Vẽ hình chữ nhật xung quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hiển thị nhãn dự đoán
        text = f"{predicted_label} ({confidence:.2f}%)"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Hiển thị khung hình
    cv2.imshow("Face Recognition", frame)

    # Thoát khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
