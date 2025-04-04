import os

# ==== CẤU HÌNH ĐƯỜNG DẪN ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Thư mục gốc
DATA_DIR = os.path.join(BASE_DIR, "..", "dataset")  # Ảnh gốc
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")  # Thư mục lưu mô hình
HAARCASCADE_DIR = os.path.join(BASE_DIR, "..","haarcascade")

# ==== CẤU HÌNH ẢNH ====
IMG_SIZE = (224, 224)  # Kích thước ảnh đầu vào cho CNN
IMG_CHANNELS = 3  # Ảnh RGB (3 kênh màu)

# ==== CẤU HÌNH THU THẬP DỮ LIỆU ====
MAX_IMAGES_PER_STUDENT = 500  # Số ảnh tối đa mỗi sinh viên
WEBCAM_INDEX = 0  # Index của webcam (0 là webcam mặc định)





