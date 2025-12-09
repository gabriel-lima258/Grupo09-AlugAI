<div align='center'>
  <h1>🏠 AlugAI</h1>
  <p><strong>Sistema de Precificação Inteligente de Aluguel de Imóveis</strong></p>
  <p>Estimativa de preços de aluguel usando Machine Learning | Distrito Federal</p>
</div>

<div align="center">
  <img src="docs/assets/logo_agente.png" alt="Logo AlugAI" style="max-width: 25%; height: auto; margin-bottom: 15px;">
  <p><strong>Figura 1:</strong> Logo da aplicação</p>
  <p><em>Fonte: <a href="https://www.flaticon.com/br/" target="_blank">Flaticon</a>, 2025</em></p>
</div>

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Deploy](#deploy)
- [Documentação](#documentação)
- [Equipe](#equipe)

---

## 🎯 Sobre o Projeto

O **AlugAI** é uma aplicação web com integração de Inteligência Artificial que possibilita:

- ✅ **Estimar o valor justo** de aluguel de imóveis no Distrito Federal
- ✅ **Buscar e comparar** imóveis do mercado
- ✅ **Visualizar análises** regionais de preços
- ✅ **Interface moderna** e intuitiva

A iniciativa nasce com o propósito de **reduzir a assimetria de informações** no setor imobiliário, prover uma facilitação da análise do **custo x benefício** de um imóvel e promover **transparência, acessibilidade e eficiência** para locadores e locatários.

---

## 🛠️ Tecnologias

### Backend / Machine Learning
- **Python 3.8+**
- **XGBoost**: Modelo de regressão para predição
- **Scikit-learn**: Pipeline de ML e avaliação
- **Pandas**: Processamento de dados
- **Flask**: API REST
- **Flask-CORS**: Integração frontend-backend

### Frontend
- **Streamlit**: Framework web em Python
- **Plotly**: Visualizações interativas
- **Pandas**: Manipulação de dados
- **Requests**: Comunicação com API

### Infraestrutura
- **GitHub**: Controle de versão
- **Render**: Deploy do backend
- **Streamlit Cloud**: Deploy do frontend
- **MkDocs**: Documentação

### Design
- **Figma**: Prototipação
- **Miro**: Design Thinking
- **Canva**: Assets visuais

---

## 📁 Estrutura do Projeto

```
Grupo09-AlugAI/
├── backend/                    # Backend ML e API
│   ├── src/                    # Código fonte
│   │   ├── data_processing.py  # Processamento de dados
│   │   └── model_trainer.py    # Treinamento do modelo
│   ├── api/                    # API REST
│   │   └── app.py             # Servidor Flask
│   ├── models/                 # Modelos treinados
│   ├── train_model.py         # Script de treinamento
│   └── requirements.txt       # Dependências
│
├── frontend/                   # Frontend Streamlit
│   ├── app.py                 # Aplicação principal
│   ├── pages/                 # Páginas do app
│   │   ├── estimativa_preco.py
│   │   ├── buscar_imoveis.py
│   │   ├── comparativo_regional.py
│   │   ├── historico.py
│   │   └── sobre.py
│   ├── utils/                 # Utilitários
│   └── requirements.txt       # Dependências
│
├── data/                       # Datasets
│   └── imoveis-df.csv         # Dataset de treinamento
│
├── docs/                       # Documentação
│   ├── Arquitetura/
│   ├── Elicitacao/
│   ├── Design_thinking/
│   └── assets/
│
└── README.md                   # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/unb-Sistemas-de-Machine-learning/Grupo09-AlugAI.git
   cd Grupo09-AlugAI
   ```

2. **Instale as dependências do backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Instale as dependências do frontend:**
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   ```

4. **Para macOS (se necessário para XGBoost):**
   ```bash
   brew install libomp
   ```

---

## ▶️ Como Executar

### 1. Treinar o Modelo (Backend)

```bash
cd backend
python train_model.py
```

Isso irá:
- Processar o dataset `data/imoveis-df.csv`
- Treinar o modelo XGBoost
- Salvar o modelo em `backend/models/`

### 2. Iniciar a API (Backend)

```bash
cd backend/api
python app.py
```

A API estará disponível em: `http://localhost:5020`

**Endpoints principais:**
- `GET /health` - Health check
- `POST /predict` - Predição de preço
- `GET /data/properties` - Lista de imóveis
- `GET /data/unique-values` - Valores únicos

### 3. Iniciar o Frontend

**Terminal separado:**
```bash
cd frontend
streamlit run app.py
```

O frontend estará disponível em: `http://localhost:8501`

---

## 🌐 Deploy

### Backend - Render

1. **Acesse:** https://render.com
2. **Conecte** seu repositório GitHub
3. **Configure:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api/app.py`
4. **Deploy automático** a cada push

**URL do Backend:** https://alugai.onrender.com

### Frontend - Streamlit Cloud

1. **Acesse:** https://streamlit.io/cloud
2. **Conecte** seu repositório GitHub
3. **Configure:**
   - **Main file path**: `frontend/app.py`
4. **Configure Secrets:**
   - `API_URL = "https://alugai.onrender.com"`
5. **Deploy automático** a cada push

**URL do Frontend:** https://alugai.streamlit.app

### Guias Detalhados

- **Backend:** Veja `backend/README.md`
- **Frontend:** Veja `frontend/README.md`

---

## 📊 Funcionalidades

### 🎯 Estimativa de Preço
- Formulário completo de entrada
- Predição em tempo real via ML
- Visualização gráfica
- Histórico de consultas

### 🔍 Busca de Imóveis
- Carrega todos os imóveis do dataset
- Filtros opcionais (tipo, bairro, área, preço)
- Paginação
- Classificação de custo-benefício
- Estimativa de preço para cada imóvel

### 📈 Comparativo Regional
- Análise por região
- Gráficos interativos
- Distribuição de preços
- Comparação por tipo

### 📝 Histórico
- Consultas anteriores
- Filtros e busca
- Exportação

---

## 📚 Documentação

### Documentação Completa

A documentação oficial do projeto (incluindo artefatos do framework PIM-Go e Machine Learning Canvas) está disponível em:

**[📖 Acesse a Documentação do AlugAI](https://unb-sistemas-de-machine-learning.github.io/Grupo09-AlugAI/)**

### READMEs Específicos

- **[Backend README](backend/README.md)**: Detalhes sobre ML, API, treinamento
- **[Frontend README](frontend/README.md)**: Detalhes sobre Streamlit, páginas, integração

---

## 🤖 Modelo de Machine Learning

### Algoritmo
- **XGBoost Regressor**: Gradient Boosting para regressão

### Métricas
- **MAE**: Erro médio absoluto
- **RMSE**: Raiz do erro quadrático médio
- **R²**: Coeficiente de determinação

### Features
- Área, quartos, banheiros, vagas
- Tipo de imóvel, bairro, cidade
- Condomínio, mobiliado
- Preço por m² (derivada)

### Dataset
- **Fonte**: `data/imoveis-df.csv`
- **Registros**: ~2.858 imóveis
- **Região**: Distrito Federal

---

## 👥 Equipe de Desenvolvimento

<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/gabriel-lima258">
        <img style="border-radius: 50%;" src="https://github.com/gabriel-lima258.png" width="100px;" alt=""/><br/>
        <sub><b>Gabriel Lima</b></sub>
      </a><br/>
      <sub>Desenvolvedor Full-Stack / IA</sub>
    </td>
    <td align="center">
      <a href="https://github.com/EliasOliver21">
        <img style="border-radius: 50%;" src="https://github.com/EliasOliver21.png" width="100px;" alt=""/><br/>
        <sub><b>Elias Oliveira</b></sub>
      </a><br/>
      <sub>Engenharia de Dados / ML</sub>
    </td>
    <td align="center">
      <a href="https://github.com/mateusvasconcelos182">
        <img style="border-radius: 50%;" src="https://github.com/mateusvasconcelos182.png" width="100px;" alt=""/><br/>
        <sub><b>Mateus Vasconcelos</b></sub>
      </a><br/>
      <sub>Engenharia de Dados</sub>
    </td>
  </tr>
</table>

</div>

---

## 🎓 Contexto Acadêmico

Projeto desenvolvido como parte da disciplina  
**Tópicos Especiais de Engenharia de Software – FCTE / Universidade de Brasília (UnB)**  
**Professora:** Carla Rocha

---

## 📄 Licença

Este projeto é de uso **acadêmico e educacional**, distribuído sob a licença MIT.  
Sinta-se à vontade para estudar, adaptar e expandir a solução.

---

## 🔗 Links Úteis

- **Documentação:** https://unb-sistemas-de-machine-learning.github.io/Grupo09-AlugAI/
- **Backend Deploy:** https://alugai.onrender.com
- **Frontend Deploy:** https://alugai.streamlit.app
- **Repositório:** https://github.com/unb-Sistemas-de-Machine-learning/Grupo09-AlugAI

---

## 🆘 Suporte

Para dúvidas ou problemas:

1. **Consulte os READMEs específicos:**
   - `backend/README.md`
   - `frontend/README.md`

2. **Verifique a documentação completa** no link acima

3. **Abra uma issue** no repositório GitHub

---

<div align="center">
  <p>Feito com ❤️ por <a href="https://github.com/gabriel-lima258">Gabriel Lima</a> e equipe AlugAI</p>
  <p>UnB 2025</p>
</div>
