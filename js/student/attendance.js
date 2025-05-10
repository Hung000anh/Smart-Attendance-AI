const apiBaseUrl = window.location.origin === 'http://127.0.0.1:5500' || window.location.origin === 'http://localhost:5500'
    ? 'http://127.0.0.1:5000'
    : 'https://your-deploy-link.onrender.com';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');

let predictionBuffer = [];
let isStop = false;
const BUFFER_LIMIT = 50;
let intervalId = null;

// Lấy tham số code và class từ URL
const urlParams = new URLSearchParams(window.location.search);
const classCode = urlParams.get('code');
const class_name = urlParams.get('class'); // Lấy tham số class (cnpm1 hoặc cnpm2)

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
        video.addEventListener('loadeddata', () => {
            startAutoCapture();
        });
    })
    .catch((err) => {
        console.error("Lỗi truy cập webcam: ", err);
        statusDiv.textContent = "❌ Không thể truy cập webcam.";
    });

function startAutoCapture() {
    // Kiểm tra xem className có hợp lệ không
    if (!class_name || (class_name !== 'cnpm1' && class_name !== 'cnpm2')) {
        statusDiv.textContent = '❌ Lớp không hợp lệ.';
        return;
    }
    if (!classCode) {
        statusDiv.textContent = '❌ Mã điểm danh không hợp lệ.';
        return;
    }

    intervalId = setInterval(() => {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append('image', blob, 'webcam.png');
            formData.append('classCode', classCode);

            //loadingDiv.style.display = 'block';

            fetch(`${apiBaseUrl}/api/face-detect`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.face_box && data.predicted_name) {
                    const { x, y, w, h } = data.face_box;

                    context.clearRect(0, 0, canvas.width, canvas.height);
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    context.strokeStyle = 'red';
                    context.lineWidth = 2;
                    context.strokeRect(x, y, w, h);
                    context.fillStyle = 'red';
                    context.font = '16px Arial';
                    context.fillText(`${data.predicted_name} (${data.confidence})`, x, y - 5);

                    predictionBuffer.push({
                        name: data.predicted_name.trim().toLowerCase(),
                        confidence: data.confidence
                    });

                    if (predictionBuffer.length >= BUFFER_LIMIT && isStop === false) {
                        finalizePrediction();
                        isStop = true;
                    }
                }
            })
            .catch(error => {
                console.error('Lỗi gửi ảnh:', error);
                statusDiv.textContent = 'Lỗi kết nối đến server.';
            })
            .finally(() => {
                //loadingDiv.style.display = 'none';
            });
        }, 'image/png');
    }, 200);
}

function finalizePrediction() {
    //clearInterval(intervalId);

    const nameCounts = {};
    predictionBuffer.forEach(item => {
        nameCounts[item.name] = (nameCounts[item.name] || 0) + 1;
        console.log(item.name + " " + nameCounts[item.name]);
    });

    const mostCommonName = Object.keys(nameCounts).reduce((a, b) =>
        nameCounts[a] > nameCounts[b] ? a : b
    );

    if (mostCommonName !== 'unknown') {

        let id_student = mostCommonName.substring(0, 8);
        sendAttendanceToServer(id_student, class_name);
        displayProfileStudent(id_student, class_name);
    } else {
        statusDiv.textContent = '❌ Không nhận diện được sinh viên.';
    }
}

function displayProfileStudent(id_student, class_id){
    fetch(`${apiBaseUrl}/api/student/${id_student}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Không tìm thấy sinh viên");
        }
        return response.json();
    })
    .then(student => {
        console.log("Thông tin sinh viên:", student);
        // Hiển thị thông tin sinh viên lên giao diện
        class_name = "";
        if (class_id === "cnpm1"){
            class_name = "Công nghệ phần mềm 1";
        } else if (class_id === "cnpm2"){
            class_name = "Công nghệ phần mềm 2";
        }
        statusDiv.textContent = `👤 ${student.name} - Trạng thái: ${student.status} - Mã lớp: ${class_name} `;
    })
    .catch(error => {
        console.error('Lỗi khi lấy thông tin sinh viên:', error);
        statusDiv.textContent = '❌ Không lấy được thông tin sinh viên.';
    });
}


function sendAttendanceToServer(id_student, class_name) {
    fetch(`${apiBaseUrl}/api/attendance`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ class_name: class_name, id_student: id_student }) // Thêm classCode
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error sending attendance:', error);
        statusDiv.textContent = 'Lỗi gửi thông tin điểm danh lên server.';
    });
}