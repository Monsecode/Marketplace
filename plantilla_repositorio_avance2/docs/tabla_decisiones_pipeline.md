# Tabla de decisiones de mi pipeline

## Riesgos que introduce MI aplicacion
| # | Riesgo concreto de mi app | Que control lo cubre | Por que ese control |
|---|---|---|---|
| 1 | Uso de librerías desactualizadas con fallos. | Escaneo de dependencias (Trivy). | Previene ejecución de código malicioso. |
| 2 | Credenciales de AWS expuestas. | Escaneo de secretos (Trivy). | Evita robo de cuentas. |

## Mis etapas y sus umbrales
| Etapa | Herramienta | Que revisa | Umbral que bloquea | Por que ese umbral |
|---|---|---|---|---|
| Seguridad | Trivy | Vulnerabilidades en código | HIGH, CRITICAL | Para bloquear solo lo urgente. |

## Lo que decidi NO cubrir
| Riesgo que dejo fuera | Por que lo dejo fuera | Que haria si tuviera mas tiempo |
|---|---|---|
| Calidad del código (SAST) | Falta de tiempo. | Integrar SonarQube. |
