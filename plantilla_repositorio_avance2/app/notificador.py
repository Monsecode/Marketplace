from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({"estado": "ok", "servicio": "notificaciones"}), 200

@app.route('/notificar', methods=['POST'])
def notificar():
    datos = request.json
    usuario = datos.get("usuario")
    mensaje = datos.get("mensaje")
    
    print("=========================================")
    print(f"ENVIANDO NOTIFICACIÓN A: {usuario}")
    print(f"MENSAJE: {mensaje}")
    print("=========================================")
    
    return jsonify({"estado": "notificacion_enviada"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
