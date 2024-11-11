from website import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Crea todas las tablas definidas en los modelos