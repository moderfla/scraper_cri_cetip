#!/bin/bash
set -euo pipefail

API_URL="https://sistemaswebb3-balcao.b3.com.br/featuresCRIProxy/CriCall/GetDownload"
OUTPUT_FILE="emissoes_cri.csv"

# Criar arquivo temporário
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

echo "Fazendo requisição para API da B3..."

# Fazer download com verificação de erro HTTP
HTTP_CODE=$(curl -sSL --compressed -w "%{http_code}" \
    -H "Accept: application/octet-stream" \
    -H "Content-Type: application/json" \
    -H "Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7" \
    -H "Referer: https://sistemaswebb3-balcao.b3.com.br/" \
    -H "User-Agent: Mozilla/5.0 (compatible; Scraper/1.0)" \
    -o "$TEMP_FILE" \
    "$API_URL")

if [ "$HTTP_CODE" != "200" ]; then
    echo "Erro: API retornou HTTP $HTTP_CODE" >&2
    echo "Conteúdo da resposta:" >&2
    head -c 500 "$TEMP_FILE" >&2
    exit 1
fi

# Verificar se o arquivo tem conteúdo
if [ ! -s "$TEMP_FILE" ]; then
    echo "Erro: resposta vazia da API" >&2
    exit 1
fi

echo "Decodificando base64..."
# Decodificar base64 para arquivo temporário CSV
TEMP_CSV=$(mktemp)
trap "rm -f $TEMP_FILE $TEMP_CSV" EXIT

if ! base64 -d "$TEMP_FILE" > "$TEMP_CSV" 2>/dev/null; then
    echo "Erro: conteúdo não é base64 válido" >&2
    echo "Conteúdo recebido (primeiros 500 chars):" >&2
    head -c 500 "$TEMP_FILE" >&2
    exit 1
fi

echo "Convertendo delimitador ; para vírgula..."
# Converter ISO-8859-1 -> UTF-8, remover coluna 13, e trocar ; por ,
iconv -f ISO-8859-1 -t UTF-8 "$TEMP_CSV" | \
    cut -d';' -f1-12 | \
    sed 's/;/,/g' > "$OUTPUT_FILE"

echo "OK: Arquivo '$OUTPUT_FILE' gerado com sucesso"
