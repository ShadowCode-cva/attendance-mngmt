const API_BASE = "http://127.0.0.1:5000/api";

// Elements
const loginSection = document.getElementById('login-section');
const dashboard = document.getElementById('staff-dashboard');
const loader = document.getElementById('loader');
const userInfo = document.getElementById('user-info');
const staffNameSpan = document.getElementById('staff-name');

// Forms
const emailInput = document.getElementById('email');
const passInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');

// State
let currentUser = JSON.parse(localStorage.getItem('user'));
let token = localStorage.getItem('token');

// Initialize
if (token && currentUser) {
    showDashboard();
}

// Password Toggle Logic
document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const input = document.getElementById(targetId);
        if (input.type === 'password') {
            input.type = 'text';
            this.innerText = '🚫'; // Or a slash eye icon
        } else {
            input.type = 'password';
            this.innerText = '👁️';
        }
    });
});

// Auth Logic
loginBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();
    const password = passInput.value.trim();

    if (!email || !password) return alert("Please fill credentials");

    toggleLoader(true);
    try {
        const res = await fetch(`${API_BASE}/staff/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (res.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            token = data.access_token;
            currentUser = data.user;
            
            // Auto-redirect Admin to Admin Panel
            if (currentUser.role === 'ADMIN') {
                window.location.href = "admin.html";
            } else {
                showDashboard();
            }
        } else {
            alert(data.message || "Login Failed");
        }
    } catch (e) {
        alert("Server connection error");
    } finally {
        toggleLoader(false);
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    location.reload();
});

function showDashboard() {
    loginSection.classList.add('hidden');
    dashboard.classList.remove('hidden');
    userInfo.classList.remove('hidden');
    staffNameSpan.innerText = `Welcome, ${currentUser.name}`;
    loadMetadata();
}

function toggleLoader(show) {
    loader.classList.toggle('hidden', !show);
}

// Dashboard Tabs
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.remove('hidden');
    });
});

// Load Classes and Subjects
let currentClassId = null;

async function loadMetadata() {
    try {
        const [yearsRes, deptsRes, subsRes] = await Promise.all([
            fetch(`${API_BASE}/metadata/years`),
            fetch(`${API_BASE}/metadata/departments`),
            fetch(`${API_BASE}/metadata/subjects`)
        ]);

        const yearsData = await yearsRes.json();
        const deptsData = await deptsRes.json();
        const subsData = await subsRes.json();

        // Populate Mark Attendance Tabs
        populateSelect('year-select', yearsData.years, '_id', 'name');
        populateSelect('dept-select', deptsData.departments, '_id', 'name');
        populateSelect('subject-select', subsData.subjects, 'name', 'name');

        // Populate Reports Tabs
        populateSelect('rep-year-select', yearsData.years, '_id', 'name');
        populateSelect('rep-dept-select', deptsData.departments, '_id', 'name');
        populateSelect('rep-subject-select', subsData.subjects, 'name', 'name');

    } catch (e) {
        console.error("Error loading metadata", e);
    }
}

function populateSelect(elementId, items, valueKey, textKey) {
    const select = document.getElementById(elementId);
    if (!select) return;
    select.innerHTML = '';
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item[valueKey];
        option.innerText = item[textKey];
        select.appendChild(option);
    });
}

// Attendance Marking Logic
const loadStudentsBtn = document.getElementById('load-students-btn');
const studentTableBody = document.getElementById('student-list-body');
const listContainer = document.getElementById('attendance-list-container');

loadStudentsBtn.addEventListener('click', async () => {
    const yearId = document.getElementById('year-select').options[document.getElementById('year-select').selectedIndex].value; // In a real app, use the actual _id if year uses ObjectId, but our seed uses the name/code or ObjectId. Let's assume we need to fetch the class by finding the matching year and dept.
    // Actually, in seed_db.py, years[1] was an ObjectId.
    // Wait, the API for /years returns the _id. I populated 'code' as the value, let's fix populateSelect call above to use '_id' for year. 
    // I will adjust the populateSelect above to use '_id'.
    // Let's assume the value is the _id for both year and dept.
    const yId = document.getElementById('year-select').value;
    const dId = document.getElementById('dept-select').value;

    toggleLoader(true);
    try {
        // Find Class ID
        const classRes = await fetch(`${API_BASE}/metadata/class?year_id=${yId}&dept_id=${dId}`);
        const classData = await classRes.json();

        if (!classRes.ok) {
            alert("No class found for this Year and Department combination.");
            studentTableBody.innerHTML = "";
            listContainer.classList.add('hidden');
            return;
        }

        currentClassId = classData.class_data._id;

        // Fetch Students
        const studentsRes = await fetch(`${API_BASE}/metadata/students?class_id=${currentClassId}`);
        const studentsData = await studentsRes.json();
        
        if (!studentsRes.ok || studentsData.students.length === 0) {
            alert("No students found in this class.");
            studentTableBody.innerHTML = "";
            listContainer.classList.add('hidden');
            return;
        }

        studentTableBody.innerHTML = "";
        studentsData.students.forEach(s => {
            const row = document.createElement('tr');
            row.classList.add('student-row');
            row.innerHTML = `
                <td>${s.reg_no}</td>
                <td>${s.name}</td>
                <td>
                    <div class="status-toggle" data-id="${s._id}">
                        <button class="toggle-btn present active" data-status="PRESENT">PRESENT</button>
                        <button class="toggle-btn absent" data-status="ABSENT">ABSENT</button>
                    </div>
                </td>
            `;
            studentTableBody.appendChild(row);
        });

        document.getElementById('student-count').innerText = studentsData.students.length;
        listContainer.classList.remove('hidden');

        // Add Toggle Logic
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const parent = btn.parentElement;
                parent.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

    } catch (e) {
        alert("Error loading class data");
    } finally {
        toggleLoader(false);
    }
});

// Bulk Present
document.getElementById('all-present-btn').addEventListener('click', () => {
    document.querySelectorAll('.toggle-btn[data-status="PRESENT"]').forEach(btn => btn.click());
});

// Final Submit
document.getElementById('submit-attendance-btn').addEventListener('click', async () => {
    if (!currentClassId) return alert("Please load students first.");

    const payload = {
        class_id: currentClassId,
        subject: document.getElementById('subject-select').value,
        hour: parseInt(document.getElementById('hour-select').value),
        date: new Date().toISOString().split('T')[0],
        records: []
    };

    document.querySelectorAll('.status-toggle').forEach(toggle => {
        const studentId = toggle.dataset.id;
        const status = toggle.querySelector('.active').dataset.status;
        payload.records.push({ student_id: studentId, status });
    });

    toggleLoader(true);
    try {
        const res = await fetch(`${API_BASE}/staff/mark`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });
        const responseText = await res.text();
        let data = {};
        try { data = JSON.parse(responseText); } catch(e) {}
        
        if (res.ok) {
            alert("Success: Attendance Recorded");
            listContainer.classList.add('hidden');
        } else if (res.status === 401) {
            alert("Your session has expired. Please log in again.");
            localStorage.clear();
            location.reload();
        } else {
            console.error("Submission failed:", responseText);
            alert(`Error ${res.status}: ` + (data.message || data.msg || data.error || responseText || "Submission Failed"));
        }
    } catch (e) {
        alert("Error submitting: " + e.message);
    } finally {
        toggleLoader(false);
    }
});

// Staff Report Logic
const genReportBtn = document.getElementById('gen-report-btn');
const reportResult = document.getElementById('report-result');

genReportBtn.addEventListener('click', async () => {
    const yId = document.getElementById('rep-year-select').value;
    const dId = document.getElementById('rep-dept-select').value;
    const date = document.getElementById('rep-date-select').value;
    const subject = document.getElementById('rep-subject-select').value;

    if (!date) return alert("Please select a date.");

    toggleLoader(true);
    try {
        // Find Class ID
        const classRes = await fetch(`${API_BASE}/metadata/class?year_id=${yId}&dept_id=${dId}`);
        const classData = await classRes.json();

        if (!classRes.ok) {
            alert("No class found for this Year and Department combination.");
            reportResult.innerHTML = "";
            reportResult.classList.add('hidden');
            return;
        }

        const classId = classData.class_data._id;

        const res = await fetch(`${API_BASE}/staff/report/class?class_id=${classId}&date=${date}&subject=${subject}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.status === 401) {
            alert("Your session has expired. Please log in again.");
            localStorage.clear();
            location.reload();
            return;
        }
        
        const data = await res.json();
        
        if (res.ok) {
            reportResult.innerHTML = `
                <div class="report-card" style="padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px; margin-top: 20px;">
                    <h3 style="color: var(--primary);">Report: ${data.class_name}</h3>
                    <p style="color: var(--text-dim); margin-bottom: 15px;">Subject: ${subject} | Date: ${date}</p>
                    <div class="stats-row">
                        <div class="stat-card glass">
                            <span class="label">Total Strength</span>
                            <span class="value">${data.total_strength}</span>
                        </div>
                        <div class="stat-card glass">
                            <span class="label">Total Absentees</span>
                            <span class="value" style="color: #ff4d4d;">${data.absentees ? data.absentees.length : 0}</span>
                        </div>
                    </div>
                </div>
            `;
            reportResult.classList.remove('hidden');
        } else {
            alert(data.message || "Failed to generate report.");
        }
    } catch (e) {
        alert("Error generating report: " + e.message);
    } finally {
        toggleLoader(false);
    }
});
