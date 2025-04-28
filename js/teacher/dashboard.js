let codeClass1 = "";
let codeClass2 = "";

function startAttendance(className) {
    let code;
    if (className === 'class1') {
    code = generateCode();
    codeClass1 = code;
    const link = `attend.html?code=${code}`;
    document.getElementById("status1").textContent = "🔔 Đang điểm danh...";
    document.getElementById("attendance-link1").style.display = "block";
    document.getElementById("linkText1").href = link;
    document.getElementById("linkText1").textContent = link;
    document.getElementById("startBtn1").style.display = "none";
    document.getElementById("stopBtn1").style.display = "inline-block";
    } else if (className === 'class2') {
    code = generateCode();
    codeClass2 = code;
    const link = `attend.html?code=${code}`;
    document.getElementById("status2").textContent = "🔔 Đang điểm danh...";
    document.getElementById("attendance-link2").style.display = "block";
    document.getElementById("linkText2").href = link;
    document.getElementById("linkText2").textContent = link;
    document.getElementById("startBtn2").style.display = "none";
    document.getElementById("stopBtn2").style.display = "inline-block";
    }
}

function stopAttendance(className) {
    if (className === 'class1') {
    document.getElementById("status1").textContent = "✅ Đã dừng điểm danh.";
    document.getElementById("attendance-link1").style.display = "none";
    document.getElementById("startBtn1").style.display = "inline-block";
    document.getElementById("stopBtn1").style.display = "none";
    } else if (className === 'class2') {
    document.getElementById("status2").textContent = "✅ Đã dừng điểm danh.";
    document.getElementById("attendance-link2").style.display = "none";
    document.getElementById("startBtn2").style.display = "inline-block";
    document.getElementById("stopBtn2").style.display = "none";
    }
}

function copyLink(className) {
    let link;
    if (className === 'class1') {
    link = document.getElementById("linkText1").href;
    } else if (className === 'class2') {
    link = document.getElementById("linkText2").href;
    }

    navigator.clipboard.writeText(link).then(() => {
    alert("Đã copy link vào clipboard! Gửi cho sinh viên nhé 👨‍🎓");
    });
}

function viewStudents(className) {
    let classQuery = (className === 'class1') ? 'cnpm1' : 'cnpm2';
    window.location.href = `students-list.html?class=${classQuery}`;
}

function generateCode(length = 6) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}