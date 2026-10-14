# servicio_interno.py
# -------------------------------------------------------------------
# Simula un servicio INTERNO que NUNCA deberia ser accesible desde afuera.
# En el mundo real esto seria, por ejemplo:
#   - el endpoint de metadatos de la nube (http://169.254.169.254) que
#     guarda credenciales de AWS/Google, o
#   - un panel de administracion interno.
# Aqui es el "tesoro" que el atacante quiere robar usando el SSRF.
# -------------------------------------------------------------------
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Servicio interno. No deberias poder ver esto desde fuera de la red."


@app.route('/secreto')
def secreto():
    # Datos sensibles SIMULADOS (no son reales, es solo para la demostracion).
    return jsonify({
        "servicio": "metadata-interna",
        "usuario_admin": "root",
        "token_secreto": "AKIA-FAKE-1234567890-SSRF-DEMO",
        "nota": "Si ves esto desde el navegador via /fetch, el SSRF funciono."
    })


if __name__ == '__main__':
    print("Servicio INTERNO corriendo en http://127.0.0.1:8000")
    print("Representa un recurso privado que NO deberia ser accesible desde fuera.")
    app.run(host='127.0.0.1', port=8000)
