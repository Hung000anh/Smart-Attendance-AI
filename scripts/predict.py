import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet_v2 import preprocess_input

# Load mô hình đã huấn luyện
model = load_model('model/model.keras')

# Danh sách nhãn lớp
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

# Load bộ phát hiện khuôn mặt Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Kích thước ảnh đầu vào cho model
input_shape = (224, 224)

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Nhấn 'q' để thoát")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể truy cập webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(face_rgb).resize(input_shape)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        confidence = np.max(predictions) * 100
        predicted_index = np.argmax(predictions)

        # Xử lý nhãn nếu tự tin dưới 85%
        if confidence < 80:
            label = "Unknown"
        else:
            predicted_class = class_labels[predicted_index]
            label = f"{predicted_class} ({confidence:.2f}%)"

        # Vẽ khung và nhãn
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Smart Attendance AI - Press 'q' to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
