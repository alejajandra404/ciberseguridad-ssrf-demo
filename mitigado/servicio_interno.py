# servicio_interno.py
# -------------------------------------------------------------------
# Identico al de la carpeta /vulnerable.
# Simula un recurso INTERNO que nunca deberia ser accesible desde afuera.
# -------------------------------------------------------------------
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Servicio interno. No deberias poder ver esto desde fuera de la red."


@app.route('/secreto')
def secreto():
    return jsonify({
        "servicio": "metadata-interna",
        "usuario_admin": "root",
        "token_secreto": "AKIA-FAKE-1234567890-SSRF-DEMO",
        "nota": "Si ves esto desde el navegador via /fetch, el SSRF funciono."
    })


if __name__ == '__main__':
    print("Servicio INTERNO corriendo en http://127.0.0.1:8000")
    app.run(host='127.0.0.1', port=8000)
