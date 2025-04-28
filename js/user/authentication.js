const form = document.getElementById('loginForm');
const message = document.getElementById('message');

form.addEventListener('submit', function(event) {
event.preventDefault(); // Ngăn gửi form đi

const username = document.getElementById('username').value.trim();
const password = document.getElementById('password').value;

// Kiểm tra tài khoản ADMIN
if (username === 'ADMIN' && password === 'ADMIN') {
    message.textContent = 'Đăng nhập thành công!';
    message.className = 'message success';
    window.location.href = "teacher-dashboard.html";
} else {
    message.textContent = 'Tên đăng nhập hoặc mật khẩu sai!';
    message.className = 'message error';
}
});