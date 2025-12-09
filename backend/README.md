# 🚀 Backend AlugAI - Machine Learning API

Backend de Machine Learning para o sistema AlugAI, responsável pelo treinamento e serviço do modelo de predição de preços de aluguel de imóveis no Distrito Federal.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Treinamento do Modelo](#treinamento-do-modelo)
- [API REST](#api-rest)
- [Processamento de Dados](#processamento-de-dados)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [Deploy](#deploy)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O backend AlugAI é composto por:

- **Pipeline de Processamento de Dados**: Limpeza, feature engineering e preparação dos dados
- **Modelo XGBoost**: Algoritmo de regressão para predição de preços
- **API REST Flask**: Serviço web para servir predições em tempo real
- **Endpoints de Dados**: Fornece dados únicos (cidades, bairros, tipos) para o frontend

---

## 📁 Estrutura do Projeto

```
backend/
├── src/
│   ├── __init__.py
│   ├── data_processing.py    # Processamento e feature engineering
│   └── model_trainer.py      # Treinamento e avaliação do modelo
├── api/
│   ├── app.py                # API REST (Flask)
│   ├── Procfile              # Configuração para deploy (Render)
│   └── start_api.sh          # Script de inicialização
├── models/                   # Modelos treinados (gerado automaticamente)
│   ├── model_*.pkl          # Modelo XGBoost
│   ├── scaler_*.pkl         # Scaler para normalização
│   ├── metadata_*.json       # Metadados do modelo
│   └── encoding_*.json       # Mapeamentos de encoding
├── train_model.py           # Script principal de treinamento
├── test_api.py              # Testes da API
├── test_training.py         # Testes do pipeline de treinamento
├── requirements.txt         # Dependências Python
├── render.yaml              # Configuração para deploy no Render
├── start.sh                 # Script alternativo de start
└── README.md               # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Navegue até o diretório do backend:**
   ```bash
   cd backend
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

4. **Para macOS (se necessário):**
   ```bash
   # XGBoost pode precisar de libomp
   brew install libomp
   ```

---

## 📊 Treinamento do Modelo

### Dataset

O modelo é treinado com o dataset `data/imoveis-df.csv`, que contém informações sobre imóveis para aluguel no Distrito Federal.

### Executar Treinamento

```bash
cd backend
python train_model.py
```

### O que o script faz:

1. **Carrega os dados** de `../data/imoveis-df.csv`
2. **Processa os dados**:
   - Filtra apenas imóveis para aluguel
   - Remove outliers (método IQR)
   - Trata valores faltantes
   - Aplica feature engineering
   - Faz encoding categórico
3. **Treina o modelo XGBoost**:
   - Divisão: 70% treino, 15% validação, 15% teste
   - Cross-validation para avaliação
4. **Avalia o modelo**:
   - MAE (Mean Absolute Error)
   - RMSE (Root Mean Squared Error)
   - R² (Coeficiente de Determinação)
5. **Salva o modelo** em `models/`:
   - Modelo treinado (`.pkl`)
   - Scaler (`.pkl`)
   - Metadados (`.json`)
   - Mapeamentos de encoding (`.json`)

### Saída Esperada

```
INFO: Carregando dados...
INFO: Processando dados...
INFO: Treinando modelo...
INFO: Avaliando modelo...
INFO: MAE: 250.50
INFO: RMSE: 350.75
INFO: R²: 0.85
INFO: Modelo salvo em models/model_20251209_194317.pkl
```

---

## 🔌 API REST

### Iniciar a API

```bash
cd backend/api
python app.py
```

A API estará disponível em `http://localhost:5020`

### Variáveis de Ambiente

A API suporta as seguintes variáveis de ambiente:

- `PORT`: Porta do servidor (padrão: 5020)
- `DEBUG`: Modo debug (padrão: false)

### Endpoints Disponíveis

#### `GET /health`

Health check da API e status do modelo.

**Resposta:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### `POST /predict`

Predição de preço de aluguel.

**Body (JSON):**
```json
{
  "area": 70.0,
  "bedrooms": 2,
  "bathrooms": 2,
  "parking_spaces": 1,
  "furnished": false,
  "hoa": 400.0,
  "property_type": "Apartamento",
  "city": "Brasília",
  "neighborhood": "asa norte",
  "suites": 0
}
```

**Resposta:**
```json
{
  "predicted_price": 2500.50,
  "price_per_sqm": 35.72,
  "model_version": "20251209_194317",
  "model_metrics": {
    "mae": 250.0,
    "rmse": 350.0,
    "r2": 0.85
  }
}
```

#### `GET /data/unique-values`

Retorna valores únicos de cidades, bairros e tipos de imóveis.

**Resposta:**
```json
{
  "cities": ["Brasília"],
  "neighborhoods": ["asa norte", "asa sul", "aguas claras", ...],
  "property_types": ["Apartamento", "Kitnet", "Casa", ...]
}
```

#### `GET /data/properties`

Retorna todos os imóveis do dataset com filtros opcionais.

**Query Parameters:**
- `property_type`: Filtrar por tipo de imóvel
- `neighborhood`: Filtrar por bairro
- `min_area`, `max_area`: Filtrar por área
- `min_bedrooms`, `max_bedrooms`: Filtrar por número de quartos
- `min_price`, `max_price`: Filtrar por preço
- `limit`: Limite de resultados (padrão: 1000)
- `offset`: Offset para paginação (padrão: 0)

**Exemplo:**
```
GET /data/properties?property_type=Apartamento&min_area=50&limit=10
```

**Resposta:**
```json
{
  "properties": [
    {
      "id": 0,
      "property_type": "Apartamento",
      "neighborhood": "asa norte",
      "area": 70.0,
      "bedrooms": 2,
      "bathrooms": 2,
      "parking_spaces": 1,
      "hoa": 400.0,
      "furnished": false,
      "rent_amount": 2500.0,
      "city": "Brasília"
    }
  ],
  "total": 2858,
  "returned": 10,
  "offset": 0,
  "limit": 10
}
```

#### `GET /data/cities`

Lista de cidades disponíveis.

#### `GET /data/neighborhoods`

Lista de bairros disponíveis.

#### `GET /data/property-types`

Lista de tipos de imóveis disponíveis.

---

## 🔧 Processamento de Dados

### Pipeline Completo

1. **Carregamento**: Leitura do CSV com separador `;`
2. **Filtragem**: Apenas imóveis para aluguel
3. **Seleção de Features**:
   - Numéricas: `area`, `bedrooms`, `bathrooms`, `parking_spaces`, `hoa`, `suites`
   - Categóricas: `property_type`, `city`, `neighborhood`, `furnished`
4. **Tratamento de Missing Values**:
   - Numéricos: Mediana
   - Categóricos: 'Desconhecido'
5. **Remoção de Outliers**: Método IQR (Interquartile Range)
6. **Feature Engineering**:
   - `price_per_sqm`: Preço por metro quadrado
7. **Encoding**:
   - One-Hot Encoding para `property_type` e `furnished`
   - Target Encoding para `city` e `neighborhood`
8. **Normalização**: StandardScaler para features numéricas

### Features Utilizadas

| Feature | Tipo | Descrição |
|---------|------|-----------|
| `area` | Numérica | Área do imóvel em m² |
| `bedrooms` | Numérica | Número de quartos |
| `bathrooms` | Numérica | Número de banheiros |
| `parking_spaces` | Numérica | Número de vagas de garagem |
| `hoa` | Numérica | Valor do condomínio |
| `suites` | Numérica | Número de suítes |
| `furnished` | Booleana | Imóvel mobiliado |
| `property_type` | Categórica | Tipo do imóvel (Apartamento, Casa, etc.) |
| `city` | Categórica | Cidade (Brasília) |
| `neighborhood` | Categórica | Bairro |
| `price_per_sqm` | Numérica (derivada) | Preço por metro quadrado |

---

## 🤖 Modelo de Machine Learning

### Algoritmo

- **XGBoost Regressor**: Gradient Boosting para regressão
- **Target**: `rent_amount` (preço de aluguel em R$)

### Hiperparâmetros

```python
{
    'n_estimators': 100,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42
}
```

### Métricas de Avaliação

- **MAE (Mean Absolute Error)**: Erro médio absoluto em R$
- **RMSE (Root Mean Squared Error)**: Raiz do erro quadrático médio
- **R² (Coeficiente de Determinação)**: Proporção da variância explicada (0-1)

### Validação

- Divisão: 70% treino, 15% validação, 15% teste
- Cross-validation: 5 folds
- Early stopping: Baseado no conjunto de validação

---

## 🚀 Deploy

### Render (Recomendado)

1. **Criar conta:** https://render.com
2. **Conectar repositório GitHub**
3. **Configurar:**
   - **Name**: `alugai-api`
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api/app.py`
   - **Plan**: Free

4. **Variáveis de Ambiente:**
   - `PORT`: Será definido automaticamente pelo Render
   - `DEBUG`: `false`

5. **Upload dos Modelos:**
   - Commit os arquivos em `backend/models/` no GitHub
   - Ou use storage externo (S3, etc.)

### Verificar Deploy

```bash
curl https://seu-backend.onrender.com/health
```

---

## 🧪 Testes

### Testar API Localmente

```bash
cd backend
python test_api.py
```

### Testar Pipeline de Treinamento

```bash
cd backend
python test_training.py
```

---

## 🔍 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'xgboost'"

**Solução:**
```bash
pip install xgboost
```

### Erro: "XGBoost Library (libxgboost.dylib) could not be loaded" (macOS)

**Solução:**
```bash
brew install libomp
```

### Erro: "Model not found"

**Solução:**
1. Execute `python train_model.py` para gerar o modelo
2. Verifique se os arquivos estão em `backend/models/`

### Erro: "Port already in use"

**Solução:**
1. Altere a porta no código ou variável de ambiente
2. Ou mate o processo usando a porta:
   ```bash
   lsof -ti:5020 | xargs kill -9
   ```

### API não conecta ao modelo

**Solução:**
1. Verifique os logs: `tail -f /tmp/api.log`
2. Confirme que o modelo está em `backend/models/`
3. Verifique se o caminho está correto no código

### Erro de encoding no dataset

**Solução:**
1. Verifique se o CSV está em UTF-8
2. Confirme que o separador é `;`
3. Verifique se as colunas estão corretas

---

## 📚 Dependências

- `pandas>=2.0.0`: Manipulação de dados
- `numpy>=1.24.0`: Operações numéricas
- `scikit-learn>=1.3.0`: Machine Learning
- `xgboost>=2.0.0`: Algoritmo XGBoost
- `flask>=2.3.0`: Framework web
- `flask-cors>=4.0.0`: CORS para integração
- `requests>=2.31.0`: Cliente HTTP

---

## 🔗 Integração com Frontend

O frontend Streamlit consome a API através de requisições HTTP:

```python
import requests

API_URL = "http://localhost:5020"  # ou URL do deploy

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

prediction = response.json()['predicted_price']
```

---

## 📝 Notas Importantes

- O modelo é treinado com dados do dataset completo
- Para produção, recomenda-se retreinar periodicamente
- Os modelos são versionados por timestamp
- A API carrega automaticamente o modelo mais recente
- CORS está configurado para permitir requisições do Streamlit Cloud

---

## 👥 Desenvolvido por

Equipe AlugAI - UnB 2025

---

## 📄 Licença

Este projeto é de uso acadêmico e educacional.
