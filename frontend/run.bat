@echo off
REM Script para executar o frontend AlugAI no Windows

echo 🏠 Iniciando AlugAI Frontend...
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

REM Verificar se o Streamlit está instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependências...
    pip install -r requirements.txt
)

REM Executar o aplicativo
echo 🚀 Iniciando aplicativo Streamlit...
echo 📱 Acesse: http://localhost:8501
echo.

streamlit run app.py

pause




