import sys
import os

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import create_app  # Importa después de ajustar el sys.path

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)