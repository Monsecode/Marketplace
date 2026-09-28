from flask import Blueprint, jsonify, request
from app.db import obtener_pedido_por_id
from app.notificaciones import enviar_correo_confirmacion

reenviar_bp = Blueprint("reenviar", __name__)

@reenviar_bp.route("/pedidos/<int:pedido_id>/reenviar-confirmacion", methods=["POST"])
def reenviar_confirmacion(pedido_id):
    """Reenvía el correo de confirmación validando la propiedad del pedido."""
    pedido = obtener_pedido_por_id(pedido_id)

    if pedido is None:
        return jsonify({"error": "pedido no encontrado"}), 404

    usuario_actual = request.json.get("usuario_solicitante") if request.is_json else None
    
    if not usuario_actual or usuario_actual != pedido.get("correo_comprador"):
        return jsonify({"error": "No autorizado para reenviar este pedido"}), 403

    enviar_correo_confirmacion(
        destinatario=pedido["correo_comprador"],
        numero_pedido=pedido["id"],
        detalle=pedido["detalle"],
    )
    return jsonify({"mensaje": f"Confirmacion reenviada para el pedido {pedido_id}"})
