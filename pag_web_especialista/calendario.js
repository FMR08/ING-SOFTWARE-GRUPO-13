document.addEventListener("DOMContentLoaded", () => {
    const yearSelector = document.getElementById("year-selector");
    const monthSelector = document.getElementById("month-selector");
    const calendarGrid = document.querySelector(".calendar-grid");

    let horarios = {}; // Aquí se guardarán los horarios traídos de la API

    const fetchHorarios = async () => {
        try {
            console.log("Obteniendo horarios...");
            const response = await fetch("/api/horarios");
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Horarios recibidos:", data);
            horarios = data;
        } catch (error) {
            console.error("Error al obtener los horarios:", error);
            horarios = {};
        }
    };

    const generateCalendar = (year, month) => {
        console.log("Generando calendario para:", year, month);
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
            emptyCell.classList.add("day-cell", "empty");
            calendarGrid.appendChild(emptyCell);
        }

        // Agrega días del mes con horarios
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement("div");
            dayCell.classList.add("day-cell");
            
            // Contenedor para el número del día
            const dayNumber = document.createElement("div");
            dayNumber.classList.add("day-number");
            dayNumber.textContent = day;
            dayCell.appendChild(dayNumber);

            // Verificar si hay citas para este día
            const fecha = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
            console.log("Verificando fecha:", fecha);
            
            if (horarios[fecha] && horarios[fecha].length > 0) {
                console.log("Citas encontradas para", fecha, ":", horarios[fecha]);
                const citasList = document.createElement("div");
                citasList.classList.add("citas-list");

                horarios[fecha].forEach(cita => {
                    const citaItem = document.createElement("div");
                    citaItem.classList.add("cita-item");
                    citaItem.textContent = `${cita.hora} - ${cita.paciente}`;
                    citasList.appendChild(citaItem);
                });

                dayCell.appendChild(citasList);
            }

            calendarGrid.appendChild(dayCell);
        }
    };

    // Población de selectores
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year <= currentYear + 5; year++) {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearSelector.appendChild(option);
    }

    for (let month = 0; month < 12; month++) {
        const option = document.createElement("option");
        option.value = month;
        option.textContent = new Date(2000, month).toLocaleString("es", { month: "long" });
        monthSelector.appendChild(option);
    }

    // Eventos para cambiar mes/año
    yearSelector.addEventListener("change", async () => {
        await fetchHorarios();
        generateCalendar(parseInt(yearSelector.value), parseInt(monthSelector.value));
    });

    monthSelector.addEventListener("change", async () => {
        await fetchHorarios();
        generateCalendar(parseInt(yearSelector.value), parseInt(monthSelector.value));
    });

    // Inicializa el calendario
    const initCalendar = async () => {
        console.log("Inicializando calendario...");
        await fetchHorarios();
        const currentDate = new Date();
        yearSelector.value = currentDate.getFullYear();
        monthSelector.value = currentDate.getMonth();
        generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
    };

    initCalendar();
});

