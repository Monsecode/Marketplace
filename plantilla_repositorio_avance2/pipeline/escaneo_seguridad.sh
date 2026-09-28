#!/bin/bash
echo "Generando reportes reales de seguridad y SBOM..."

trivy fs --format table --output reportes/vulnerabilidades.txt .
trivy fs --format cyclonedx --output reportes/sbom.json .

echo "Listo, reportes guardados en la carpeta de reportes"
