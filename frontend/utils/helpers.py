"""
Funções auxiliares para a aplicação
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional

# Dados padrão (serão substituídos por dados da API)
BAIRROS_DF = [
    "Asa Norte", "Asa Sul", "Águas Claras", "Taguatinga", "Ceilândia",
    "Guará", "Sobradinho", "Planaltina", "Gama", "Santa Maria",
    "São Sebastião", "Recanto das Emas", "Samambaia", "Brazlândia",
    "Núcleo Bandeirante", "Riacho Fundo", "Lago Norte", "Lago Sul",
    "Sudoeste", "Noroeste", "Vicente Pires", "Águas Lindas"
]

TIPOS_IMOVEL = [
    "UNIT", "APARTMENT", "HOUSE"
]

def get_api_data(api_url: str = None):
    """Busca dados únicos da API"""
    import requests
    import os
    
    # Usar variável de ambiente ou padrão
    if api_url is None:
        api_url = os.getenv('API_URL', 'http://localhost:5020')
    
    try:
        # Buscar valores únicos
        response = requests.get(f"{api_url}/data/unique-values", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'cities': data.get('cities', []),
                'neighborhoods': data.get('neighborhoods', []),
                'property_types': data.get('property_types', [])
            }
    except:
        pass
    
    # Fallback para valores padrão
    return {
        'cities': [],
        'neighborhoods': BAIRROS_DF,
        'property_types': TIPOS_IMOVEL
    }

def format_currency(value: float) -> str:
    """Formata um valor numérico como moeda brasileira"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate_price_per_sqm(price: float, area: float) -> float:
    """Calcula o preço por metro quadrado"""
    if area > 0:
        return price / area
    return 0

def classify_property(estimated_price: float, announced_price: float, threshold: float = 0.1) -> Dict:
    """
    Classifica um imóvel como vantajoso ou não baseado na diferença entre
    preço estimado e anunciado
    
    Args:
        estimated_price: Preço estimado pelo modelo
        announced_price: Preço anunciado
        threshold: Limiar de diferença percentual (padrão 10%)
    
    Returns:
        Dict com classificação e informações
    """
    if announced_price == 0:
        return {
            "status": "info",
            "label": "Sem preço anunciado",
            "message": "Apenas estimativa disponível"
        }
    
    diff = announced_price - estimated_price
    diff_pct = (diff / estimated_price) * 100
    
    if diff_pct <= -threshold * 100:  # Preço anunciado muito abaixo da estimativa
        return {
            "status": "success",
            "label": "Muito Vantajoso",
            "message": f"Preço {abs(diff_pct):.1f}% abaixo da estimativa",
            "diff": diff,
            "diff_pct": diff_pct
        }
    elif abs(diff_pct) <= threshold * 100:  # Preço próximo da estimativa
        return {
            "status": "info",
            "label": "Preço Justo",
            "message": f"Preço próximo da estimativa ({diff_pct:+.1f}%)",
            "diff": diff,
            "diff_pct": diff_pct
        }
    else:  # Preço anunciado muito acima da estimativa
        return {
            "status": "warning",
            "label": "Atenção",
            "message": f"Preço {diff_pct:.1f}% acima da estimativa",
            "diff": diff,
            "diff_pct": diff_pct
        }

def save_query(query_data: Dict):
    """Salva uma consulta no histórico"""
    query_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.consultas.append(query_data)

def get_recent_queries(limit: int = 10) -> List[Dict]:
    """Retorna as consultas mais recentes"""
    queries = st.session_state.consultas.copy()
    queries.reverse()  # Mais recentes primeiro
    return queries[:limit]

def create_property_card(property_data: Dict) -> str:
    """
    Cria um card HTML para exibir informações de um imóvel
    
    Args:
        property_data: Dicionário com dados do imóvel
    
    Returns:
        HTML string do card
    """
    classification = classify_property(
        property_data.get("estimated_price", 0),
        property_data.get("announced_price", 0)
    )
    
    badge_class = {
        "success": "badge-success",
        "warning": "badge-warning",
        "info": "badge-info"
    }.get(classification["status"], "badge-info")
    
    card_html = f"""
    <div class="property-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3>{property_data.get('title', 'Imóvel')}</h3>
                <p><strong>📍 {property_data.get('neighborhood', 'N/A')}</strong></p>
            </div>
            <span class="badge {badge_class}">{classification['label']}</span>
        </div>
        <div style="margin-top: 1rem;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                <div>
                    <strong>💰 Preço Anunciado</strong><br>
                    {format_currency(property_data.get('announced_price', 0))}
                </div>
                <div>
                    <strong>🤖 Preço Estimado</strong><br>
                    {format_currency(property_data.get('estimated_price', 0))}
                </div>
                <div>
                    <strong>📐 Área</strong><br>
                    {property_data.get('area', 0)} m²
                </div>
                <div>
                    <strong>🛏️ Quartos</strong><br>
                    {property_data.get('rooms', 0)}
                </div>
            </div>
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;">
            <p><strong>ℹ️ {classification['message']}</strong></p>
            <p><small>🏢 {property_data.get('property_type', 'N/A')} | 
                      🚗 {property_data.get('parking_spaces', 0)} vagas | 
                      🛁 {property_data.get('bathrooms', 0)} banheiros</small></p>
        </div>
    </div>
    """
    return card_html

def generate_mock_properties(count: int = 5) -> List[Dict]:
    """Gera dados mock de imóveis para desenvolvimento"""
    import random
    
    properties = []
    for i in range(count):
        area = random.randint(40, 200)
        rooms = random.randint(1, 4)
        announced_price = random.randint(1500, 5000)
        estimated_price = announced_price * random.uniform(0.85, 1.15)
        
        properties.append({
            "id": i + 1,
            "title": f"Imóvel {i + 1}",
            "neighborhood": random.choice(BAIRROS_DF),
            "area": area,
            "rooms": rooms,
            "bathrooms": random.randint(1, rooms + 1),
            "parking_spaces": random.randint(0, 2),
            "announced_price": announced_price,
            "estimated_price": estimated_price,
            "property_type": random.choice(TIPOS_IMOVEL),
            "furniture": random.choice([True, False]),
            "hoa": random.randint(200, 800)
        })
    
    return properties




