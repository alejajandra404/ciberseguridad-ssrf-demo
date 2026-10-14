# Laboratorio SSRF — Exploit y Mitigación

**Materia:** Ciberseguridad Aplicada — Ingeniería en Software (ITSON)
**Tema:** SSRF (Server-Side Request Forgery)

> Laboratorio local y seguro. Todos los servicios corren en `127.0.0.1`
> (tu propia máquina). Los datos "secretos" son inventados para la
> demostración; no se ataca ningún sistema real.

---

**Idea clave:** el atacante usa al servidor como *intermediario* para
alcanzar recursos internos (un panel de administración, la red interna, o
el endpoint de metadatos de la nube `169.254.169.254` donde se guardan
credenciales).

**Referencia OWASP:**
- `A10:2021` — SSRF tenía su propia categoría (puesto #10).
- `A01:2025` — se **fusionó dentro de Broken Access Control** (el riesgo
  #1), porque en el fondo SSRF es una falla de control de acceso: el
  servidor accede a algo que no debería.

---

## 1. Estructura del proyecto

```
ssrf-lab/
├── vulnerable/
│   ├── servicio_interno.py      # El "recurso interno secreto" (puerto 8000)
│   └── servidor_vulnerable.py   # App SIN validación (puerto 5000)
├── mitigado/
│   ├── servicio_interno.py      # Idéntico (solo necesitas correr una copia)
│   └── servidor_mitigado.py     # App CON validación (puerto 5001)
└── README.md
```

Hay **tres piezas**:
1. **Servicio interno** (puerto 8000): simula el recurso privado = el
   "tesoro" que el atacante quiere robar.
2. **Servidor vulnerable** (puerto 5000): consulta cualquier URL sin validar.
3. **Servidor mitigado** (puerto 5001): la versión corregida que valida el destino.

---

## 2. Requisitos

```
pip install flask requests
```

Necesitas Python 3. (Si `pip` no funciona, prueba `pip3`.)

---

## 3. Cómo correr la demostración en vivo

Abrir **tres terminales** en la carpeta `ssrf-lab`. En cada una corre un
servidor:

**Terminal 1 — el recurso interno secreto:**
```
python vulnerable/servicio_interno.py
```

**Terminal 2 — el servidor vulnerable:**
```
python vulnerable/servidor_vulnerable.py
```

**Terminal 3 — el servidor mitigado:**
```
python mitigado/servidor_mitigado.py
```

> Nota: el servicio interno es el mismo para ambos escenarios, por eso
> solo se corre una copia (la de la carpeta `vulnerable`).

Abrir el **navegador**. Vas a mostrar dos cosas:

### Paso A — El ataque FUNCIONA (servidor vulnerable, puerto 5000)

Pegar en el navegador:
```
http://127.0.0.1:5000/fetch?url=http://127.0.0.1:8000/secreto
```
En pantalla aparece el **token secreto del servicio interno**. El
atacante, desde afuera, acaba de leer un recurso privado usando al
servidor como intermediario. **Eso es SSRF.**

### Paso B — El ataque se BLOQUEA (servidor mitigado, puerto 5001)

Pegar el **mismo ataque**, solo cambia el puerto a 5001:
```
http://127.0.0.1:5001/fetch?url=http://127.0.0.1:8000/secreto
```
Ahora responde:
```
{"error": "URL no permitida - acceso a recursos internos bloqueado"}
```
con código **HTTP 403**. La validación cortó el ataque.

### Paso C (opcional) — El uso legítimo sigue funcionando

> ⚠️ Este paso necesita **internet**. 

```
http://127.0.0.1:5001/fetch?url=https://httpbin.org/get
```
Esto sí se permite, porque apunta a un sitio **público externo**, no a la
red interna. Demuestra que la mitigación **no rompe el uso normal**: solo
bloquea lo interno.

---

## 5. ¿Por qué es vulnerable el código?

En `servidor_vulnerable.py`, la función `fetch_url()` toma la URL del
usuario y la consulta directamente:

```python
url = request.args.get('url')      # viene del usuario, sin filtrar
resp = requests.get(url, ...)      # el servidor consulta CUALQUIER destino
return jsonify({"body": resp.text}) # y le devuelve el contenido al atacante
```

No hay ninguna verificación de **a dónde** apunta la URL. Por eso
`http://127.0.0.1:8000/secreto` (un recurso interno) se consulta sin
problema.

---

## 6. ¿Por qué la corrección elimina la vulnerabilidad?

En `servidor_mitigado.py` se agrega la función `is_safe_url()`, que se
ejecuta **antes** de consultar la URL:

1. **Solo permite esquemas `http` y `https`** (bloquea trucos como
   `file://` o `gopher://`).
2. **Resuelve el nombre de dominio a su dirección IP real.**
3. **Rechaza la petición si esa IP es privada, de loopback (`127.x.x.x`)
   o reservada.** Así se cierra el acceso a la red interna y a los
   metadatos de la nube.
4. Si algo falla (DNS inválido, formato raro), **bloquea por seguridad**
   (deny-by-default: prohibido salvo que se pruebe que es seguro).

En una frase: **se valida el destino de la petición y se denega por
defecto todo lo que apunte hacia adentro.** Eso es exactamente lo que
elimina el SSRF.
