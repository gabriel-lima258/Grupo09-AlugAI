#!/bin/bash
# Script de start para Render
# Detecta automaticamente o caminho correto

# Tentar diferentes caminhos possíveis
if [ -d "api" ]; then
    cd api && python app.py
elif [ -d "backend/api" ]; then
    cd backend/api && python app.py
else
    # Se não encontrar, tentar executar diretamente
    python api/app.py || python backend/api/app.py
fi

