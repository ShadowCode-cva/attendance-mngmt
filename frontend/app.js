const searchBtn = document.getElementById('search-btn');
const backBtn = document.getElementById('back-btn');
const regInput = document.getElementById('reg-no');
const searchSection = document.getElementById('search-section');
const dashboardSection = document.getElementById('dashboard-section');
const loader = document.getElementById('loader');

const percentageVal = document.getElementById('percentage-val');
const presentVal = document.getElementById('present-val');
const absentVal = document.getElementById('absent-val');
const totalVal = document.getElementById('total-val');
const circle = document.getElementById('progress-circle');

const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = circumference;

function setProgress(percent) {
    const offset = circumference - (percent / 100 * circumference);
    circle.style.strokeDashoffset = offset;
}

searchBtn.addEventListener('click', async () => {
    const regNo = regInput.value.trim();
    if (!regNo) {
        alert('Please enter a registration number');
        return;
    }

    loader.classList.remove('hidden');

    try {
        // Fetch from Backend API
        const response = await fetch(`http://127.0.0.1:5000/api/student/attendance/${regNo}`);
        const data = await response.json();

        if (response.ok) {
            // Update UI
            percentageVal.innerText = Math.round(data.percentage);
            presentVal.innerText = data.present_count;
            absentVal.innerText = data.absent_count;
            totalVal.innerText = data.total_sessions;

            // Transition
            searchSection.classList.add('hidden');
            dashboardSection.classList.remove('hidden');
            
            // Animate progress
            setTimeout(() => {
                setProgress(data.percentage);
            }, 300);
        } else {
            alert(data.message || 'Error fetching data');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the server. Make sure the backend is running.');
    } finally {
        loader.classList.add('hidden');
    }
});

backBtn.addEventListener('click', () => {
    dashboardSection.classList.add('hidden');
    searchSection.classList.remove('hidden');
    setProgress(0);
});

// Allow 'Enter' key to search
regInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchBtn.click();
});
