# Backend AlugAI - Machine Learning

Backend de Machine Learning para o sistema AlugAI, responsável pelo treinamento e serviço do modelo de predição de preços de aluguel.

## 📁 Estrutura

```
backend/
├── src/
│   ├── data_processing.py    # Processamento e feature engineering
│   └── model_trainer.py      # Treinamento do modelo
├── api/
│   └── app.py                # API REST (Flask)
├── models/                   # Modelos treinados (gerado)
├── train_model.py           # Script de treinamento
├── requirements.txt         # Dependências
└── README.md               # Este arquivo
```

## 🚀 Instalação

1. **Instalar dependências:**
```bash
cd backend
pip install -r requirements.txt
```

## 📊 Treinamento do Modelo

Para treinar o modelo com o dataset:

```bash
python train_model.py
```

O script irá:
1. Carregar e processar os dados de `../data/dataZAP.csv`
2. Aplicar feature engineering
3. Treinar modelo XGBoost
4. Avaliar o modelo (MAE, RMSE, R²)
5. Salvar modelo em `models/`

## 🔌 API REST

### Iniciar a API:

```bash
cd api
python app.py
```

A API estará disponível em `http://localhost:5020`

### Endpoints:

#### `GET /health`
Health check da API

**Resposta:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### `POST /predict`
Predição de preço de aluguel

**Body (JSON):**
```json
{
  "area": 70.0,
  "bedrooms": 2,
  "bathrooms": 2,
  "parking_spaces": 1,
  "furnished": false,
  "hoa": 400.0,
  "property_type": "UNIT",
  "city": "Brasília",
  "neighborhood": "Asa Norte",
  "suites": 0
}
```

**Resposta:**
```json
{
  "predicted_price": 2500.50,
  "price_per_sqm": 35.72,
  "features_used": {
    "area": "Alto",
    "city": "Alto",
    "neighborhood": "Alto"
  },
  "model_version": "20250101_120000",
  "model_metrics": {
    "mae": 250.0,
    "r2": 0.85
  }
}
```

#### `GET /model/info`
Informações sobre o modelo carregado

## 🔧 Processamento de Dados

O pipeline de processamento inclui:

1. **Filtragem**: Apenas imóveis para aluguel
2. **Seleção de Features**: Área, quartos, banheiros, vagas, etc.
3. **Tratamento de Missing Values**: Mediana para numéricos, moda para categóricos
4. **Remoção de Outliers**: Método IQR
5. **Feature Engineering**: 
   - `price_per_sqm`: Preço por metro quadrado
6. **Encoding**: 
   - One-Hot Encoding para features categóricas de baixa cardinalidade
   - Target Encoding para city e neighborhood

## 🤖 Modelo

- **Algoritmo**: XGBoost Regressor
- **Target**: `rent_amount` (preço de aluguel)
- **Métricas**: MAE, RMSE, R²
- **Validação**: 70% treino, 15% validação, 15% teste + Cross-validation

## 📝 Notas

- O modelo é treinado com dados do dataset completo
- Para produção, recomenda-se filtrar apenas dados do DF
- O modelo salvo inclui scaler e metadados
- A API carrega automaticamente o modelo mais recente

## 🔗 Integração com Frontend

O frontend Streamlit pode consumir a API através de requisições HTTP:

```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    'area': 70,
    'bedrooms': 2,
    'bathrooms': 2,
    'parking_spaces': 1,
    'furnished': False,
    'hoa': 400,
    'property_type': 'UNIT',
    'city': 'Brasília',
    'neighborhood': 'Asa Norte'
})

prediction = response.json()['predicted_price']
```

