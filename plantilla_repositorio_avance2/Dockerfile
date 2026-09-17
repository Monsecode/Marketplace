# 1. Versión fija de la imagen base
FROM python:3.9-slim

# Evitar crear archivos basura de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. Crear usuario sin privilegios (no root)
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Instalar curl para que funcione el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias primero (optimización de caché)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY app/ .

# Darle los permisos al usuario que creamos
RUN chown -R appuser:appuser /app

# 3. Usar el usuario no root
USER appuser

# 4. HEALTHCHECK apuntando al endpoint /salud
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-5000}/salud || exit 1

# Por defecto levanta la API, pero docker-compose lo puede cambiar
CMD ["python", "app.py"]
