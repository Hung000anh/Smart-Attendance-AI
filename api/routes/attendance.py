from flask import Blueprint, request, jsonify

attendance_bp = Blueprint('attendance', __name__)


# Dữ liệu mẫu
students_data = {
    "cnpm1": [
        {"id_student": "21060451", "name": "Nguyễn Hùng Anh", "status": "Vắng mặt", "image": ''},
        {"id_student": "21073141","name": "Lê Phú Hào", "status": "Vắng mặt", "image": ''},
        {"id_student": "21119631","name": "Nguyễn Minh Long", "status": "Vắng mặt", "image": ''},
        {"id_student": "21075071","name": "Nguyễn Hạnh Bảo Ân", "status": "Vắng mặt", "image": ''},
        {"id_student": "21090261","name": "Dương Ngọc Anh", "status": "Vắng mặt", "image": ''},
        {"id_student": "21094341","name": "Chau Tiểu Long", "status": "Vắng mặt", "image": ''},
        {"id_student": "21096911","name": "Nguyễn Nhật Tùng", "status": "Vắng mặt", "image": ''},
        {"id_student": "21105351","name": "Tống Thành Lộc", "status": "Vắng mặt", "image": ''},
        {"id_student": "21115461","name": "Trần Tuấn Anh", "status": "Vắng mặt", "image": ''},
    ],
    "cnpm2": [
        {"id_student": "21060452", "name": "Nguyễn Hùng Anh", "status": "Vắng mặt", "image": ''},
        {"id_student": "21073142","name": "Lê Phú Hào", "status": "Vắng mặt", "image": ''},
    ]
}

@attendance_bp.route('/api/student/<id_student>', methods=['GET'])
def get_student_by_id(id_student):
    for class_students in students_data.values():
        for student in class_students:
            if student['id_student'] == id_student:
                return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404


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
