"""
API REST simples para servir o modelo de ML
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Permitir CORS - incluir domínios de deploy (Streamlit Cloud, etc)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://*.streamlit.app",  # Streamlit Cloud
            "http://localhost:8501",    # Local
            "http://localhost:8502",    # Local alternativo
            "*"  # Em produção, remover e especificar apenas domínios permitidos
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Variáveis globais para modelo e scaler
model = None
scaler = None
feature_names = None
metadata = None
encoding_maps = None
unique_values = None


def load_latest_model():
    """Carrega o modelo mais recente"""
    global model, scaler, feature_names, metadata, encoding_maps, unique_values
    
    models_dir = Path(__file__).parent.parent / "models"
    
    # Encontrar modelo mais recente
    model_files = list(models_dir.glob("model_*.pkl"))
    if not model_files:
        raise FileNotFoundError("Nenhum modelo encontrado. Execute train_model.py primeiro.")
    
    # Pegar o mais recente
    latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
    version = latest_model.stem.replace("model_", "")
    
    logger.info(f"Carregando modelo versão: {version}")
    
    # Carregar modelo
    with open(latest_model, 'rb') as f:
        model = pickle.load(f)
    
    # Carregar scaler
    scaler_path = models_dir / f"scaler_{version}.pkl"
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    # Carregar metadados
    metadata_path = models_dir / f"metadata_{version}.json"
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        feature_names = metadata['feature_names']
    
    # Carregar encoding maps e unique values
    encoding_path = models_dir / f"encoding_{version}.json"
    if encoding_path.exists():
        with open(encoding_path, 'r', encoding='utf-8') as f:
            encoding_data = json.load(f)
            encoding_maps = encoding_data.get('encoding_maps', {})
            unique_values = encoding_data.get('unique_values', {})
        logger.info("Mapeamentos de encoding carregados com sucesso!")
    else:
        logger.warning("Arquivo de encoding não encontrado. Usando valores padrão.")
        encoding_maps = {}
        unique_values = {}
    
    logger.info("Modelo carregado com sucesso!")


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para predição de preço de aluguel
    
    Body esperado (JSON):
    {
        "area": float,
        "bedrooms": int,
        "bathrooms": int,
        "parking_spaces": int,
        "furnished": bool,
        "hoa": float,
        "property_type": str,
        "city": str,
        "neighborhood": str,
        "suites": int (opcional)
    }
    """
    if model is None or scaler is None:
        return jsonify({'error': 'Modelo não carregado'}), 500
    
    try:
        data = request.json
        
        # Validar campos obrigatórios
        required_fields = ['area', 'bedrooms', 'bathrooms', 'parking_spaces', 
                         'furnished', 'hoa', 'property_type']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': f'Campos obrigatórios faltando: {missing_fields}'
            }), 400
        
        # Preparar features
        features = prepare_features(data)
        
        # Fazer predição
        prediction = model.predict(features)[0]
        
        # Calcular preço por m²
        price_per_sqm = prediction / data['area'] if data['area'] > 0 else 0
        
        # Feature importance (simplificado)
        feature_importance = get_simple_feature_importance(data)
        
        return jsonify({
            'predicted_price': float(prediction),
            'price_per_sqm': float(price_per_sqm),
            'features_used': feature_importance,
            'model_version': metadata.get('version', 'unknown'),
            'model_metrics': {
                'mae': metadata.get('metrics', {}).get('MAE', 0),
                'r2': metadata.get('metrics', {}).get('R2', 0)
            }
        })
    
    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        return jsonify({'error': str(e)}), 500


def prepare_features(data: dict) -> np.ndarray:
    """Prepara features para predição"""
    # Inicializar DataFrame com zeros para todas as features esperadas
    df = pd.DataFrame(0, index=[0], columns=feature_names)
    
    # Preencher features numéricas básicas
    df['area'] = data.get('area', 0)
    df['bedrooms'] = data.get('bedrooms', 0)
    df['bathrooms'] = data.get('bathrooms', 0)
    df['parking_spaces'] = data.get('parking_spaces', 0)
    df['furnished'] = 1 if data.get('furnished', False) else 0
    df['hoa'] = data.get('hoa', 0)
    df['suites'] = data.get('suites', 0)
    
    # Calcular price_per_sqm (estimativa inicial baseada na média)
    mean_rent = encoding_maps.get('mean_rent', 2000) if encoding_maps else 2000
    if df['area'].iloc[0] > 0:
        # Usar média de preço por m² do dataset
        estimated_price_per_sqm = mean_rent / 70  # Assumindo área média de 70m²
        df['price_per_sqm'] = estimated_price_per_sqm
    else:
        df['price_per_sqm'] = mean_rent / 70
    
    # Encoding de city (target encoding)
    if 'city_encoded' in df.columns:
        city = data.get('city', '')
        city_encoding = encoding_maps.get('city_encoding', {}) if encoding_maps else {}
        df['city_encoded'] = city_encoding.get(city, mean_rent)
    
    # Encoding de neighborhood (target encoding)
    if 'neighborhood_encoded' in df.columns:
        neighborhood = data.get('neighborhood', '')
        neighborhood_encoding = encoding_maps.get('neighborhood_encoding', {}) if encoding_maps else {}
        df['neighborhood_encoded'] = neighborhood_encoding.get(neighborhood, mean_rent)
    
    # Encoding de property_type (One-Hot - se necessário)
    property_type = data.get('property_type', 'UNIT')
    property_col = f'property_type_{property_type}'
    if property_col in df.columns:
        df[property_col] = 1
    
    # Garantir que todas as features estão presentes e na ordem correta
    df = df[feature_names]
    
    # Normalizar
    features_scaled = scaler.transform(df)
    
    return features_scaled


def get_simple_feature_importance(data: dict) -> dict:
    """Retorna importância simplificada das features"""
    importance = {}
    
    # Valores baseados na importância típica
    importance['area'] = 'Alto'
    importance['city'] = 'Alto'
    importance['neighborhood'] = 'Alto'
    importance['bedrooms'] = 'Médio'
    importance['hoa'] = 'Médio'
    importance['bathrooms'] = 'Médio'
    importance['parking_spaces'] = 'Baixo'
    importance['furnished'] = 'Baixo'
    
    return importance


@app.route('/model/info', methods=['GET'])
def model_info():
    """Retorna informações sobre o modelo"""
    if metadata is None:
        return jsonify({'error': 'Modelo não carregado'}), 500
    
    return jsonify({
        'version': metadata.get('version', 'unknown'),
        'timestamp': metadata.get('timestamp', 'unknown'),
        'metrics': metadata.get('metrics', {}),
        'top_features': metadata.get('feature_importance', [])[:10]
    })


@app.route('/data/unique-values', methods=['GET'])
def get_unique_values():
    """Retorna valores únicos de features categóricas"""
    if unique_values is None:
        return jsonify({'error': 'Dados não carregados'}), 500
    
    return jsonify(unique_values)


@app.route('/data/cities', methods=['GET'])
def get_cities():
    """Retorna lista de cidades disponíveis"""
    if unique_values is None:
        return jsonify({'error': 'Dados não carregados'}), 500
    
    cities = unique_values.get('cities', [])
    return jsonify({'cities': cities})


@app.route('/data/neighborhoods', methods=['GET'])
def get_neighborhoods():
    """Retorna lista de bairros disponíveis"""
    if unique_values is None:
        return jsonify({'error': 'Dados não carregados'}), 500
    
    neighborhoods = unique_values.get('neighborhoods', [])
    return jsonify({'neighborhoods': neighborhoods})


@app.route('/data/property-types', methods=['GET'])
def get_property_types():
    """Retorna lista de tipos de imóveis disponíveis"""
    if unique_values is None:
        return jsonify({'error': 'Dados não carregados'}), 500
    
    property_types = unique_values.get('property_types', [])
    return jsonify({'property_types': property_types})


@app.route('/data/properties', methods=['GET'])
def get_properties():
    """
    Retorna todos os imóveis do dataset treinado
    Permite filtros opcionais via query parameters
    """
    try:
        # Carregar dados originais do dataset
        data_path = Path(__file__).parent.parent.parent / "data" / "imoveis-df.csv"
        
        if not data_path.exists():
            # Tentar formato antigo
            data_path = Path(__file__).parent.parent.parent / "data" / "dataZAP.csv"
            if not data_path.exists():
                return jsonify({'error': 'Dataset não encontrado'}), 404
        
        # Carregar dados
        df = pd.read_csv(data_path, sep=';', low_memory=False)
        
        # Aplicar filtros opcionais
        filters = request.args.to_dict()
        
        if 'preco' in df.columns:
            # Formato novo: imoveis-df.csv
            # Converter preco para numérico
            df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
            df = df[df['preco'].notna() & (df['preco'] > 0) & (df['preco'] < 100000)].copy()
            
            # Renomear colunas para formato padrão
            df = df.rename(columns={
                'preco': 'rent_amount',
                'tipo': 'property_type',
                'area': 'area',
                'quartos': 'bedrooms',
                'bairro': 'neighborhood'
            })
            
            # Adicionar campos padrão
            df['bathrooms'] = 1
            df['parking_spaces'] = 0
            df['hoa'] = 0
            df['furnished'] = False
            df['suites'] = 0
            df['city'] = 'Brasília'
        
        # Aplicar filtros opcionais
        if 'property_type' in filters and filters['property_type'] and filters['property_type'] != 'Todos':
            df = df[df['property_type'].str.contains(filters['property_type'], case=False, na=False)]
        
        if 'neighborhood' in filters and filters['neighborhood'] and filters['neighborhood'] != 'Todos':
            df = df[df['neighborhood'].str.contains(filters['neighborhood'], case=False, na=False)]
        
        if 'min_area' in filters and filters['min_area']:
            try:
                min_area = float(filters['min_area'])
                df = df[pd.to_numeric(df['area'], errors='coerce') >= min_area]
            except:
                pass
        
        if 'max_area' in filters and filters['max_area']:
            try:
                max_area = float(filters['max_area'])
                df = df[pd.to_numeric(df['area'], errors='coerce') <= max_area]
            except:
                pass
        
        if 'min_bedrooms' in filters and filters['min_bedrooms']:
            try:
                min_bedrooms = int(filters['min_bedrooms'])
                df = df[pd.to_numeric(df['bedrooms'], errors='coerce') >= min_bedrooms]
            except:
                pass
        
        if 'max_bedrooms' in filters and filters['max_bedrooms']:
            try:
                max_bedrooms = int(filters['max_bedrooms'])
                df = df[pd.to_numeric(df['bedrooms'], errors='coerce') <= max_bedrooms]
            except:
                pass
        
        if 'min_price' in filters and filters['min_price']:
            try:
                min_price = float(filters['min_price'])
                df = df[df['rent_amount'] >= min_price]
            except:
                pass
        
        if 'max_price' in filters and filters['max_price']:
            try:
                max_price = float(filters['max_price'])
                df = df[df['rent_amount'] <= max_price]
            except:
                pass
        
        # Limitar número de resultados (paginacao)
        limit = int(filters.get('limit', 1000))
        offset = int(filters.get('offset', 0))
        
        # Converter para formato JSON
        properties = []
        for idx, row in df.iloc[offset:offset+limit].iterrows():
            prop = {
                'id': int(idx) if pd.notna(idx) else len(properties),
                'property_type': str(row.get('property_type', 'Desconhecido')),
                'neighborhood': str(row.get('neighborhood', 'Desconhecido')),
                'area': float(row.get('area', 0)) if pd.notna(row.get('area')) else 0,
                'bedrooms': int(row.get('bedrooms', 0)) if pd.notna(row.get('bedrooms')) else 0,
                'bathrooms': int(row.get('bathrooms', 1)) if pd.notna(row.get('bathrooms')) else 1,
                'parking_spaces': int(row.get('parking_spaces', 0)) if pd.notna(row.get('parking_spaces')) else 0,
                'hoa': float(row.get('hoa', 0)) if pd.notna(row.get('hoa')) else 0,
                'furnished': bool(row.get('furnished', False)) if pd.notna(row.get('furnished')) else False,
                'rent_amount': float(row.get('rent_amount', 0)) if pd.notna(row.get('rent_amount')) else 0,
                'city': str(row.get('city', 'Brasília'))
            }
            properties.append(prop)
        
        return jsonify({
            'properties': properties,
            'total': len(df),
            'returned': len(properties),
            'offset': offset,
            'limit': limit
        })
    
    except Exception as e:
        logger.error(f"Erro ao buscar propriedades: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Carregar modelo ao iniciar
    try:
        load_latest_model()
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        logger.warning("API iniciada sem modelo. Endpoints de predição não funcionarão.")
    
    # Iniciar servidor - suporta variável PORT para deploy (Render, Railway, etc)
    import os
    port = int(os.environ.get('PORT', 5020))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    logger.info(f"Iniciando servidor na porta {port}...")
    logger.info(f"API disponível em: http://localhost:{port}")
    # use_reloader=False evita erro de signal em threads não-principais
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)

