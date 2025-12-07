# app.py
from routes.rutas import app

# Opcional, solo para correr local con `python app.py`
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Para evitar DB locks y se levanten 2 procesos (reloader y app)
