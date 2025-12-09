# 🎨 Frontend AlugAI - Streamlit

Frontend desenvolvido em Streamlit para o sistema AlugAI de precificação de aluguel de imóveis no Distrito Federal.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Execução](#execução)
- [Funcionalidades](#funcionalidades)
- [Integração com Backend](#integração-com-backend)
- [Deploy](#deploy)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O frontend AlugAI é uma aplicação web interativa construída com Streamlit que permite:

- **Estimar preços** de aluguel usando modelo de ML
- **Buscar imóveis** do dataset treinado
- **Comparar preços** por região
- **Visualizar histórico** de consultas
- **Interface moderna** e responsiva

---

## 📁 Estrutura do Projeto

```
frontend/
├── app.py                      # Aplicação principal (página inicial)
├── pages/                       # Páginas do aplicativo
│   ├── __init__.py
│   ├── estimativa_preco.py     # Estimativa de preço com ML
│   ├── buscar_imoveis.py       # Busca e listagem de imóveis
│   ├── comparativo_regional.py # Comparativo de preços por região
│   ├── historico.py            # Histórico de consultas
│   └── sobre.py                # Sobre o projeto
├── utils/                       # Utilitários
│   ├── __init__.py
│   ├── config.py               # Configurações (CSS, página)
│   └── helpers.py              # Funções auxiliares
├── requirements.txt            # Dependências Python
├── run.sh                      # Script de execução (Linux/Mac)
├── run.bat                     # Script de execução (Windows)
└── README.md                   # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Navegue até o diretório do frontend:**
   ```bash
   cd frontend
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Execução

### Método 1: Streamlit CLI (Recomendado)

```bash
cd frontend
streamlit run app.py
```

### Método 2: Scripts de Execução

**Linux/Mac:**
```bash
cd frontend
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
cd frontend
run.bat
```

### Acessar a Aplicação

Após executar, a aplicação estará disponível em:

- **URL Local**: `http://localhost:8501`
- O navegador abrirá automaticamente

---

## 🎯 Funcionalidades

### 1. Página Inicial (`app.py`)

- Apresentação do projeto
- Navegação para outras páginas
- Estatísticas gerais

### 2. Estimativa de Preço (`pages/estimativa_preco.py`)

**Funcionalidades:**
- Formulário completo para entrada de dados do imóvel
- Integração com API de predição
- Exibição de preço estimado e preço por m²
- Visualização gráfica (Plotly)
- Histórico de consultas

**Campos do Formulário:**
- Tipo de imóvel
- Bairro
- Área (m²)
- Número de quartos
- Número de banheiros
- Vagas de garagem
- Condomínio (R$)
- Mobiliado (Sim/Não)

### 3. Buscar Imóveis (`pages/buscar_imoveis.py`)

**Funcionalidades:**
- Carrega todos os imóveis do dataset treinado
- Filtros opcionais:
  - Tipo de imóvel
  - Bairro
  - Área (min/max)
  - Número de quartos
  - Preço (min/max)
- Paginação (10 imóveis por página)
- Classificação automática de custo-benefício
- Botão para obter estimativa de preço do modelo
- Favoritar imóveis

### 4. Comparativo Regional (`pages/comparativo_regional.py`)

**Funcionalidades:**
- Comparação de preços por região
- Visualizações interativas (Plotly)
- Gráficos de distribuição de preços
- Análise por tipo de imóvel

### 5. Histórico (`pages/historico.py`)

**Funcionalidades:**
- Lista de consultas anteriores
- Filtros por data e tipo
- Exportação de dados

### 6. Sobre (`pages/sobre.py`)

**Funcionalidades:**
- Informações sobre o projeto
- Equipe de desenvolvimento
- Tecnologias utilizadas

---

## 🔗 Integração com Backend

### Configuração da URL da API

O frontend usa variável de ambiente para configurar a URL do backend:

**Localmente:**
```python
API_URL = os.getenv('API_URL', 'http://localhost:5020')
```

**Em produção (Streamlit Cloud):**
Configure nos Secrets:
```toml
API_URL = "https://alugai.onrender.com"
```

### Endpoints Utilizados

1. **`POST /predict`**: Predição de preço
2. **`GET /data/unique-values`**: Valores únicos (cidades, bairros, tipos)
3. **`GET /data/properties`**: Lista de imóveis com filtros
4. **`GET /data/cities`**: Lista de cidades
5. **`GET /data/neighborhoods`**: Lista de bairros
6. **`GET /data/property-types`**: Lista de tipos de imóveis

### Exemplo de Uso

```python
import requests
import os

API_URL = os.getenv('API_URL', 'http://localhost:5020')

# Predição
response = requests.post(f"{API_URL}/predict", json={
    'area': 70,
    'bedrooms': 2,
    'bathrooms': 2,
    'parking_spaces': 1,
    'furnished': False,
    'hoa': 400,
    'property_type': 'Apartamento',
    'city': 'Brasília',
    'neighborhood': 'asa norte',
    'suites': 0
})

if response.status_code == 200:
    result = response.json()
    predicted_price = result['predicted_price']
else:
    # Fallback ou tratamento de erro
    pass
```

---

## 🚀 Deploy

### Streamlit Cloud (Recomendado)

1. **Acesse:** https://streamlit.io/cloud
2. **Faça login** com GitHub
3. **Clique em:** "New app"
4. **Configure:**
   - **Repository**: Seu repositório GitHub
   - **Branch**: `main` (ou `master`)
   - **Main file path**: `frontend/app.py` ⭐
   - **App name**: `alugai` (ou outro nome)
5. **Clique em:** "Deploy"
6. **Configure Secrets:**
   - Vá em "Settings" → "Secrets"
   - Adicione:
     ```toml
     API_URL = "https://alugai.onrender.com"
     ```
   - (Substitua pela URL do seu backend)

### Verificar Deploy

1. Acesse a URL do app (ex: `https://alugai.streamlit.app`)
2. Teste uma predição
3. Verifique se conecta ao backend

---

## 🎨 Personalização

### CSS Customizado

O CSS customizado está em `utils/config.py`. Você pode modificar:

- Cores do tema
- Estilos de componentes
- Layout geral

### Configurações do Streamlit

Crie/edite `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = true

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## 🧪 Testes

### Testar Localmente

1. **Inicie o backend:**
   ```bash
   cd backend/api
   python app.py
   ```

2. **Inicie o frontend:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. **Teste as funcionalidades:**
   - Estimativa de preço
   - Busca de imóveis
   - Comparativo regional

---

## 🔍 Troubleshooting

### Erro: "Não foi possível conectar à API"

**Solução:**
1. Verifique se o backend está rodando
2. Confirme a URL da API (local ou deploy)
3. Verifique CORS no backend
4. Teste a URL diretamente:
   ```bash
   curl http://localhost:5020/health
   ```

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install -r requirements.txt
```

### Página não carrega

**Solução:**
1. Verifique os logs do Streamlit
2. Confirme que `app.py` está no caminho correto
3. Verifique se todas as dependências estão instaladas

### Dropdowns vazios

**Solução:**
1. Verifique se o backend está respondendo
2. Teste o endpoint `/data/unique-values`
3. Verifique os logs do frontend

### Erro de CORS

**Solução:**
1. Confirme que o backend tem CORS configurado
2. Verifique se o domínio do frontend está permitido
3. Para local: `http://localhost:8501`
4. Para Streamlit Cloud: `https://*.streamlit.app`

---

## 📚 Dependências

- `streamlit>=1.28.0`: Framework web
- `pandas>=2.0.0`: Manipulação de dados
- `plotly>=5.17.0`: Visualizações interativas
- `numpy>=1.24.0`: Operações numéricas
- `requests>=2.31.0`: Cliente HTTP para API

---

## 🎨 Tecnologias Utilizadas

- **Streamlit**: Framework para aplicações web em Python
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Gráficos interativos
- **NumPy**: Operações numéricas
- **Requests**: Comunicação HTTP com a API

---

## 📝 Notas Importantes

- O histórico é armazenado em sessão (não persistente entre reinicializações)
- Os dados são carregados dinamicamente do backend
- O frontend funciona offline apenas para visualização (sem predições)
- CORS está configurado para permitir requisições do Streamlit Cloud

---

## 👥 Desenvolvido por

Equipe AlugAI - UnB 2025

---

## 📄 Licença

Este projeto é de uso acadêmico e educacional.
