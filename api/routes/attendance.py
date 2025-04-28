from flask import Blueprint, request, jsonify

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/api/attendance', methods=['POST'])
def attendance():
    try:
        data = request.get_json()  # Lấy dữ liệu JSON từ body của yêu cầu
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400  # Nếu không có JSON, trả về lỗi

        student_name = data.get('studentName')  # Lấy tên sinh viên từ dữ liệu JSON
        if not student_name:
            return jsonify({"error": "Missing studentName"}), 400
        
        # Tiến hành các xử lý khác với student_name ở đây
        return jsonify({"message": f"Attendance marked for {student_name}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500