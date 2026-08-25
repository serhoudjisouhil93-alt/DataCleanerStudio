// Live Feature Search Filter
document.getElementById('feature-search').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('#features-grid .card');

    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        const tags = card.getAttribute('data-tags').toLowerCase();
        if (text.includes(searchTerm) || tags.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// Download Counter Tracker Logic
const downloadBtn = document.getElementById('main-download-btn');
const countVal = document.getElementById('count-val');

downloadBtn.addEventListener('click', () => {
    let currentCount = parseInt(countVal.innerText);
    countVal.innerText = currentCount + 1;
});

// Smooth Scroll Helper
function scrollToPreview() {
    document.getElementById('preview').scrollIntoView({ behavior: 'smooth' });
}

// Interactive Data Sandbox Logic
const initialData = {
    headers: ["First Name  ", "LAST_NAME", " Age ", " Email Address "],
    rows: [
        ["  Alex ", "Smith", "29", "alex@test.com"],
        ["  Alex ", "Smith", "29", "alex@test.com"],
        ["Sarah  ", "CONNOR", "34", "sarah@domain.org "]
    ]
};

let currentHeaders = [...initialData.headers];
let currentRows = JSON.parse(JSON.stringify(initialData.rows));

function renderTable() {
    const headTr = document.getElementById('table-head');
    const bodyTb = document.getElementById('table-body');

    headTr.innerHTML = currentHeaders.map(h => `<th>${h}</th>`).join('');
    bodyTb.innerHTML = currentRows.map(r => `<tr>${r.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('');
}

function applyDemoTransform(action) {
    if (action === 'headers') {
        currentHeaders = currentHeaders.map(h => h.trim().toLowerCase().replace(/\s+/g, '_'));
    } else if (action === 'whitespace') {
        currentRows = currentRows.map(row => row.map(cell => cell.trim()));
    } else if (action === 'duplicates') {
        const unique = [];
        const seen = new Set();
        currentRows.forEach(row => {
            const key = row.join('|');
            if (!seen.has(key)) {
                seen.add(key);
                unique.push(row);
            }
        });
        currentRows = unique;
    }
    renderTable();
}

function resetDemoData() {
    currentHeaders = [...initialData.headers];
    currentRows = JSON.parse(JSON.stringify(initialData.rows));
    renderTable();
}