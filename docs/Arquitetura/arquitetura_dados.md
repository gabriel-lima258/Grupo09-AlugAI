## Arquitetura de Dados

O projeto **AlugAI** é fundamentado em um *pipeline* de Machine Learning (MLOps) desenhado para garantir a precisão contínua da precificação de
alugéis em Brasília. Nossa arquitetura se concentra em um fluxo robusto de dados estruturados, desde a coleta, tratamento, qualidade dos dados, engenharia de *features* e a disponibilização do modelo via API para sistema web.

<p style="text-align:center"><b><a id="tab_1" style="visibility:hidden;"></a>Figura 1</b> – Diagrama da Arquitetura</p>

![Diagrama da Arquitetura](../assets/arquitetura/arquitetura_dados.PNG)

### Coleta de Dados

- A coleta será manual no inicio, combinando datasets estáticos do Kaggle (base) com scraping dinâmico de portais imobiliários do DF, onde a coleta dos datasets disponíveis do Kaggle será utilizado apenas uma vez para o treinamento e o scraping de dados ocorrerá mensalmente. Os dados brutos são armazenados localmente no inicio em formato csv, onde será rotulado como um DataLake e podendo evoluir para um bucket S3 na AWS.

- O projeto será automatizado no futuro utilizando DAG's do Airflow mensalmente para atualização dos dados do modelo de predição dos novos imóveis disponibilizados nos portais de aluguel de imóveis.

- Os portais de aluguel de imóveis escolhidos para scraping, foram:
    - https://www.dfimoveis.com.br/
    - https://www.zapimoveis.com.br/
    - https://www.olx.com.br/


*Tecnologias Utilizadas*

- Apache Airflow: Orquestração de pipelines
- Bibliotecas: kagglehub, selenium, beautifulsouap, pandas, requests, regex


### Dados Brutos

- Após a coleta (manual ou automatizada), todos os dados brutos são armazenados localmente em formato CSV, compondo o Data Lake inicial do projeto.

- Cada fonte (Kaggle, DF Imóveis, Zap Imóveis, OLX) possui uma pasta própria dentro do diretório data/raw/.

- Os arquivos seguem uma convenção de nomenclatura padronizada, incluindo o nome da fonte e a data de extração, no formato YYYYMMDD.

- Essa estrutura facilita o versionamento, auditoria e futura migração para o Amazon S3.

```
AlugAi/
│
├── data/
│   ├── raw/                      # Dados brutos (Data Lake local)
│   │   ├── kaggle/
│   │   │   ├── kaggle_alugueis_20251001.csv
│   │   │   └── kaggle_alugueis_20251002.csv
│   │   ├── dfimoveis/
│   │   │   ├── dfimoveis_20251024.csv
│   │   │   └── dfimoveis_20251124.csv
│   │   ├── zapimoveis/
│   │   │   └── zapimoveis_20251024.csv
│   │   └── olx/
│   │       └── olx_20251024.csv
```

### Tratamento e Qualidade dos dados

- Após a coleta e o armazenamento dos dados brutos na Camada Raw, é realizada a etapa combinada de Tratamento e Validação de Qualidade, garantindo que apenas dados limpos, padronizados e confiáveis avancem para a Camada Stage. Essa etapa é um Data Quality Gate, ou seja, um ponto de controle que só permite a promoção para a camada Stage os dados que atendam aos critérios de qualidade definidos.

- Aqui será realizado o tratamento e normalização dos dados. Também será definido regras de qualidade para o PyDeequ onde serão avaliados completude, consistência e faixas válidas.

- Em caso de falha, será salvo um log para revisão manual

*Tecnologias Utilizadas*

- Pandas, NumPy, PyDeequ, Regex, Logging


### Dados Tratados

- A Camada Stage representa o conjunto de dados já limpos, validados e aprovados pelo Data Quality Gate, sendo a principal fonte para o treinamento e re-treinamento do modelo de predição de preços de aluguel.

- Os dados armazenados nessa camada são considerados **confiáveis** e possuem estrutura padronizada, garantindo consistência para uso analítico e científico.

- Os dados serão gravados localmente para validação do MVP, após isto serão migrados para uma camada Stage no AWS S3.

- Os dados serão gravados em formato parquet.


### Inferência Modelo

- Após o processamento e a validação dos dados na Camada Stage, inicia-se a etapa de treinamento do modelo de Machine Learning, responsável por prever o valor de aluguel de imóveis no Distrito Federal.

- O modelo utiliza o XGBoost por sua eficiência em problemas tabulares e regressão supervisionada.

- Objetivos na inferência

    - Treinar um modelo de regressão robusto para estimar preços de aluguel;
    - Ajustar hiperparâmetros para maximizar o desempenho (R², RMSE);
    - Versionar e armazenar o modelo treinado para uso em inferências futuras;
    - Permitir re-treinamentos automáticos conforme novos dados são coletados.


*Tecnologias Utilizadas*

- XGBoost, Pandas, Scikit-learn, Pickle

- Evolução para Cloud: SageMaker

## Histórico de versões
| Versão | Data | Descrição | Autor | Revisor
| :-: | :-: | :-: | :-: | :-:|
|`1.0`| 19/10/2025 | Criação do documento de Engenharia de Dados| [Mateus]() | |
|`1.1`| 25/10/2025 | Melhoria da Arquitetura e Descrição| [Mateus]() | |