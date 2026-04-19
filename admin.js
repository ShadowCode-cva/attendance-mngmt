const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:5000/api'
    : '/api';
let token = localStorage.getItem('token');
let currentUser = JSON.parse(localStorage.getItem('user'));

// Check Auth
if (!token || currentUser?.role !== 'ADMIN') {
    alert("Admin access only. Please login as admin.");
    window.location.href = "staff.html";
}

// Password Toggle Logic
document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const input = document.getElementById(targetId);
        if (input.type === 'password') {
            input.type = 'text';
            this.innerText = '🚫';
        } else {
            input.type = 'password';
            this.innerText = '👁️';
        }
    });
});

// Nav Logic
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.admin-page').forEach(p => p.classList.add('hidden'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.page).classList.remove('hidden');
    });
});

// Logout
document.getElementById('admin-logout').addEventListener('click', () => {
    localStorage.clear();
    window.location.href = "staff.html";
});

// Initial Load
document.getElementById('admin-welcome').innerText = `Logged in as ${currentUser.name}`;
loadMetadata();
loadStaff();

async function loadStaff() {
    try {
        const res = await fetch(`${API_BASE}/admin/staff`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        
        if (res.ok) {
            const tbody = document.getElementById('staff-list-body');
            tbody.innerHTML = '';
            data.staff.forEach(s => {
                tbody.innerHTML += `
                    <tr class="student-row">
                        <td>${s.name}</td>
                        <td>${s.email}</td>
                        <td>${s.department || '-'}</td>
                        <td><span style="color: var(--success); font-weight: bold;">Active</span></td>
                    </tr>
                `;
            });
            document.getElementById('count-staff').innerText = data.staff.length;
        }
    } catch (e) {
        console.error("Error loading staff", e);
    }
}

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

        populateSelect('adm-year-select', yearsData.years, '_id', 'name');
        populateSelect('adm-dept-select', deptsData.departments, '_id', 'name');
        populateSelect('adm-subject-select', subsData.subjects, 'name', 'name');
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

// Mock Stats (In reality, fetch from API)
document.getElementById('count-staff').innerText = "3";
document.getElementById('count-students').innerText = "150";
document.getElementById('count-classes').innerText = "12";

// Staff Management
const staffTableBody = document.getElementById('staff-list-body');
const openModalBtn = document.getElementById('open-staff-modal');
const closeModalBtn = document.getElementById('close-staff-modal');
const staffModal = document.getElementById('staff-modal');
const createStaffBtn = document.getElementById('create-staff-btn');

openModalBtn.addEventListener('click', () => staffModal.classList.remove('hidden'));
closeModalBtn.addEventListener('click', () => staffModal.classList.add('hidden'));

createStaffBtn.addEventListener('click', async () => {
    const payload = {
        name: document.getElementById('new-staff-name').value,
        email: document.getElementById('new-staff-email').value,
        password: document.getElementById('new-staff-pass').value,
        department: document.getElementById('new-staff-dept').value
    };

    try {
        const res = await fetch(`${API_BASE}/admin/create-staff`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            alert("Staff Account Created Successfully!");
            staffModal.classList.add('hidden');
            document.getElementById('new-staff-name').value = '';
            document.getElementById('new-staff-email').value = '';
            document.getElementById('new-staff-pass').value = '';
            document.getElementById('new-staff-dept').value = '';
            loadStaff();
        } else {
            alert(data.error || data.message || "Error creating staff");
        }
    } catch (e) {
        alert("Server error");
    }
});

// Global Report Logic
const genBtn = document.getElementById('adm-gen-report');
genBtn.addEventListener('click', async () => {
    const yId = document.getElementById('adm-year-select').value;
    const dId = document.getElementById('adm-dept-select').value;
    const date = document.getElementById('adm-date-select').value;
    const subject = document.getElementById('adm-subject-select').value;

    try {
        // Find Class ID
        const classRes = await fetch(`${API_BASE}/metadata/class?year_id=${yId}&dept_id=${dId}`);
        const classData = await classRes.json();

        if (!classRes.ok) {
            alert("No class found for this Year and Department combination.");
            return;
        }

        const classId = classData.class_data._id;

        const res = await fetch(`${API_BASE}/admin/reports/all?class_id=${classId}&date=${date}&subject=${subject}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.status === 401) {
            alert("Your session has expired. Please log in again.");
            localStorage.clear();
            window.location.href = "staff.html";
            return;
        }
        
        const data = await res.json();
        
        if (res.ok) {
            let absenteesHtml = data.absentees.length > 0 ? 
                `<ul style="list-style: none; padding: 0; margin-top: 10px;">` + 
                data.absentees.map(a => `<li style="padding: 8px; background: rgba(255,0,0,0.1); margin-bottom: 5px; border-radius: 6px;">${a.reg_no || ''} - ${a.student_name}</li>`).join('') + 
                `</ul>` : 
                `<p style="color: var(--success); margin-top: 10px;">Perfect attendance! No absentees.</p>`;

            document.getElementById('adm-report-result').innerHTML = `
                <div class="report-card glass" style="padding: 20px; border-radius: 12px;">
                    <h3 style="color: var(--primary);">Audit Report: ${data.class_name}</h3>
                    <p style="color: var(--text-dim); margin-bottom: 15px;">Subject: ${subject} | Date: ${date}</p>
                    <div class="stats-row" style="margin-bottom: 20px;">
                        <div class="stat-card" style="background: rgba(255,255,255,0.05);">
                            <span class="label">Total Strength</span>
                            <span class="value">${data.total_strength}</span>
                        </div>
                        <div class="stat-card" style="background: rgba(255,255,255,0.05);">
                            <span class="label">Total Absentees</span>
                            <span class="value" style="color: #ff4d4d;">${data.absentees.length}</span>
                        </div>
                    </div>
                    <h4>Absentees List</h4>
                    ${absenteesHtml}
                </div>
            `;
            document.getElementById('adm-report-result').classList.remove('hidden');
        } else {
            alert(data.message || "Failed to fetch report.");
        }
    } catch (e) {
        alert("Server error");
    }
});

// Student Lookup Logic
const lookupBtn = document.getElementById('lookup-btn');
lookupBtn.addEventListener('click', async () => {
    const regNo = document.getElementById('lookup-reg-no').value.trim();
    if (!regNo) return alert("Please enter a register number.");

    try {
        const res = await fetch(`${API_BASE}/student/attendance/${regNo}`);
        const data = await res.json();

        if (res.ok) {
            document.getElementById('lookup-result').innerHTML = `
                <div class="report-card glass" style="padding: 20px; border-radius: 12px; display: flex; flex-direction: column; gap: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
                        <div>
                            <h3 style="color: var(--primary); margin: 0; font-size: 1.5rem;">${data.student_name}</h3>
                            <span style="color: var(--text-dim);">${regNo}</span>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2.5rem; font-weight: 800; color: ${data.percentage >= 75 ? 'var(--success)' : '#ff4d4d'};">${data.percentage}%</div>
                            <span style="color: var(--text-dim); font-size: 0.9rem;">Attendance</span>
                        </div>
                    </div>
                    <div class="stats-row">
                        <div class="stat-card" style="background: rgba(255,255,255,0.05);">
                            <span class="label">Total Classes</span>
                            <span class="value">${data.total_sessions}</span>
                        </div>
                        <div class="stat-card" style="background: rgba(255,255,255,0.05);">
                            <span class="label">Classes Attended</span>
                            <span class="value" style="color: var(--success);">${data.present_count}</span>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('lookup-result').classList.remove('hidden');
        } else {
            alert(data.message || "Student not found.");
        }
    } catch (e) {
        alert("Server error");
    }
});
