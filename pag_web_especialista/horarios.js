document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#schedule-table tbody");

    // Función para cargar los datos desde un servidor
    async function loadSchedule() {
        try {
            const response = await fetch("/api/horarios"); // Cambia esta ruta según tu servidor
            const data = await response.json();

            tableBody.innerHTML = ""; // Limpia la tabla

            // Rellena la tabla con los datos
            data.forEach((entry) => {
                const row = document.createElement("tr");

                const hourCell = document.createElement("td");
                hourCell.textContent = entry.hora;

                const patientCell = document.createElement("td");
                patientCell.textContent = entry.paciente;

                const contactCell = document.createElement("td");
                contactCell.textContent = entry.contacto;

                const noteCell = document.createElement("td");
                noteCell.textContent = entry.nota;

                row.appendChild(hourCell);
                row.appendChild(patientCell);
                row.appendChild(contactCell);
                row.appendChild(noteCell);

                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error("Error cargando los datos:", error);
        }
    }

    // Cargar el horario al iniciar
    loadSchedule();
});
