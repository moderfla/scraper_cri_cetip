#!/bin/bash
set -euo pipefail

# Download e decodificação base64 direta
curl -sSL -H "Accept: application/json" \
  -H "Referer: https://sistemaswebb3-balcao.b3.com.br/" \
  "https://sistemaswebb3-balcao.b3.com.br/featuresCRIProxy/CriCall/GetDownload" | \
  base64 -d | \
  iconv -f ISO-8859-1 -t UTF-8 > emissoes_cri_raw.csv

# Remover a coluna 13 (índice 12) usando cut (mais rápido que awk para CSV simples)
# Assume que o delimitador é ; e não há ; dentro dos campos
HEADERS=$(head -1 emissoes_cri_raw.csv | cut -d';' -f1-12)
echo "$HEADERS" > emissoes_cri.csv
tail -n +2 emissoes_cri_raw.csv | cut -d';' -f1-12 >> emissoes_cri.csv

rm emissoes_cri_raw.csv
