# servidor_vulnerable.py
# Requiere: pip install flask requests
# -------------------------------------------------------------------
# Servidor VULNERABLE a SSRF.
# Toma una URL del usuario y la consulta SIN validar el destino.
# Basado en el codigo visto en clase.
# -------------------------------------------------------------------
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/fetch')
def fetch_url():
    # RIESGO: la URL viene directamente del parametro del usuario.
    #         No se valida si apunta a recursos internos.
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Falta el parametro ?url="}), 400

    try:
        # RIESGO: el servidor realiza la peticion SIN verificar el destino.
        resp = requests.get(url, timeout=5)
        # RIESGO: se devuelve el contenido completo al atacante.
        return jsonify({
            "status_code": resp.status_code,
            "body": resp.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return '''
    <h2>SSRF Vulnerable Demo</h2>
    <p>Esta app pide una URL y el servidor la consulta por ti.</p>
    <p>Uso normal (externo, legitimo):</p>
    <ul>
        <li><a href="/fetch?url=https://httpbin.org/get">/fetch?url=https://httpbin.org/get</a></li>
    </ul>
    <p>Ataque SSRF (alcanzar el servicio interno secreto que corre en el puerto 8000):</p>
    <ul>
        <li><a href="/fetch?url=http://127.0.0.1:8000/secreto">/fetch?url=http://127.0.0.1:8000/secreto</a></li>
    </ul>
    '''


if __name__ == '__main__':
    print("Servidor VULNERABLE corriendo en http://127.0.0.1:5000")
    print("Prueba el ataque en: http://127.0.0.1:5000/fetch?url=http://127.0.0.1:8000/secreto")
    app.run(host='127.0.0.1', port=5000, debug=True)
