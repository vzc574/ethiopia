const monthNames = ["Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit", "Megabit", "Miazia", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"];

// Initialize Month Buttons in Sidebar
const nav = document.getElementById('month-list');
monthNames.forEach((name, idx) => {
    const btn = document.createElement('button');
    btn.innerText = name;
    btn.className = "month-btn";
    btn.onclick = () => loadMonth(idx);
    nav.appendChild(btn);
});

async function loadMonth(idx) {
    const year = document.getElementById('eth-year').value;
    try {
        const response = await fetch(`http://127.0.0.1:8000/month/${year}/${idx}`);
        const data = await response.json();

        // Update Header
        document.getElementById('month-title').innerText = `${data.month_name} ${year}`;
        document.getElementById('evangelist-tag').innerText = `Zemene ${data.evangelist}`;

        const grid = document.getElementById('days-grid');
        grid.innerHTML = '';

        // Add Empty Slots for Weekday Alignment
        for (let i = 0; i < data.start_col; i++) {
            grid.innerHTML += `<div class="day-cell empty"></div>`;
        }

        // Add Day Cells
        for (let d = 1; d <= data.num_days; d++) {
            const hols = data.holidays[d] || [];
            const isHoliday = hols.length > 0;
            
            const cell = document.createElement('div');
            cell.className = `day-cell ${isHoliday ? 'holiday' : ''}`;
            cell.innerHTML = `<strong>${d}</strong>${isHoliday ? `<br><small>${hols[0]}</small>` : ''}`;
            
            if (isHoliday) {
                cell.onclick = () => showHolidayDetail(hols[0]);
            }
            grid.appendChild(cell);
        }
    } catch (error) {
        console.error("Error loading month:", error);
    }
}

async function showHolidayDetail(holidayKey) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/detail/${holidayKey}`);
        const data = await response.json();

        // Map Data to Modal Elements
        document.getElementById('m-name-en').innerText = data.name.english;
        document.getElementById('m-name-am').innerText = data.name.amharic;
        document.getElementById('m-desc-am').innerText = data.description.amharic;
        document.getElementById('m-desc-en').innerText = data.description.english;

        // Handle Image loading similar to main_calendar.py logic
        const imgElement = document.getElementById('m-image');
        if (data.image) {
            // Points to the FastAPI static mount /assest/
            imgElement.src = `http://127.0.0.1:8000/${data.image}`;
            imgElement.style.display = "block";
        } else {
            imgElement.style.display = "none";
        }

        document.getElementById('modal').classList.remove('hidden');
    } catch (error) {
        console.error("Error loading details:", error);
    }
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}

// Date Converter Logic mirroring run_conversion
async function convert() {
    const day = document.getElementById('c-d').value;
    const month = document.getElementById('c-m').value;
    const year = document.getElementById('eth-year').value;

    if (!day || !month) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/convert?year=${year}&month=${month}&day=${day}`);
        const data = await response.json();
        
        const out = document.getElementById('conv-out');
        if (data.formatted) {
            out.innerText = "GC: " + data.formatted;
            out.style.color = "green";
        } else {
            out.innerText = "Invalid Input";
            out.style.color = "red";
        }
    } catch (error) {
        document.getElementById('conv-out').innerText = "Server Error";
    }
}