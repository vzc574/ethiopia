const months = ["Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit", "Megabit", "Miazia", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"];

// 1. Initialize Sidebar (Downward Stack)
const nav = document.getElementById('month-list');
months.forEach((name, i) => {
    const btn = document.createElement('button');
    btn.className = "month-btn";
    btn.innerText = name;
    btn.onclick = () => loadMonth(i);
    nav.appendChild(btn);
});

// 2. Load Month Grid (Orange/Blue Logic)
async function loadMonth(idx) {
    const year = parseInt(document.getElementById('eth-year').value);
    
    const res = await fetch('http://127.0.0.1:8000/month', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ year: year, month_idx: idx })
    });
    const data = await res.json();
    
    document.getElementById('view-title').innerText = `${data.month_name} ${data.year}`;
    const grid = document.getElementById('days-grid');
    grid.innerHTML = '';

    // Add spacers for weekday alignment
    for (let i = 0; i < data.start_col; i++) {
        grid.innerHTML += '<div class="day-cell empty"></div>';
    }

    // Add days
    data.grid.forEach(item => {
        const hasHol = item.holidays && item.holidays.length > 0;
        const cell = document.createElement('div');
        
        // Match GUI Colors
        cell.className = `day-cell ${hasHol ? 'holiday' : 'regular'}`;
        cell.innerHTML = `<span>${item.day}</span>`;
        
        if (hasHol) {
            cell.onclick = () => openDetail(item.holidays[0]);
        }
        grid.appendChild(cell);
    });
}

// 3. Holiday Detail (Descriptions and Image)
async function openDetail(key) {
    const res = await fetch(`http://127.0.0.1:8000/holiday/${key}`);
    const data = await res.json();

    document.getElementById('m-name-en').innerText = data.name.english;
    document.getElementById('m-name-am').innerText = data.name.amharic;
    document.getElementById('m-desc-am').innerText = data.description.amharic;
    document.getElementById('m-desc-en').innerText = data.description.english;
    
    const img = document.getElementById('m-image');
    img.src = `http://127.0.0.1:8000/${data.image}`;
    img.style.display = data.image ? "block" : "none";

    document.getElementById('modal').classList.remove('hidden');
}

// 4. Converter Function
async function convertDate() {
    const d = parseInt(document.getElementById('c-d').value);
    const m = parseInt(document.getElementById('c-m').value);
    const y = parseInt(document.getElementById('eth-year').value);

    const res = await fetch('http://127.0.0.1:8000/convert', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ year: y, month: m, day: d })
    });
    const data = await res.json();
    const resEl = document.getElementById('conv-res');
    
    if (data.gregorian) {
        resEl.innerText = `GC: ${data.gregorian}`;
        resEl.style.color = "lightgreen";
    } else {
        resEl.innerText = "Error: Invalid Input";
        resEl.style.color = "red";
    }
}

function closeModal() { document.getElementById('modal').classList.add('hidden'); }