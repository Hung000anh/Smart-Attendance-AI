from flask import Flask
from flask_cors import CORS
from routes import face_detect_bp, attendance_bp # Import các Blueprint từ thư mục routes

app = Flask(__name__)
CORS(app)  # Enable CORS

# Đăng ký các Blueprint
app.register_blueprint(face_detect_bp)
app.register_blueprint(attendance_bp)

if __name__ == '__main__':
    app.run(debug=True)
