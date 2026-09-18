# Markcode

> Avance 2 del Reto - LSCA2314 - Periodo AD26
> Alumno: Carolina Hermosillo   |   Matricula: AL02938037   |   Tema elegido: MarketPlace

## Que hace esta aplicacion
Es una API de marketplace contenerizada y segura en la que resuelve la necesidad de gestionar usuarios y productos integrando un escaneo de seguridad automático en su código para así prevenir el despliegue de vulnerabilidades

## Como se levanta

```bash
cp .env.ejemplo .env     # y llena tus valores
docker compose up --build
```

La aplicacion queda en http://localhost:5000 y su endpoint de salud
responde en /salud.

## Arquitectura

La aplicación está contenerizada en Docker, usando servicios para la API y notificaciones. Estos servicios se conectan de forma segura a una base de datos MySQL en AWS RDS para guardar la información, y utilizan un bucket de AWS S3 para almacenar archivos. Toda la infraestructura se gestiona como código y es validada por un pipeline de seguridad

Ver el diagrama en `docs/diagrama_arquitectura.png`.

## Servicios de AWS que usa

| Servicio | Para que lo uso | Como lo asegure |
|---|---|---|
| S3 | Almacenamiento de imágenes y archivos del marketplace. | Cifrado SSE-S3 habilitado y bloqueo de acceso público (Block Public Access) activo. |
| RDS| Base de datos relacional (MySQL) para persistencia de datos. | Cifrado en reposo (KMS), configurado sin acceso público y protegido por un Security Group estricto. |

## Requisitos minimos del tema

| Requisito de mi tema | Donde se cumple |
|---|---|
| Escaneo de vulnerabilidades y generación de SBOM | En el pipeline automatizado usando Trivy para bloquear despliegues inseguros |

## Como se corre el pipeline

```bash
./pipeline/escaneo_seguridad.sh
```
