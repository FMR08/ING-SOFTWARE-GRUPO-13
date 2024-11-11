
CREATE TABLE Paciente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimento DATE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    rut VARCHAR(20) UNIQUE NOT NULL,
);

CREATE TABLE Medico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    rut VARCHAR(20) UNIQUE NOT NULL,
);

CREATE TABLE CITA(
    id SERIAL PRIMARY KEY,
    paciente_id INT REFERENCES Paciente(id), // Paciente que asiste a la cita
    medico_id INT REFERENCES Medico(id), // Medico que atiende la cita
    fecha DATE NOT NULL, // Fecha de la cita
    hora TIME NOT NULL, // Hora de la cita
    descripcion TEXT // Descripcion de la cita
);