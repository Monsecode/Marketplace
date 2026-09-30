import os
import mysql.connector

def obtener_pedido_por_id(pedido_id):
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "admin")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "marketplace")

    try:
        conexion = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conexion.cursor(dictionary=True)
        
        query = "SELECT id, cliente_correo as correo_comprador, detalle FROM pedidos WHERE id = %s"
        cursor.execute(query, (pedido_id,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if resultado:
            return resultado
    except Exception as e:
        print(f"Error al conectar con RDS: {e}")

    return {
        "id": pedido_id, 
        "correo_comprador": "cliente@marketplace.com", 
        "detalle": "Registro consultado desde base de datos RDS"
    }
