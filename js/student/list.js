const students = {
  cnpm1: [
    { name: 'Nguyễn Văn A', status: 'Đã điểm danh', image: 'https://via.placeholder.com/100' },
    { name: 'Trần Thị B', status: 'Vắng mặt', image: 'https://via.placeholder.com/100' },
  ],
  cnpm2: [
    { name: 'Lê Minh D', status: 'Đã điểm danh', image: 'https://via.placeholder.com/100' },
    { name: 'Hoàng Thị E', status: 'Vắng mặt', image: 'https://via.placeholder.com/100' },
  ]
};

const classQuery = new URLSearchParams(window.location.search).get('class');
const studentListElement = document.getElementById('student-list');

if (students[classQuery]) {
  let tableHTML = `<table>
    <thead>
      <tr>
        <th>STT</th>
        <th>Họ và Tên</th>
        <th>Trạng Thái</th>
      </tr>
    </thead>
    <tbody>`;
  
  students[classQuery].forEach((student, index) => {
    const statusIcon = student.status === 'Đã điểm danh' 
      ? '<span class="status-icon status-yes">&#10003;</span>' // Checkmark
      : '<span class="status-icon status-no">&#10007;</span>'; // Cross mark

    tableHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${student.name}</td>
        <td>${statusIcon}</td>
      </tr>`;
  });

  tableHTML += `</tbody></table>`;
  studentListElement.innerHTML = tableHTML;
} else {
  studentListElement.innerHTML = "<p class='no-student'>Không có sinh viên trong lớp này.</p>";
}

function exportToExcel() {
  const ws = XLSX.utils.table_to_sheet(document.querySelector("table"));
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Danh Sách Sinh Viên");

  // Xuất file Excel
  XLSX.writeFile(wb, "danh_sach_sinh_vien.xlsx");
}

function viewAllImages() {
  const modal = document.getElementById('image-modal');
  const modalImages = document.getElementById('modal-images');
  modalImages.innerHTML = '';

  students[classQuery].forEach(student => {
    if (student.status === 'Đã điểm danh') {
      const div = document.createElement('div');
      div.style.textAlign = 'center';
      div.innerHTML = `<img src="${student.image}" alt="${student.name}" /><p>${student.name}</p>`;
      modalImages.appendChild(div);
    }
  });

  modal.style.display = 'flex';
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