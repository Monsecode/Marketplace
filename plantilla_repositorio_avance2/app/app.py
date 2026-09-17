from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

CATALOGO = [
    {"id": 1, "nombre": "Teclado Mecánico", "precio": 1200},
    {"id": 2, "nombre": "Monitor 144hz", "precio": 4500}
]

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({"estado": "ok", "servicio": "marketplace-api"}), 200

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(CATALOGO), 200

@app.route('/comprar', methods=['POST'])
def comprar():
    datos = request.json
    usuario = datos.get("usuario")
    producto_id = datos.get("producto_id")
    
    if not usuario or not producto_id:
        return jsonify({"error": "Falta usuario o producto"}), 400

    notificacion_url = os.environ.get("NOTIFICACIONES_URL", "http://notificaciones:5001/notificar")
    try:
        requests.post(notificacion_url, json={"usuario": usuario, "mensaje": f"Pedido confirmado del producto {producto_id}"})
    except Exception as e:
        print(f"Error al notificar: {e}")

    return jsonify({"mensaje": "Compra exitosa", "usuario": usuario}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
