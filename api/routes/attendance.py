from flask import Blueprint, request, jsonify

attendance_bp = Blueprint('attendance', __name__)


# Dữ liệu mẫu
students_data = {
    "cnpm1": [
        {"id_student": "21060451", "name": "Nguyễn Hùng Anh", "status": "Vắng mặt", "image": ''},
        {"id_student": "21073141","name": "Lê Phú Hào", "status": "Vắng mặt", "image": ''},
        {"id_student": "21119631","name": "Nguyễn Minh Long", "status": "Vắng mặt", "image": ''},
    ],
    "cnpm2": [
        {"id_student": "21060452", "name": "Nguyễn Hùng Anh", "status": "Vắng mặt", "image": ''},
        {"id_student": "21073142","name": "Lê Phú Hào", "status": "Vắng mặt", "image": ''},
    ]
}

@attendance_bp.route('/api/students/<class_id>', methods=['GET'])
def get_students(class_id):
    students = students_data.get(class_id)
    if students is None:
        return jsonify({"error": "Class not found"}), 404
    return jsonify(students), 200


@attendance_bp.route('/api/attendance', methods=['POST'])
def attendance():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        class_name = data.get('class_name')
        print(class_name)
        id_student = data.get('id_student')

        if not class_name or not id_student:
            return jsonify({"error": "Missing class or idStudent (id_student)"}), 400
        
        # Tìm lớp học
        students = students_data.get(class_name)
        if not students:
            return jsonify({"error": "Class not found"}), 404

        # Tìm sinh viên trong lớp
        student_found = False
        for student in students:
            if student.get("id_student") == id_student:
                student["status"] = "Đã điểm danh"
                student_found = True
                break

        if not student_found:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": f"Attendance marked for {id_student} in class {class_name}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
