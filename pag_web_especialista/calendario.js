document.addEventListener("DOMContentLoaded", () => {
    const yearSelector = document.getElementById("year-selector");
    const monthSelector = document.getElementById("month-selector");
    const calendarGrid = document.querySelector(".calendar-grid");

    let horarios = {}; // Aquí se guardarán los horarios traídos de la API

    const fetchHorarios = async () => {
        try {
            const response = await fetch("/api/horarios");
            horarios = await response.json();
        } catch (error) {
            console.error("Error al obtener los horarios:", error);
        }
    };

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

        // Agrega días del mes con horarios
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement("div");
            dayCell.classList.add("day-cell");
            dayCell.textContent = day;

            const fecha = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
            if (horarios[fecha]) {
                const horariosList = document.createElement("ul");
                horariosList.classList.add("horarios-list");

                horarios[fecha].forEach(horario => {
                    const horarioItem = document.createElement("li");
                    horarioItem.textContent = `${horario.hora} - ${horario.paciente}`;
                    horariosList.appendChild(horarioItem);
                });

                dayCell.appendChild(horariosList);
            }

            calendarGrid.appendChild(dayCell);
        }
    };

    // Población de selectores
    for (let year = 2024; year <= 3000; year++) {
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

    // Inicializa el calendario
    const initCalendar = async () => {
        await fetchHorarios(); // Obtiene los horarios antes de generar el calendario
        const currentDate = new Date();
        yearSelector.value = currentDate.getFullYear();
        monthSelector.value = currentDate.getMonth();
        generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
    };

    initCalendar();
});

