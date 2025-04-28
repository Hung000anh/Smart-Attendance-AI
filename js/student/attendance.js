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
const BUFFER_LIMIT = 50;
let intervalId = null;

const urlParams = new URLSearchParams(window.location.search);
const classCode = urlParams.get('code');

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

            if (predictionBuffer.length >= BUFFER_LIMIT) {
            finalizePrediction();
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
    clearInterval(intervalId);
    video.srcObject.getTracks().forEach(track => track.stop());

    const nameCounts = {};
    predictionBuffer.forEach(item => {
    nameCounts[item.name] = (nameCounts[item.name] || 0) + 1;
    console.log(item.name + " " + nameCounts[item.name]);
    });

    const mostCommonName = Object.keys(nameCounts).reduce((a, b) =>
    nameCounts[a] > nameCounts[b] ? a : b
    );

    if (mostCommonName !== 'unknown') {
    statusDiv.textContent = `✅ Đã điểm danh: ${mostCommonName}`;
    sendAttendanceToServer(mostCommonName);
    } else {
    statusDiv.textContent = '❌ Không nhận diện được sinh viên.';
    }
}

function sendAttendanceToServer(name) {
    fetch(`${apiBaseUrl}/api/attendance`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ studentName: name })
    })
    .then(response => response.json())
    .then(data => {
    console.log('Server response:', data);
    })
    .catch(error => {
    console.error('Error sending attendance:', error);
    });
}