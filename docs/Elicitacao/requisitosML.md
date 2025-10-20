# Requisitos de Machine Learning 

## **1. Introdução**

Esta seção define os **Requisitos de Machine Learning (RML)** do projeto **PrediAluguel**, especificando o comportamento esperado dos modelos de IA utilizados para **predizer valores de aluguel de imóveis residenciais**.  

Os requisitos a seguir foram elaborados considerando **aspectos técnicos, éticos e operacionais** do ciclo de vida de aprendizado de máquina — desde a coleta de dados até a avaliação contínua do modelo em produção.

---

## **2. Requisitos de Dados (RML-D)**

| Código | Requisito | Descrição |
|:------:|------------|-----------|
| **RML-D01** | **Fontes de Dados Confiáveis** | Os dados de treinamento devem ser coletados exclusivamente de fontes públicas ou autorizadas, como **Kaggle (Zap Imóveis)**, **IBGE** e **APIs de geolocalização**. |
| **RML-D02** | **Qualidade dos Dados** | O conjunto de dados deve passar por etapas de **limpeza, padronização e tratamento de outliers**, assegurando a consistência e validade das informações. |
| **RML-D03** | **Balanceamento de Atributos** | O modelo deve evitar viés regional — garantindo que bairros ou cidades com menos amostras não prejudiquem as previsões. |
| **RML-D04** | **Atualização Periódica** | O dataset deve ser atualizado **pelo menos uma vez por trimestre**, refletindo variações do mercado imobiliário. |
| **RML-D05** | **Anonimização** | Nenhum dado sensível de indivíduos (como CPF, nome ou endereço exato) deve ser armazenado, em conformidade com a **LGPD**. |

<font size="2"><p style="text-align: center"><b>Fonte: <a href="https://github.com/gabriel-lima258">Gabriel Lima</a></b></p></font>


---

## **3. Requisitos de Modelagem (RML-M)**

| Código | Requisito | Descrição |
|:------:|------------|-----------|
| **RML-M01** | **Tipo de Aprendizado** | O modelo deve seguir o paradigma de **Aprendizado Supervisionado**, com foco em **Regressão** para estimativa numérica de valores de aluguel. |
| **RML-M02** | **Modelos Testados** | Devem ser avaliados pelo menos três algoritmos distintos: **Regressão Linear**, **Random Forest** e **XGBoost**. |
| **RML-M03** | **Feature Engineering** | O processo de treinamento deve incluir a criação e normalização de *features* derivadas (ex: preço por m², densidade demográfica, distância ao centro). |
| **RML-M04** | **Hiperparâmetros Otimizados** | A escolha de parâmetros deve ser automatizada via **Grid Search** ou **Random Search**, com validação cruzada (k-fold ≥ 5). |
| **RML-M05** | **Explicabilidade do Modelo** | O sistema deve gerar explicações locais das previsões, indicando quais variáveis mais impactaram o valor estimado (ex: **SHAP values** ou **Feature Importance**). |
| **RML-M06** | **Versionamento de Modelos** | Cada versão treinada do modelo deve ser registrada com data, hiperparâmetros e métricas de desempenho. |
| **RML-M07** | **Reprodutibilidade** | O treinamento deve ser totalmente reproduzível a partir de scripts e seeds fixas, garantindo consistência dos resultados. |

<font size="2"><p style="text-align: center"><b>Fonte: <a href="https://github.com/gabriel-lima258">Gabriel Lima</a></b></p></font>


---

## **4. Requisitos de Avaliação e Métricas (RML-A)**

| Código | Requisito | Descrição |
|:------:|------------|-----------|
| **RML-A01** | **Métricas de Avaliação** | O modelo deve ser avaliado usando **MAE (Mean Absolute Error)**, **RMSE (Root Mean Squared Error)** e **R² (Coeficiente de Determinação)**. |
| **RML-A02** | **Meta de Precisão** | O erro médio absoluto (MAE) deve ser inferior a **10%** do valor real do aluguel em dados de teste. |
| **RML-A03** | **Validação Cruzada** | O desempenho deve ser validado por **cross-validation** para reduzir overfitting e garantir robustez. |
| **RML-A04** | **Comparação entre Modelos** | O modelo final selecionado deve apresentar o **menor erro médio** e **maior estabilidade** entre múltiplos datasets de teste. |
| **RML-A05** | **Monitoramento Contínuo** | Após a implantação, as métricas de desempenho devem ser monitoradas periodicamente para detectar **degradação do modelo (drift)**. |
| **RML-A06** | **Feedback de Usuário** | As avaliações dos usuários (“correto”, “alto”, “baixo”) devem alimentar um módulo de **reajuste supervisionado** do modelo ao longo do tempo. |

<font size="2"><p style="text-align: center"><b>Fonte: <a href="https://github.com/gabriel-lima258">Gabriel Lima</a></b></p></font>


---

## **5. Requisitos Éticos e de Conformidade (RML-E)**

| Código | Requisito | Descrição |
|:------:|------------|-----------|
| **RML-E01** | **Transparência Algorítmica** | O sistema deve permitir ao usuário visualizar um resumo explicativo sobre como a IA chegou ao valor estimado. |
| **RML-E02** | **Imparcialidade** | O modelo não deve favorecer ou penalizar regiões específicas; qualquer viés identificado deve ser corrigido. |
| **RML-E03** | **Auditabilidade** | Todas as etapas de treinamento, avaliação e atualização do modelo devem ser registradas para auditoria. |
| **RML-E04** | **Conformidade Legal** | O uso dos dados deve seguir rigorosamente as normas da **LGPD** e das políticas de privacidade vigentes. |
| **RML-E05** | **Uso Responsável da IA** | O sistema deve apresentar avisos claros de que o valor fornecido é **uma estimativa**, não uma avaliação oficial. |

<font size="2"><p style="text-align: center"><b>Fonte: <a href="https://github.com/gabriel-lima258">Gabriel Lima</a></b></p></font>


---

## **6. Considerações Finais**

Os Requisitos de Machine Learning aqui descritos garantem que o **PrediAluguel** opere de forma **precisa, ética e escalável**, assegurando:

- **Confiabilidade técnica**, com modelos testados e reproduzíveis;  
- **Transparência**, com explicações compreensíveis sobre o raciocínio da IA;  
- **Evolução contínua**, com atualização periódica de dados e métricas;  
- **Conformidade ética e legal**, conforme a LGPD e boas práticas de IA responsável.  

Esses requisitos complementam os requisitos funcionais e não funcionais do sistema, compondo o **núcleo inteligente** do projeto.

---

## Histórico de versões
| Versão | Data | Descrição | Autor | Revisor
| :-: | :-: | :-: | :-: | :-:|
|`1.0`| 07/10/2025 | Criação da página | [Gabriel Lima](https://github.com/gabriel-lima258) | [Mateus](), [Elias]()|