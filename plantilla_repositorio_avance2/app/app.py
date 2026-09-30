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
        cursor = conexion.cursor()
        cursor.execute("SELECT user FROM user LIMIT 1;") # Consulta de prueba
        cursor.close()
        conexion.close()
        
        productos = [
            {"id": 1, "nombre": "Teclado Mecánico", "precio": 1200},
            {"id": 2, "nombre": "Monitor 144hz", "precio": 4500}
        ]
        return jsonify(productos), 200
    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return jsonify({"error": "Fallo la conexion a la Base de Datos RDS"}), 500

@app.route('/comprar', methods=['POST'])
def comprar():
    datos = request.json
    usuario = datos.get("usuario")
    producto_id = datos.get("producto_id")

    if not usuario or not producto_id:
        return jsonify({"error": "Falta usuario o producto"}), 400

    try:
        recibo = f"El usuario {usuario} compro el articulo {producto_id}"
        s3_client.put_object(
            Bucket=BUCKET_NAME, 
            Key=f"recibos/compra_{usuario}_{producto_id}.txt", 
            Body=recibo
        )
    except Exception as e:
        print(f"Error con S3: {e}")

    notificacion_url = os.environ.get("NOTIFICACIONES_URL", "http://notificaciones:5001/notificar")
    try:
        requests.post(notificacion_url, json={"usuario": usuario, "mensaje": f"Pedido confirmado del producto {producto_id}"})
    except Exception as e:
        print(f"Error al notificar: {e}")

    return jsonify({"mensaje": "Compra exitosa, recibo guardado en S3", "usuario": usuario}), 200


from reenviar_confirmacion import reenviar_bp
app.register_blueprint(reenviar_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
