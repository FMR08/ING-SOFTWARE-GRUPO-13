document.addEventListener("DOMContentLoaded", () => {
    const yearSelector = document.getElementById("year-selector");
    const monthSelector = document.getElementById("month-selector");
    const calendarGrid = document.querySelector(".calendar-grid");

    const generateCalendar = (year, month) => {
        // Limpia el calendario anterior
        const days = calendarGrid.querySelectorAll(".day-cell");
        days.forEach(day => day.remove());

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Ajuste del índice del día (empieza en lunes)
        const adjustedFirstDay = (firstDay === 0 ? 6 : firstDay - 1);

        // Agrega celdas vacías para días previos al inicio del mes
        for (let i = 0; i < adjustedFirstDay; i++) {
            const emptyCell = document.createElement("div");
            emptyCell.classList.add("day-cell", "empty-cell");
            calendarGrid.appendChild(emptyCell);
        }

        // Agrega días del mes
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement("div");
            dayCell.classList.add("day-cell");
            dayCell.textContent = day;
            calendarGrid.appendChild(dayCell);
        }
    };

    // Población de selectores
    for (let year = 2023; year <= 2030; year++) {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearSelector.appendChild(option);
    }

    for (let month = 0; month < 12; month++) {
        const option = document.createElement("option");
        option.value = month;
        option.textContent = new Date(0, month).toLocaleString("es", { month: "long" });
        monthSelector.appendChild(option);
    }

    // Eventos para cambiar mes/año
    yearSelector.addEventListener("change", () => {
        generateCalendar(parseInt(yearSelector.value), parseInt(monthSelector.value));
    });

    monthSelector.addEventListener("change", () => {
        generateCalendar(parseInt(yearSelector.value), parseInt(monthSelector.value));
    });

    // Inicializa con el mes actual
    const currentDate = new Date();
    yearSelector.value = currentDate.getFullYear();
    monthSelector.value = currentDate.getMonth();
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
});

// Redirección al HTML de horarios
function redirectToSchedule() {
    window.location.href = "horarios.html";
}
