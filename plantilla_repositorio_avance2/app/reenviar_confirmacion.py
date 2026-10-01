import os
from flask import Blueprint, jsonify, request
from db import obtener_pedido_por_id
from notificaciones import enviar_correo_confirmacion

reenviar_bp = Blueprint("reenviar", __name__)

# 1. CONTENCIÓN: Bandera para mitigar el ataque inmediatamente
BANDERA_CONTENCION_ACTIVA = True

@reenviar_bp.route("/pedidos/<int:pedido_id>/reenviar-confirmacion", methods=["POST"])
def reenviar_confirmacion(pedido_id):
    # Aplicación de la contención
    if BANDERA_CONTENCION_ACTIVA:
        return jsonify({"alerta_soc": "Endpoint deshabilitado temporalmente por incidente de seguridad (Contencion Activa)"}), 503

    pedido = obtener_pedido_por_id(pedido_id)
    if pedido is None:
        return jsonify({"error": "pedido no encontrado"}), 404

    # 2. REMEDIACIÓN: Validar la sesión del usuario mediante Token de Autorización, NO mediante el cuerpo del request
    token_sesion = request.headers.get("Authorization")
    
    if not token_sesion or token_sesion != "token-valido-123":
        return jsonify({"error": "Acceso denegado: Token de sesion invalido o ausente. Peticion rechazada."}), 403

    enviar_correo_confirmacion(
        destinatario=pedido["correo_comprador"],
        numero_pedido=pedido["id"],
        detalle=pedido["detalle"],
    )
    return jsonify({"mensaje": "Confirmacion reenviada de forma segura"})
