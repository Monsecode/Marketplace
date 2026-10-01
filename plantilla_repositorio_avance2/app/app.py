from flask import Flask, request, jsonify
import os
import requests
import mysql.connector
import boto3

app = Flask(__name__)

s3_client = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = os.environ.get("S3_BUCKET")

def obtener_conexion_bd():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD"),
        database="mysql"
    )

@app.route('/', methods=['GET'])
def index():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markcode - Tu Tienda de Tecnología</title>
        <style>
            body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #2c3e50; }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { margin: 0; font-size: 2.2rem; color: #1a252f; }
            .header p { color: #7f8c8d; font-size: 1.1rem; margin-top: 5px; }
            .card { background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); padding: 25px; text-align: center; border: 1px solid #e1e8ed; }
            .btn { background-color: #3498db; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 1rem; font-weight: bold; width: 100%; transition: 0.2s;}
            .btn:hover { background-color: #2980b9; }
            .btn-success { background-color: #2ecc71; }
            .btn-success:hover { background-color: #27ae60; }
            input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #bdc3c7; border-radius: 5px; }
            #login-section { max-width: 350px; margin: 50px auto; }
            #app-section { display: none; max-width: 1000px; margin: auto; }
            .layout { display: flex; gap: 20px; flex-wrap: wrap; justify-content: space-between;}
            .catalog { display: flex; gap: 15px; flex-wrap: wrap; flex: 2; }
            .item-card { background: white; padding: 20px; border-radius: 8px; width: 220px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #ecf0f1;}
            .cart-section { flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); min-width: 250px; border: 1px solid #ecf0f1; height: fit-content;}
            .cart-item { display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; font-size: 0.9rem;}
            #notificacion { display: none; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Tienda Markcode</h1>
            <p>La mejor tecnología a tu alcance</p>
        </div>

        <!-- LOGIN -->
        <div id="login-section" class="card">
            <h3 style="margin-top:0;">Bienvenido</h3>
            <input type="text" id="user" placeholder="Usuario" value="admin">
            <input type="password" id="pass" placeholder="Contraseña" value="admin123">
            <button class="btn" onclick="hacerLogin()">Iniciar Sesión</button>
            <p id="login-error" style="color:#e74c3c; display:none; font-size: 14px;">Usuario o contraseña incorrectos</p>
        </div>

        <!-- APP PRINCIPAL -->
        <div id="app-section">
            <div id="notificacion"></div>
            
            <div class="layout">
                <!-- CATÁLOGO -->
                <div class="catalog" id="catalog">
                    <p style="color:#7f8c8d;">Cargando productos...</p>
                </div>
                
                <!-- CARRITO LATERAL -->
                <div class="cart-section">
                    <h3 style="margin-top:0;">Tu Carrito 🛒</h3>
                    <div id="cart-items">
                        <p style="color:#95a5a6; font-size: 14px; text-align:center;">El carrito está vacío</p>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold; margin-bottom: 15px;">
                        <span>Total:</span>
                        <span id="cart-total">$0 MXN</span>
                    </div>
                    <button class="btn btn-success" id="btn-pagar" style="display:none;" onclick="procesarPago()">Proceder al Pago</button>
                </div>
            </div>
        </div>
        
        <script>
            let authToken = '';
            let carrito = [];
            let catalogoDatos = [];

            async function hacerLogin() {
                const u = document.getElementById('user').value;
                const p = document.getElementById('pass').value;
                
                try {
                    const res = await fetch('/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({usuario: u, password: p})
                    });
                    const data = await res.json();
                    
                    if(res.ok) {
                        authToken = data.token;
                        document.getElementById('login-section').style.display = 'none';
                        document.getElementById('app-section').style.display = 'block';
                        cargarCatalogo();
                    } else {
                        document.getElementById('login-error').style.display = 'block';
                    }
                } catch(e) {
                    alert("Error de conexión");
                }
            }

            function cargarCatalogo() {
                fetch('/productos')
                    .then(res => res.json())
                    .then(data => {
                        catalogoDatos = data;
                        const catalog = document.getElementById('catalog');
                        catalog.innerHTML = '';
                        data.forEach(p => {
                            catalog.innerHTML += `
                                <div class="item-card">
                                    <h4 style="margin: 0 0 10px 0;">${p.nombre}</h4>
                                    <h2 style="color: #27ae60; margin: 0 0 15px 0;">$${p.precio}</h2>
                                    <button class="btn" onclick="agregarAlCarrito(${p.id})">Agregar al Carrito</button>
                                </div>
                            `;
                        });
                    });
            }

            function agregarAlCarrito(id) {
                const producto = catalogoDatos.find(p => p.id === id);
                carrito.push(producto);
                actualizarVistaCarrito();
            }

            function actualizarVistaCarrito() {
                const contenedor = document.getElementById('cart-items');
                const btnPagar = document.getElementById('btn-pagar');
                const totalText = document.getElementById('cart-total');
                
                if (carrito.length === 0) return;

                contenedor.innerHTML = '';
                let total = 0;
                
                carrito.forEach(p => {
                    total += p.precio;
                    contenedor.innerHTML += `
                        <div class="cart-item">
                            <span>${p.nombre}</span>
                            <strong>$${p.precio}</strong>
                        </div>
                    `;
                });
                
                totalText.innerText = `$${total} MXN`;
                btnPagar.style.display = 'block';
            }

            async function procesarPago() {
                if(carrito.length === 0) return;
                
                const notif = document.getElementById('notificacion');
                notif.style.display = 'block';
                notif.style.background = '#f1c40f';
                notif.style.color = '#333';
                notif.innerHTML = 'Procesando pago de forma segura...';
                
                // Tomamos el primer ID del carrito para la simulación del backend
                const producto_id_a_comprar = carrito[0].id;

                try {
                    const res = await fetch('/comprar', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': authToken
                        },
                        body: JSON.stringify({ producto_id: producto_id_a_comprar })
                    });
                    const data = await res.json();
                    
                    if(res.ok) {
                        notif.style.background = '#d4edda';
                        notif.style.color = '#155724';
                        notif.innerHTML = `✅ ¡Gracias por tu compra! Tu pedido ha sido confirmado y pronto recibirás un correo con tu recibo.`;
                        carrito = [];
                        actualizarVistaCarrito();
                        document.getElementById('cart-items').innerHTML = '<p style="color:#95a5a6; font-size: 14px; text-align:center;">El carrito está vacío</p>';
                        document.getElementById('cart-total').innerText = '$0 MXN';
                        document.getElementById('btn-pagar').style.display = 'none';
                    } else {
                        throw new Error(data.error);
                    }
                } catch(e) {
                    notif.style.background = '#f8d7da';
                    notif.style.color = '#721c24';
                    notif.innerHTML = '❌ Error al procesar el pago. Intenta nuevamente.';
                }
            }
        </script>
    </body>
    </html>
    """
    return html

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({"estado": "ok", "servicio": "marketplace-api"}), 200

@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    usuario = datos.get("usuario")
    password = datos.get("password")
    if usuario == "admin" and password == "admin123":
        return jsonify({"mensaje": "Login exitoso", "token": "token-valido-123"}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        conexion = obtener_conexion_bd()
        cursor = conexion.cursor(buffered=True)
        cursor.execute("SELECT user FROM user LIMIT 1;")
        cursor.close()
        conexion.close()
        
        productos = [
            {"id": 1, "nombre": "Teclado Mecánico", "precio": 1200},
            {"id": 2, "nombre": "Monitor 144hz", "precio": 4500}
        ]
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": "Fallo la conexion a la Base de Datos RDS"}), 500

@app.route('/comprar', methods=['POST'])
def comprar():
    token = request.headers.get("Authorization")
    if token != "token-valido-123":
        return jsonify({"error": "Acceso denegado. Token invalido o ausente."}), 401
    
    datos = request.json
    producto_id = datos.get("producto_id")
    usuario = "admin"
    if not producto_id:
        return jsonify({"error": "Falta producto_id"}), 400
        
    try:
        recibo = f"El usuario {usuario} compro el articulo {producto_id}"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"recibos/compra_{usuario}_{producto_id}.txt",
            Body=recibo
        )
    except Exception as e:
        pass
        
    notificacion_url = os.environ.get("NOTIFICACIONES_URL", "http://notificaciones:5001/notificar")
    try:
        requests.post(notificacion_url, json={"usuario": usuario, "mensaje": f"Pedido confirmado del producto {producto_id}"})
    except Exception as e:
        pass
        
    return jsonify({"mensaje": "Compra exitosa", "usuario": usuario}), 200

from reenviar_confirmacion import reenviar_bp
app.register_blueprint(reenviar_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
