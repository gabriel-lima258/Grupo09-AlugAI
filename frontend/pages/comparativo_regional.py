"""
Página de comparativo regional
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
else:
    neighborhoods_list = helpers.BAIRROS_DF

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
    """Exibe a página de comparativo regional"""
    
    st.title("📊 Comparativo Regional")
    st.markdown("Analise a variação de preços de aluguel por região no Distrito Federal")
    
    st.markdown("---")
    
    # Seleção de visualização
    view_type = st.radio(
        "Tipo de Visualização",
        ["Mapa Interativo", "Gráficos Comparativos", "Tabela de Dados"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if view_type == "Mapa Interativo":
        st.markdown("### 🗺️ Mapa de Preços por Bairro")
        
        # Dados mock para o mapa
        map_data = []
        for bairro in neighborhoods_list[:15]:  # Limitar para visualização
            import random
            avg_price = random.randint(2000, 4500)
            map_data.append({
                "Bairro": bairro,
                "Preço Médio": avg_price,
                "Latitude": -15.8 + random.uniform(-0.1, 0.1),
                "Longitude": -47.9 + random.uniform(-0.1, 0.1),
                "Imóveis": random.randint(10, 100)
            })
        
        df_map = pd.DataFrame(map_data)
        
        # Mapa de calor
        fig = px.scatter_mapbox(
            df_map,
            lat="Latitude",
            lon="Longitude",
            size="Preço Médio",
            color="Preço Médio",
            hover_name="Bairro",
            hover_data={"Preço Médio": ":.2f", "Imóveis": True},
            color_continuous_scale="Viridis",
            size_max=20,
            zoom=10,
            height=600,
            mapbox_style="open-street-map"
        )
        
        fig.update_layout(
            title="Distribuição de Preços Médios por Bairro",
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legenda
        st.info("💡 **Dica:** Quanto maior e mais escuro o ponto, maior o preço médio de aluguel na região")
        
    elif view_type == "Gráficos Comparativos":
        st.markdown("### 📈 Análises Comparativas")
        
        # Seleção de métrica
        metric = st.selectbox(
            "Métrica para Comparação",
            ["Preço Médio", "Preço por m²", "Número de Imóveis", "Variação Percentual"]
        )
        
        # Dados mock
        comparison_data = []
        for bairro in neighborhoods_list[:10]:
            import random
            comparison_data.append({
                "Bairro": bairro,
                "Preço Médio": random.randint(2000, 4500),
                "Preço por m²": random.randint(25, 50),
                "Número de Imóveis": random.randint(20, 150),
                "Variação Percentual": random.uniform(-5, 10)
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        df_comparison = df_comparison.sort_values(metric, ascending=False)
        
        # Gráfico de barras
        fig = px.bar(
            df_comparison.head(10),
            x="Bairro",
            y=metric,
            title=f"Top 10 Bairros - {metric}",
            color=metric,
            color_continuous_scale="Blues"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de distribuição
        st.markdown("### 📊 Distribuição de Preços")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma
            fig_hist = px.histogram(
                df_comparison,
                x="Preço Médio",
                nbins=20,
                title="Distribuição de Preços Médios",
                labels={"Preço Médio": "Preço Médio (R$)", "count": "Frequência"}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=df_comparison["Preço Médio"],
                name="Preço Médio",
                boxmean="sd"
            ))
            fig_box.update_layout(
                title="Distribuição Estatística de Preços",
                yaxis_title="Preço (R$)"
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Comparativo por tipo de imóvel
        st.markdown("### 🏘️ Comparativo por Tipo de Imóvel")
        
        tipo_data = []
        property_types_list = st.session_state.api_data.get('property_types', ['UNIT']) if st.session_state.api_data else ['UNIT']
        for tipo in property_types_list:
            import random
            tipo_data.append({
                "Tipo": tipo,
                "Preço Médio": random.randint(1500, 4000),
                "Área Média": random.randint(50, 150)
            })
        
        df_tipo = pd.DataFrame(tipo_data)
        
        fig_tipo = px.scatter(
            df_tipo,
            x="Área Média",
            y="Preço Médio",
            size="Preço Médio",
            color="Tipo",
            hover_name="Tipo",
            title="Relação Área vs Preço por Tipo"
        )
        
        st.plotly_chart(fig_tipo, use_container_width=True)
        
    else:  # Tabela de Dados
        st.markdown("### 📋 Dados Detalhados por Região")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            selected_bairros = st.multiselect(
                "Selecione os Bairros",
                neighborhoods_list,
                default=neighborhoods_list[:5] if len(neighborhoods_list) >= 5 else neighborhoods_list
            )
        
        with col2:
            sort_by = st.selectbox(
                "Ordenar por",
                ["Preço Médio", "Preço por m²", "Número de Imóveis"]
            )
        
        # Dados da tabela
        table_data = []
        for bairro in (selected_bairros if selected_bairros else neighborhoods_list):
            import random
            table_data.append({
                "Bairro": bairro,
                "Preço Médio": random.randint(2000, 4500),
                "Preço por m²": random.randint(25, 50),
                "Número de Imóveis": random.randint(20, 150),
                "Variação Mensal": f"{random.uniform(-5, 10):+.1f}%",
                "Tendência": random.choice(["↗️ Alta", "→ Estável", "↘️ Baixa"])
            })
        
        df_table = pd.DataFrame(table_data)
        df_table = df_table.sort_values(sort_by, ascending=False)
        
        # Formatação
        df_table["Preço Médio"] = df_table["Preço Médio"].apply(lambda x: helpers.format_currency(x))
        df_table["Preço por m²"] = df_table["Preço por m²"].apply(lambda x: helpers.format_currency(x))
        
        st.dataframe(
            df_table,
            column_config={
                "Bairro": "Bairro",
                "Preço Médio": "Preço Médio",
                "Preço por m²": "Preço por m²",
                "Número de Imóveis": "Imóveis",
                "Variação Mensal": "Variação",
                "Tendência": "Tendência"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Download
        csv = df_table.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="comparativo_regional.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    
    # Insights e recomendações
    st.markdown("### 💡 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Oportunidades:**
        - Bairros com boa relação custo-benefício identificados
        - Preços abaixo da média regional podem representar boas oportunidades
        """)
    
    with col2:
        st.warning("""
        **⚠️ Atenção:**
        - Verifique sempre a localização e infraestrutura do bairro
        - Considere custos adicionais como transporte e condomínio
        """)

# Executar quando o arquivo é executado diretamente pelo Streamlit
show()

