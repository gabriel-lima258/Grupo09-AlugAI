#!/bin/bash

# Script para iniciar a API AlugAI
# Mata processos antigos e inicia uma nova instância

PORT=5020
API_DIR="/Users/sosprecatorios/Desktop/Grupo09-AlugAI/backend/api"

echo "🔄 Verificando processos antigos na porta $PORT..."

# Matar processos antigos
pkill -f "backend/api/app.py" 2>/dev/null
sleep 1

# Verificar se a porta está livre
if command -v lsof &> /dev/null; then
    PID=$(lsof -ti:$PORT 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "⚠️  Matando processo $PID na porta $PORT..."
        kill -9 $PID 2>/dev/null
        sleep 1
    fi
fi

echo "🚀 Iniciando API na porta $PORT..."
cd "$API_DIR"
python3 app.py > /tmp/api_alugai.log 2>&1 &
API_PID=$!

sleep 3

# Verificar se iniciou corretamente
if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
    echo "✅ API iniciada com sucesso!"
    echo "📍 URL: http://localhost:$PORT"
    echo "📋 PID: $API_PID"
    echo "📄 Logs: tail -f /tmp/api_alugai.log"
    echo ""
    echo "Para parar a API: kill $API_PID"
else
    echo "❌ Erro ao iniciar API. Verifique os logs:"
    tail -20 /tmp/api_alugai.log
    exit 1
fi

