# ADR-001: Decisiones tecnicas de Marketplace API
Fecha: 17/09/2026 | Estado: Aceptada

## Contexto
Se requiere construir una API de marketplace contenerizada en AWS usando S3 para imágenes y RDS para base de datos, asegurando la infraestructura con un pipeline DevSecOps.

## Decisiones

### 1. Framework del backend
Elegi: Flask / FastAPI
Por que: Es ligero y fácil de implementar para APIs rápidas.
Que descarte y por que: Django, por ser demasiado monolítico y pesado.

### 2. Separacion en servicios
Elegi: Dos contenedores (API y Notificador).
Por que: Separa la lógica principal del envío de notificaciones.
Que descarte y por que: Un solo contenedor, para evitar malas prácticas.

### 3. Almacenamiento
Elegi: S3 para archivos y RDS para base de datos.
Por que: Aprovecha servicios administrados seguros y separables de AWS.
Que descarte y por que: Bases de datos locales en contenedores, por volatilidad.

## Consecuencias
Facilitó la integración, pero complicó la gestión inicial de redes y accesos.
