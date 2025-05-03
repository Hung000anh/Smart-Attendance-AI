const apiBaseUrl = window.location.origin === 'http://127.0.0.1:5500' || window.location.origin === 'http://localhost:5500'
    ? 'http://127.0.0.1:5000'
    : 'https://your-deploy-link.onrender.com';

const classQuery = new URLSearchParams(window.location.search).get('class');
const studentListElement = document.getElementById('student-list');

function fetchStudents(className) {
    fetch(`${apiBaseUrl}/api/students/${className}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data === null || data === undefined) {
            console.log("Data is null or undefined");
        } else if (Array.isArray(data) && data.length === 0) {
            console.log("Data is an empty array");
        } else if (typeof data === 'object' && Object.keys(data).length === 0) {
            console.log("Data is an empty object");
        } else {
            console.log("Data received:", data); // Log toàn bộ data để kiểm tra
        }
        if (data && Array.isArray(data) && data.length > 0) {
            renderStudentTable(data); // Truyền trực tiếp data vào renderStudentTable
        } else {
            studentListElement.innerHTML = "<p class='no-student'>Không có sinh viên trong lớp này.</p>";
        }
    })
    .catch(error => {
        console.error('Lỗi khi lấy danh sách sinh viên:', error);
        studentListElement.innerHTML = "<p class='no-student'>Lỗi khi tải danh sách sinh viên.</p>";
    });
}

function renderStudentTable(students) {
    let tableHTML = `<table>
        <thead>
            <tr>
                <th>STT</th>
                <th>MSSV</th>
                <th>Họ và Tên</th>
                <th>Trạng Thái</th>
            </tr>
        </thead>
        <tbody>`;
    
    students.forEach((student, index) => {
        const statusIcon = student.status === 'Đã điểm danh' 
            ? '<span class="status-icon status-yes">✓</span>' // Checkmark
            : '<span class="status-icon status-no">✗</span>'; // Cross mark

        tableHTML += `
            <tr>
                <td>${index + 1}</td>
                <td>${student.id_student}</td>
                <td>${student.name}</td>
                <td>${statusIcon}</td>
            </tr>`;
    });

    tableHTML += `</tbody></table>`;
    studentListElement.innerHTML = tableHTML;
}

// Gọi API khi trang được tải
if (classQuery) {
    fetchStudents(classQuery);
} else {
    studentListElement.innerHTML = "<p class='no-student'>Không có thông tin lớp.</p>";
}

function exportToExcel() {
    const table = document.querySelector("table");
    if (table) {
        const ws = XLSX.utils.table_to_sheet(table);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Danh Sách Sinh Viên");
        XLSX.writeFile(wb, "danh_sach_sinh_vien.xlsx");
    } else {
        alert("Không có bảng dữ liệu để xuất!");
    }
}

function viewAllImages() {
    const modal = document.getElementById('image-modal');
    const modalImages = document.getElementById('modal-images');
    modalImages.innerHTML = '';

    // Gọi lại API để lấy dữ liệu mới nhất
    fetchStudents(classQuery).then(() => {
        fetch(`${apiBaseUrl}/api/students?class=${classQuery}`)
            .then(response => response.json())
            .then(data => {
                if (data && Array.isArray(data.students)) {
                    data.students.forEach(student => {
                        if (student.status === 'Đã điểm danh') {
                            const div = document.createElement('div');
                            div.style.textAlign = 'center';
                            div.innerHTML = `<img src="${student.image}" alt="${student.name}" /><p>${student.name}</p>`;
                            modalImages.appendChild(div);
                        }
                    });
                    modal.style.display = 'flex';
                }
            })
            .catch(error => {
                console.error('Lỗi khi lấy danh sách sinh viên:', error);
                alert("Lỗi khi tải hình ảnh sinh viên.");
            });
    });
}

function closeModal() {
    const modal = document.getElementById('image-modal');
    modal.style.display = 'none';
}

function goBack() {
    window.history.back();
    // Hoặc bạn có thể chuyển hướng về trang chính của giáo viên
    // window.location.href = 'teacher-dashboard.html';
}