// Variables globales
const infoPanel = document.getElementById("info-panel");
const infoText = document.getElementById("info-text");
let selectedDay = null;
let calendarData = {};

// Inicializar el calendario
function initCalendar() {
    const currentYear = new Date().getFullYear();
    const yearSelect = document.getElementById("year-select");
    const monthSelect = document.getElementById("month-select");

    // Rellenar años
    for (let year = 2023; year <= 2030; year++) {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }

    // Rellenar meses
    const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    months.forEach((month, index) => {
        const option = document.createElement("option");
        option.value = index;
        option.textContent = month;
        monthSelect.appendChild(option);
    });

    yearSelect.value = currentYear;
    monthSelect.value = new Date().getMonth();
    renderCalendar(currentYear, monthSelect.value);
}

// Renderizar el calendario
function renderCalendar(year, month) {
    const calendar = document.getElementById("calendar");
    calendar.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        calendar.appendChild(document.createElement("div"));
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement("div");
        cell.className = "day-cell";
        cell.textContent = day;
        cell.onclick = () => openInfoPanel(day, month, year);
        calendar.appendChild(cell);
    }
}

// Abrir el panel de información
function openInfoPanel(day, month, year) {
    selectedDay = `${year}-${month + 1}-${day}`;
    infoText.value = calendarData[selectedDay] || "";
    infoPanel.style.display = "block";
}

// Guardar información
function guardarInfo() {
    if (selectedDay) {
        calendarData[selectedDay] = infoText.value;
        alert("Información guardada para el día " + selectedDay);
    }
}

document.getElementById("year-select").onchange = (e) => {
    renderCalendar(e.target.value, document.getElementById("month-select").value);
};

document.getElementById("month-select").onchange = (e) => {
    renderCalendar(document.getElementById("year-select").value, e.target.value);
};

// Inicializar la aplicación
initCalendar();
