## Arquitetura de Dados

O projeto **PrediAluguel** é fundamentado em um *pipeline* de Machine Learning (MLOps) desenhado para garantir a precisão contínua da precificação de aluguéis em Brasília. Nossa arquitetura se concentra em um fluxo robusto de dados estruturados, desde a coleta e engenharia de *features* até a disponibilização do modelo via API para o sistema web.

<p style="text-align:center"><b><a id="tab_1" style="visibility:hidden;"></a>Figura 1</b> – Diagrama da Arquitetura</p>

![Diagrama da Arquitetura](../assets/arquitetura/arquitetura_macro.png)



## Engenharia de Dados


#### Coleta e Armazenamento dos Dados

A coleta é semi-automatizada, combinando datasets estáticos do Kaggle (base) com scrapping dinâmico de portais imobiliários do DF (complemento e Série Temporal). Os dados brutos são armazenados no Google Drive/Cloud Storage.

O projeto utilizará de DAG's Airflow quinzenalmente/mensalmente para atualizar dados do modelo.

### Técnicas de Amostragem

Não foi utilizado técnicas de amostragem, visto que nosso MVP é focado no público específico de Brasília.

### Rotulação e Balanceamento

Não houve rotulação manual. O problema de Classificação (Custo-Benefício) é resolvido através da criação da Métrica Estatística/Regras de Negócio. O alvo principal (rent_amount) é intrinsecamente rotulado nos dados brutos. O modelo de Classificação é substituído por um Motor de Regras baseado no Modelo de Regressão.

### Balanceamento de Classes

Não. O foco é em modelos de Regressão (Precificação e Previsão), que não lidam com classes desbalanceadas. A distribuição do Target (rent_amount) será tratada com técnicas de Normalização e Tratamento de Outliers.

### Data Augmentation

Não realizamos o Data Augmentation clássico. Nossa estratégia para mitigar a falta de dados (especialmente dados históricos detalhados do DF) foi feita em duas etapas:
1. Coleta Aumentada (Scraping): O web scraping foi essencial para aumentar o dataset em volume e em features, capturando variáveis que não estavam nas bases do Kaggle (ex: valor por metro quadrado, iptu, etc.).
2. Enriquecimento de Features: Utilizamos a Engenharia de Features (Ex: price_per_sqm, densidade de ofertas por bairro) para extrair o valor preditivo máximo dos dados de localização, compensando a falta de volume com maior inteligência na modelagem.

### Feature Engineering

- **Missing Values**: Tratamento por tipo de variável: Para colunas numéricas (hoa), será utilizada a Mediana por região. Para colunas categóricas (furniture), a estratégia é Moda ou criação da categoria "Desconhecido".
- **Outliers**: Utilização da métrica IQR (Interval Range Quartile) para identificar e tratar/remover valores extremos no Target (rent_amount) e em features chave (area), que poderiam distorcer a Regressão Linear.
- **Enriquecimento dos Dados**: Criação da feature price_per_sqm. Integração de dados de infraestrutura local (distância a pontos de interesse, estações de metrô) e socioeconômicos (renda média/IDH por região).
- **Excluir Variáveis Inúteis**: Remoção de colunas com alta cardinalidade e pouca correlação (Ex: ID ou full_address - após a extração da localização).
- **Normalização e Padronização**: Padronização (StandardScaler) ou Normalização (MinMaxScaler) aplicada a variáveis com grande amplitude (area, hoa) para otimizar o desempenho de modelos sensíveis à escala (como a Regressão Linear).
- **One Hot Encoding (OHE)**: Aplicado a todas as variáveis categóricas de baixa cardinalidade (Ex: furniture, city). Para neighborhood (alta cardinalidade), será testado o OHE em combinação com a Agregação/Grouping de bairros menos representativos.
- **Dados de Teste e Treinamento**: Separação em 70% Treino, 15% Validação e 15% Teste. A validação será usada para tuning dos hiperparâmetros e o teste final para avaliação imparcial do modelo.
