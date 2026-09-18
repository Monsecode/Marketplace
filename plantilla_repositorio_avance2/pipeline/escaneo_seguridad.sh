#!/bin/bash
echo "Escaneando el proyecto en busca de vulnerabilidades y secretos..."
trivy fs --scanners secret,vuln --exit-code 1 --severity CRITICAL,HIGH .
