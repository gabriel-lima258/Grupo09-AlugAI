"""
Página de busca de imóveis
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para importações
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from utils import config, helpers
import requests

# Configuração da página
config.set_page_config()
config.apply_custom_css()

# Inicialização de sessão
if 'consultas' not in st.session_state:
    st.session_state.consultas = []
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# Buscar dados únicos da API - suporta variável de ambiente para deploy
import os
API_URL = os.getenv('API_URL', 'http://localhost:5020')
if 'api_data' not in st.session_state:
    try:
        response = requests.get(f"{API_URL}/data/unique-values", timeout=5)
        if response.status_code == 200:
            st.session_state.api_data = response.json()
        else:
            st.session_state.api_data = None
    except:
        st.session_state.api_data = None

# Usar dados da API ou fallback
if st.session_state.api_data:
    neighborhoods_list = st.session_state.api_data.get('neighborhoods', helpers.BAIRROS_DF)
    property_types_list = st.session_state.api_data.get('property_types', helpers.TIPOS_IMOVEL)
else:
    neighborhoods_list = helpers.BAIRROS_DF
    property_types_list = helpers.TIPOS_IMOVEL

# Sidebar comum
with st.sidebar:
    logo_path = current_dir.parent / "docs" / "assets" / "logo_agente.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.title("🏠 AlugAI")
    st.markdown("---")
    st.markdown("### 💡 Dica")
    st.info("Use o formulário de busca para encontrar imóveis que atendam suas preferências!")
    st.markdown("---")
    st.markdown("### 📞 Suporte")
    st.markdown("Dúvidas? Entre em contato através da página **Sobre**")

def show():
    """Exibe a página de busca de imóveis"""
    
    st.title("🔍 Buscar Imóveis")
    st.markdown("Encontre imóveis que atendam suas preferências e veja a classificação automática de custo-benefício")
    
    st.markdown("---")
    
    # Formulário de busca
    with st.form("buscar_imoveis_form"):
        st.markdown("### 📝 Preferências do Imóvel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_type = st.selectbox(
                "Tipo de Imóvel",
                ["Todos"] + property_types_list,
                help="Selecione o tipo de imóvel desejado"
            )
            
            neighborhood = st.selectbox(
                "Bairro",
                ["Todos"] + neighborhoods_list,
                help="Selecione o bairro desejado"
            )
            
            min_area = st.number_input(
                "Área Mínima (m²)",
                min_value=0,
                max_value=500,
                value=0,
                step=10,
                help="Área mínima em metros quadrados"
            )
            
            max_area = st.number_input(
                "Área Máxima (m²)",
                min_value=0,
                max_value=500,
                value=300,
                step=10,
                help="Área máxima em metros quadrados"
            )
        
        with col2:
            rooms = st.slider(
                "Número de Quartos",
                min_value=0,
                max_value=5,
                value=(1, 4),
                help="Faixa de número de quartos"
            )
            
            bathrooms = st.slider(
                "Número de Banheiros",
                min_value=1,
                max_value=5,
                value=(1, 3),
                help="Faixa de número de banheiros"
            )
            
            parking_spaces = st.slider(
                "Vagas de Garagem",
                min_value=0,
                max_value=5,
                value=(0, 2),
                help="Faixa de número de vagas"
            )
            
            furniture = st.radio(
                "Mobiliado",
                ["Todos", "Sim", "Não"],
                horizontal=True
            )
        
        # Filtros adicionais
        st.markdown("### 💰 Faixa de Preço")
        
        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input(
                "Preço Mínimo (R$)",
                min_value=0,
                max_value=10000,
                value=1000,
                step=100
            )
        with col2:
            max_price = st.number_input(
                "Preço Máximo (R$)",
                min_value=0,
                max_value=10000,
                value=5000,
                step=100
            )
        
        # Botão de busca
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            buscar_button = st.form_submit_button(
                "🔍 Buscar Imóveis",
                use_container_width=True,
                type="primary"
            )
    
    st.markdown("---")
    
    # Carregar todos os imóveis automaticamente (sem precisar clicar em buscar)
    if 'all_properties' not in st.session_state or buscar_button:
        with st.spinner("🔄 Carregando imóveis do dataset..."):
            try:
                # Construir parâmetros de filtro
                params = {}
                if property_type != "Todos":
                    params['property_type'] = property_type
                if neighborhood != "Todos":
                    params['neighborhood'] = neighborhood
                if min_area > 0:
                    params['min_area'] = min_area
                if max_area < 500:
                    params['max_area'] = max_area
                if rooms[0] > 0:
                    params['min_bedrooms'] = rooms[0]
                if rooms[1] < 5:
                    params['max_bedrooms'] = rooms[1]
                if min_price > 0:
                    params['min_price'] = min_price
                if max_price < 10000:
                    params['max_price'] = max_price
                
                # Buscar imóveis da API
                response = requests.get(f"{API_URL}/data/properties", params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    properties = data.get('properties', [])
                    total = data.get('total', 0)
                    
                    # Para cada imóvel, obter estimativa de preço
                    for prop in properties:
                        try:
                            # Preparar dados para predição
                            predict_data = {
                                "area": prop.get('area', 0),
                                "bedrooms": prop.get('bedrooms', 0),
                                "bathrooms": prop.get('bathrooms', 1),
                                "parking_spaces": prop.get('parking_spaces', 0),
                                "furnished": prop.get('furnished', False),
                                "hoa": prop.get('hoa', 0),
                                "property_type": prop.get('property_type', 'Apartamento'),
                                "city": prop.get('city', 'Brasília'),
                                "neighborhood": prop.get('neighborhood', ''),
                                "suites": 0
                            }
                            
                            # Obter estimativa
                            predict_response = requests.post(
                                f"{API_URL}/predict",
                                json=predict_data,
                                timeout=5
                            )
                            
                            if predict_response.status_code == 200:
                                predict_result = predict_response.json()
                                prop['estimated_price'] = predict_result.get('predicted_price', prop.get('rent_amount', 0))
                            else:
                                prop['estimated_price'] = prop.get('rent_amount', 0)
                        except:
                            prop['estimated_price'] = prop.get('rent_amount', 0)
                    
                    st.session_state.all_properties = properties
                    st.session_state.total_properties = total
                else:
                    st.error(f"Erro ao buscar imóveis: {response.status_code}")
                    st.session_state.all_properties = []
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")
                st.info("💡 Certifique-se de que a API está rodando em http://localhost:5020")
                st.session_state.all_properties = []
    
    # Exibir resultados
    if 'all_properties' in st.session_state and len(st.session_state.all_properties) > 0:
        properties = st.session_state.all_properties
        total = st.session_state.get('total_properties', len(properties))
        
        st.success(f"✅ {len(properties)} imóveis encontrados (de {total} total no dataset)")
        
        # Classificar por vantajosidade
        for prop in properties:
            classification = helpers.classify_property(
                prop.get('estimated_price', prop.get('rent_amount', 0)),
                prop.get('rent_amount', 0)
            )
            prop['classification'] = classification
        
        # Ordenar por vantajosidade (mais vantajosos primeiro)
        properties.sort(key=lambda x: x.get('classification', {}).get('diff_pct', 0))
        
        # Exibir resultados
        st.markdown("### 📋 Imóveis Disponíveis")
        
        # Paginação
        items_per_page = 10
        if 'page' not in st.session_state:
            st.session_state.page = 0
        
        total_pages = (len(properties) - 1) // items_per_page + 1
        start_idx = st.session_state.page * items_per_page
        end_idx = start_idx + items_per_page
        
        # Controles de paginação
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col1:
            if st.button("◀️ Anterior", disabled=st.session_state.page == 0):
                st.session_state.page = max(0, st.session_state.page - 1)
                st.rerun()
        with col3:
            st.markdown(f"**Página {st.session_state.page + 1} de {total_pages}**")
        with col5:
            if st.button("Próxima ▶️", disabled=st.session_state.page >= total_pages - 1):
                st.session_state.page = min(total_pages - 1, st.session_state.page + 1)
                st.rerun()
        
        # Exibir imóveis da página atual
        for prop in properties[start_idx:end_idx]:
            # Preparar dados para o card
            prop_card = {
                'id': prop.get('id', 0),
                'title': f"{prop.get('property_type', 'Imóvel')} - {prop.get('neighborhood', 'N/A')}",
                'neighborhood': prop.get('neighborhood', 'N/A'),
                'area': prop.get('area', 0),
                'rooms': prop.get('bedrooms', 0),
                'bathrooms': prop.get('bathrooms', 1),
                'parking_spaces': prop.get('parking_spaces', 0),
                'announced_price': prop.get('rent_amount', 0),
                'estimated_price': prop.get('estimated_price', prop.get('rent_amount', 0)),
                'property_type': prop.get('property_type', 'Apartamento'),
                'furniture': prop.get('furnished', False),
                'hoa': prop.get('hoa', 0)
            }
            
            st.markdown(helpers.create_property_card(prop_card), unsafe_allow_html=True)
            
            # Botões de ação
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"💰 Ver Detalhes", key=f"details_{prop.get('id', 0)}"):
                    # Obter estimativa real do modelo
                    try:
                        predict_data = {
                            "area": prop.get('area', 0),
                            "bedrooms": prop.get('bedrooms', 0),
                            "bathrooms": prop.get('bathrooms', 1),
                            "parking_spaces": prop.get('parking_spaces', 0),
                            "furnished": prop.get('furnished', False),
                            "hoa": prop.get('hoa', 0),
                            "property_type": prop.get('property_type', 'Apartamento'),
                            "city": prop.get('city', 'Brasília'),
                            "neighborhood": prop.get('neighborhood', ''),
                            "suites": 0
                        }
                        
                        predict_response = requests.post(
                            f"{API_URL}/predict",
                            json=predict_data,
                            timeout=5
                        )
                        
                        if predict_response.status_code == 200:
                            predict_result = predict_response.json()
                            estimated_price = predict_result.get('predicted_price', prop.get('rent_amount', 0))
                        else:
                            estimated_price = prop.get('rent_amount', 0)
                    except:
                        estimated_price = prop.get('rent_amount', 0)
                    
                    diff = prop.get('rent_amount', 0) - estimated_price
                    diff_pct = (diff / estimated_price * 100) if estimated_price > 0 else 0
                    
                    st.info(f"""
                    **Detalhes do Imóvel:**
                    - Tipo: {prop.get('property_type', 'N/A')}
                    - Bairro: {prop.get('neighborhood', 'N/A')}
                    - Área: {prop.get('area', 0)} m²
                    - Quartos: {prop.get('bedrooms', 0)}
                    - Banheiros: {prop.get('bathrooms', 1)}
                    - Vagas: {prop.get('parking_spaces', 0)}
                    - Condomínio: R$ {prop.get('hoa', 0):.2f}
                    - Mobiliado: {'Sim' if prop.get('furnished', False) else 'Não'}
                    - Preço Anunciado: {helpers.format_currency(prop.get('rent_amount', 0))}
                    - Preço Estimado (IA): {helpers.format_currency(estimated_price)}
                    - Diferença: {helpers.format_currency(abs(diff))} ({diff_pct:+.1f}%)
                    """)
            with col2:
                if st.button(f"📊 Comparar", key=f"compare_{prop.get('id', 0)}"):
                    diff = prop.get('rent_amount', 0) - prop.get('estimated_price', 0)
                    diff_pct = (diff / prop.get('estimated_price', 1)) * 100 if prop.get('estimated_price', 0) > 0 else 0
                    st.info(f"Diferença: {helpers.format_currency(abs(diff))} ({diff_pct:+.1f}%)")
            with col3:
                prop_id = prop.get('id', 0)
                if st.button(f"⭐ Favoritar", key=f"fav_{prop_id}"):
                    if prop_id not in st.session_state.favoritos:
                        st.session_state.favoritos.append(prop_id)
                        st.success("Adicionado aos favoritos!")
                    else:
                        st.info("Já está nos favoritos")
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    elif buscar_button:
        # Salvar consulta no histórico
        query_data = {
            "type": "busca",
            "property_type": property_type,
            "neighborhood": neighborhood,
            "min_area": min_area,
            "max_area": max_area,
            "rooms": rooms,
            "bathrooms": bathrooms,
            "parking_spaces": parking_spaces,
            "furniture": furniture,
            "min_price": min_price,
            "max_price": max_price
        }
        helpers.save_query(query_data)
        
        # Gerar resultados mock (será substituído por busca real)
        with st.spinner("Buscando imóveis..."):
            properties = helpers.generate_mock_properties(count=8)
            
            # Aplicar filtros
            filtered_properties = []
            for prop in properties:
                if property_type != "Todos" and prop["property_type"] != property_type:
                    continue
                if neighborhood != "Todos" and prop["neighborhood"] != neighborhood:
                    continue
                if not (min_area <= prop["area"] <= max_area):
                    continue
                if not (rooms[0] <= prop["rooms"] <= rooms[1]):
                    continue
                if not (bathrooms[0] <= prop["bathrooms"] <= bathrooms[1]):
                    continue
                if not (parking_spaces[0] <= prop["parking_spaces"] <= parking_spaces[1]):
                    continue
                if furniture == "Sim" and not prop.get("furniture", False):
                    continue
                if furniture == "Não" and prop.get("furniture", False):
                    continue
                if not (min_price <= prop["announced_price"] <= max_price):
                    continue
                
                filtered_properties.append(prop)
            
            if filtered_properties:
                st.success(f"✅ Encontrados {len(filtered_properties)} imóveis que atendem suas preferências!")
                
                # Classificar por vantajosidade
                for prop in filtered_properties:
                    classification = helpers.classify_property(
                        prop["estimated_price"],
                        prop["announced_price"]
                    )
                    prop["classification"] = classification
                
                # Ordenar por vantajosidade (mais vantajosos primeiro)
                filtered_properties.sort(key=lambda x: x["classification"]["diff_pct"])
                
                # Exibir resultados
                st.markdown("### 📋 Resultados da Busca")
                
                for prop in filtered_properties:
                    st.markdown(helpers.create_property_card(prop), unsafe_allow_html=True)
                    
                    # Botões de ação
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button(f"💰 Ver Detalhes", key=f"details_{prop['id']}"):
                            st.info(f"Detalhes completos do imóvel {prop['id']} serão exibidos aqui")
                    with col2:
                        if st.button(f"📊 Comparar Preços", key=f"compare_{prop['id']}"):
                            st.info("Redirecionando para página de comparação...")
                    with col3:
                        if st.button(f"⭐ Favoritar", key=f"fav_{prop['id']}"):
                            if prop['id'] not in st.session_state.favoritos:
                                st.session_state.favoritos.append(prop['id'])
                                st.success("Adicionado aos favoritos!")
                            else:
                                st.info("Já está nos favoritos")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Nenhum imóvel encontrado com os filtros selecionados. Tente ajustar suas preferências.")
                
                # Sugestões
                st.info("💡 **Dicas:**\n"
                       "- Tente aumentar a faixa de preço\n"
                       "- Considere outros bairros\n"
                       "- Ajuste o número de quartos ou área")
    
    else:
        # Mensagem inicial - carregar imóveis automaticamente
        if 'all_properties' not in st.session_state:
            with st.spinner("🔄 Carregando todos os imóveis do dataset..."):
                try:
                    # Buscar todos os imóveis sem filtros
                    response = requests.get(f"{API_URL}/data/properties", params={'limit': 500}, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        properties = data.get('properties', [])
                        total = data.get('total', 0)
                        
                        # Usar preço anunciado como estimativa inicial
                        # (predições podem ser feitas sob demanda)
                        for prop in properties:
                            prop['estimated_price'] = prop.get('rent_amount', 0)
                        
                        st.session_state.all_properties = properties
                        st.session_state.total_properties = total
                        st.rerun()
                    else:
                        st.error(f"Erro ao buscar imóveis: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao conectar com a API: {str(e)}")
                    st.info("💡 Certifique-se de que a API está rodando em http://localhost:5020")
        
        if 'all_properties' in st.session_state and len(st.session_state.all_properties) > 0:
            st.info(f"📊 **{len(st.session_state.all_properties)} imóveis** carregados do dataset. Use os filtros acima para refinar sua busca!")
        else:
            st.info("👆 **Carregando imóveis...** Use os filtros acima para refinar sua busca quando os dados carregarem!")

# Executar quando o arquivo é executado diretamente pelo Streamlit
show()

