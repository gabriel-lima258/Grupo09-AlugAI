"""
Página sobre o projeto
"""

import streamlit as st
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para importações
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from utils import config

# Configuração da página
config.set_page_config()
config.apply_custom_css()

# Inicialização de sessão
if 'consultas' not in st.session_state:
    st.session_state.consultas = []
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

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
    """Exibe a página sobre"""
    
    st.title("ℹ️ Sobre o AlugAI")
    
    st.markdown("---")
    
    # Logo e apresentação
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        from pathlib import Path
        logo_path = Path(__file__).parent.parent.parent / "docs" / "assets" / "logo_agente.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.title("🏠 AlugAI")
    
    st.markdown("""
    ## 🎯 Sobre o Projeto
    
    O **AlugAI** é uma aplicação web desenvolvida como parte da disciplina **"Tópicos Especiais de Engenharia de Software"** 
    da **Universidade de Brasília (UnB)**, ministrada pela professora **Carla Rocha**.
    
    O sistema utiliza modelos de **Machine Learning** para aprender padrões do mercado imobiliário e gerar estimativas 
    rápidas, confiáveis e transparentes de valores de aluguel no **Distrito Federal**.
    
    ### 🎯 Objetivos
    
    - ✅ Apresentar imóveis vantajosos para locação de acordo com as preferências do usuário
    - ✅ Fornecer comparativos de mercado por bairro e cidade
    - ✅ Prover feedback estruturado sobre custo x benefício de imóveis
    - ✅ Fornecer comparativo analisando flutuações de mercado sobre valores de imóveis similares
    
    ### 🚀 Tecnologias Utilizadas
    
    **Back-end / Machine Learning:**
    - Python
    - Scikit-learn
    - Pandas
    - XGBoost
    
    **Front-end:**
    - Streamlit
    
    **Banco de Dados:**
    - SQLite
    - CSVs públicos
    
    **Infraestrutura:**
    - GitHub Pages (documentação)
    - MkDocs
    
    """)
    
    st.markdown("---")
    
    # Equipe
    st.markdown("## 👥 Equipe de Desenvolvimento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f8f9fa;color: #1f2c33; border-radius: 10px;'>
            <h3>Gabriel Lima</h3>
            <p>Desenvolvedor Full-Stack / IA</p>
            <p><a href='https://github.com/gabriel-lima258'>@gabriel-lima258</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f8f9fa;color: #1f2c33; border-radius: 10px;'>
            <h3>Elias Oliveira</h3>
            <p>Engenharia de Dados / ML</p>
            <p><a href='https://github.com/EliasOliver21'>@EliasOliver21</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f8f9fa;color: #1f2c33; border-radius: 10px;'>
            <h3>Mateus Vasconcelos</h3>
            <p>Engenharia de Dados</p>
            <p><a href='https://github.com/mateusvasconcelos182'>@mateusvasconcelos182</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Funcionalidades principais
    st.markdown("## 🔧 Funcionalidades Principais")
    
    features = [
        {
            "icon": "🔍",
            "title": "Busca Inteligente",
            "description": "Sistema de busca com filtros avançados e classificação automática de imóveis"
        },
        {
            "icon": "💰",
            "title": "Estimativa de Preço",
            "description": "Modelo de IA para estimar valores de aluguel baseado em características do imóvel"
        },
        {
            "icon": "📊",
            "title": "Comparativo Regional",
            "description": "Análises e visualizações de preços por região no Distrito Federal"
        },
        {
            "icon": "🎯",
            "title": "Classificação Custo-Benefício",
            "description": "Sistema automático que identifica imóveis vantajosos baseado em regras de negócio"
        },
        {
            "icon": "📜",
            "title": "Histórico de Consultas",
            "description": "Armazenamento e visualização do histórico de buscas e estimativas"
        },
        {
            "icon": "🔍",
            "title": "Explicabilidade da IA",
            "description": "Visualização dos fatores que influenciaram a estimativa de preço"
        }
    ]
    
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        with col1:
            feat = features[i]
            st.markdown(f"""
            <div style='padding: 1.5rem; background-color: #f0f2f6;color: #1f2c33; border-radius: 10px; height: 100%;'>
                <h3>{feat['icon']} {feat['title']}</h3>
                <p>{feat['description']}</p>
            </div>
            <br>
            """, unsafe_allow_html=True)
        
        if i + 1 < len(features):
            with col2:
                feat = features[i + 1]
                st.markdown(f"""
                <div style='padding: 1.5rem; background-color: #f0f2f6;color: #1f2c33; border-radius: 10px; height: 100%;'>
                    <h3>{feat['icon']} {feat['title']}</h3>
                    <p>{feat['description']}</p>
                </div>
                <br>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Informações técnicas
    st.markdown("## 🔬 Informações Técnicas")
    
    st.markdown("""
    ### Modelo de Machine Learning
    
    - **Tipo:** Regressão Supervisionada
    - **Algoritmo:** XGBoost
    - **Métricas de Avaliação:** MAE, RMSE, R²
    - **Precisão:** Erro médio absoluto abaixo de 10%
    
    ### Fontes de Dados
    
    - Kaggle (Zap Imóveis Dataset)
    - Scraping de portais imobiliários (DF Imóveis, Zap Imóveis, OLX)
    - Dados públicos do IBGE
    
    ### Arquitetura
    
    - Pipeline de dados estruturado (Data Lake → Stage → Modelo)
    - Tratamento e validação de qualidade de dados
    - Feature Engineering automatizado
    - Versionamento de modelos
    """)
    
    st.markdown("---")
    
    # Contato e suporte
    st.markdown("## 📞 Contato e Suporte")
    
    st.info("""
    **Dúvidas ou sugestões?**
    
    - 📧 Entre em contato através do GitHub do projeto
    - 📚 Consulte a documentação completa em: [Documentação AlugAI](https://unb-sistemas-de-machine-learning.github.io/Grupo09-AlugAI/)
    - 🐛 Reporte problemas através das Issues do GitHub
    """)
    
    st.markdown("---")
    
    # Licença
    st.markdown("## 📄 Licença")
    
    st.markdown("""
    Este projeto é de uso **acadêmico e educacional**, desenvolvido como parte de uma disciplina da 
    Universidade de Brasília (UnB).
    
    Sinta-se à vontade para estudar, adaptar e expandir a solução.
    """)
    
    st.markdown("---")
    
    # Versão
    st.markdown("**Versão:** 1.0.0  |  **Última atualização:** Outubro 2025")

# Executar quando o arquivo é executado diretamente pelo Streamlit
show()

