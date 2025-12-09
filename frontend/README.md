# AlugAI - Frontend Streamlit

Frontend desenvolvido em Streamlit para o sistema AlugAI de precificação de aluguel de imóveis no Distrito Federal.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Navegue até o diretório do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

Execute o aplicativo Streamlit:
```bash
streamlit run app.py
```

O aplicativo estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
frontend/
├── app.py                 # Aplicação principal
├── pages/                 # Páginas do aplicativo
│   ├── __init__.py
│   ├── home.py            # Página inicial
│   ├── buscar_imoveis.py  # Busca de imóveis
│   ├── estimativa_preco.py # Estimativa de preço
│   ├── comparativo_regional.py # Comparativo regional
│   ├── historico.py       # Histórico de consultas
│   └── sobre.py           # Sobre o projeto
├── utils/                 # Utilitários
│   ├── __init__.py
│   ├── config.py          # Configurações
│   └── helpers.py         # Funções auxiliares
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🎯 Funcionalidades

- **Busca de Imóveis**: Formulário completo com filtros avançados
- **Estimativa de Preço**: Cálculo de preço usando modelo de ML
- **Comparativo Regional**: Visualizações e análises por região
- **Histórico**: Armazenamento de consultas anteriores
- **Interface Responsiva**: Design moderno e intuitivo

## 🔧 Tecnologias

- **Streamlit**: Framework para aplicações web em Python
- **Pandas**: Manipulação de dados
- **Plotly**: Visualizações interativas
- **NumPy**: Operações numéricas

## 📝 Notas

- Os dados exibidos são mock para desenvolvimento
- Integração com modelo de ML será implementada posteriormente
- Histórico é armazenado em sessão (não persistente)

## 👥 Desenvolvido por

Equipe AlugAI - UnB 2025




