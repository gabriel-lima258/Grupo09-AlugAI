# 🚀 Guia Rápido - Backend AlugAI

## Passo a Passo

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Treinar o Modelo

```bash
python train_model.py
```

Isso irá:
- Processar o dataset `../data/dataZAP.csv`
- Treinar modelo XGBoost
- Salvar modelo em `models/`

**Tempo estimado:** 5-15 minutos (dependendo do hardware)

### 3. Iniciar a API

Em um terminal separado:

```bash
cd backend/api
python app.py
```

A API estará disponível em `http://localhost:5020`

### 4. Testar a API

Em outro terminal:

```bash
cd backend
python test_api.py
```

## 📋 Exemplo de Uso da API

### Python

```python
import requests

response = requests.post('http://localhost:5020/predict', json={
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

result = response.json()
print(f"Preço estimado: R$ {result['predicted_price']:.2f}")
```

### cURL

```bash
curl -X POST http://localhost:5020/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 70,
    "bedrooms": 2,
    "bathrooms": 2,
    "parking_spaces": 1,
    "furnished": false,
    "hoa": 400,
    "property_type": "UNIT",
    "city": "Brasília",
    "neighborhood": "Asa Norte"
  }'
```

## 🔧 Troubleshooting

### Erro: "Nenhum modelo encontrado"
- Execute `python train_model.py` primeiro

### Erro: "ModuleNotFoundError"
- Instale as dependências: `pip install -r requirements.txt`

### API não responde
- Verifique se a API está rodando: `curl http://localhost:5020/health`
- Verifique os logs da API para erros

## 📊 Estrutura de Dados Esperada

O modelo espera as seguintes features:

- **area** (float): Área em m²
- **bedrooms** (int): Número de quartos
- **bathrooms** (int): Número de banheiros
- **parking_spaces** (int): Número de vagas
- **furnished** (bool): Mobiliado (True/False)
- **hoa** (float): Valor do condomínio
- **property_type** (str): Tipo do imóvel (ex: "UNIT", "APARTMENT")
- **city** (str): Cidade
- **neighborhood** (str): Bairro
- **suites** (int, opcional): Número de suítes

