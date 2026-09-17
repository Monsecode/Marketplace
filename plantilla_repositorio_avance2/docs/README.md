# [NOMBRE DE TU APLICACION]

> Avance 2 del Reto - LSCA2314 - Periodo AD26
> Alumno: Completado   |   Matricula: Completado   |   Tema elegido: Completado

## Que hace esta aplicacion

[COMPLETAR: dos o tres frases. Que problema resuelve y para quien.]

## Como se levanta

```bash
cp .env.ejemplo .env     # y llena tus valores
docker compose up --build
```

La aplicacion queda en http://localhost:Completado y su endpoint de salud
responde en /salud.

## Arquitectura

[COMPLETAR: describe en un parrafo como se comunican tus servicios.]

Ver el diagrama en `docs/diagrama_arquitectura.png`.

## Servicios de AWS que usa

| Servicio | Para que lo uso | Como lo asegure |
|---|---|---|
| S3 | Completado | [COMPLETAR: cifrado, bloqueo de acceso publico] |
| RDS | Completado | [COMPLETAR: cifrado, sin acceso publico, grupo de seguridad] |

## Requisitos minimos del tema

| Requisito de mi tema | Donde se cumple |
|---|---|
| Completado | Completado |

## Como se corre el pipeline

```bash
[COMPLETAR: el comando que corre tu pipeline]
```
