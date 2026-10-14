# servidor_mitigado.py
# Requiere: pip install flask requests
# -------------------------------------------------------------------
# Servidor PROTEGIDO contra SSRF.
# Antes de consultar la URL, valida que NO apunte a un recurso interno.
# Basado en el codigo corregido visto en clase.
# -------------------------------------------------------------------
import socket
import ipaddress
from urllib.parse import urlparse
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def is_safe_url(url):
    """Devuelve True solo si la URL es segura (no apunta a recursos internos)."""
    parsed = urlparse(url)

    # 1. Solo se permiten los esquemas http y https.
    if parsed.scheme not in ['http', 'https']:
        return False

    try:
        hostname = parsed.hostname
        if not hostname:
            return False

        # 2. Se resuelve el nombre de dominio a una direccion IP real.
        ip = socket.gethostbyname(hostname)

        # 3. Se bloquea si la IP es privada, loopback (127.x.x.x) o reservada.
        #    Asi se cierra el acceso a la red interna y a los metadatos de la nube.
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return False

        return True
    except Exception:
        # Si falla la resolucion DNS o el formato es invalido, se bloquea por seguridad.
        return False


@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Falta el parametro ?url="}), 400

    # VALIDACION DE SEGURIDAD: aqui es donde se corta el SSRF.
    if not is_safe_url(url):
        return jsonify({"error": "URL no permitida - acceso a recursos internos bloqueado"}), 403

    try:
        resp = requests.get(url, timeout=5)
        return jsonify({
            "status_code": resp.status_code,
            "body": resp.text[:1000]  # Se limita el tamano de la respuesta.
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return '''
    <h2>SSRF Secure Demo (Protegido)</h2>
    <p>Misma app, pero ahora valida el destino antes de consultar.</p>
    <p>Uso normal (externo, permitido):</p>
    <ul>
        <li><a href="/fetch?url=https://httpbin.org/get">/fetch?url=https://httpbin.org/get</a></li>
    </ul>
    <p>Intento de ataque SSRF (ahora BLOQUEADO):</p>
    <ul>
        <li><a href="/fetch?url=http://127.0.0.1:8000/secreto">/fetch?url=http://127.0.0.1:8000/secreto</a> (interno, bloqueado)</li>
        <li><a href="/fetch?url=http://169.254.169.254/latest/meta-data/">/fetch?url=http://169.254.169.254/latest/meta-data/</a> (metadatos de nube, bloqueado)</li>
    </ul>
    '''


if __name__ == '__main__':
    print("Servidor MITIGADO corriendo en http://127.0.0.1:5001")
    print("Prueba el mismo ataque: http://127.0.0.1:5001/fetch?url=http://127.0.0.1:8000/secreto")
    print("Ahora deberia responder 403 (bloqueado).")
    app.run(host='127.0.0.1', port=5001, debug=True)
