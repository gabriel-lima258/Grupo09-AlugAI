# Histórias de Usuário

## Introdução

Este artefato tem o objetivo de documentar as histórias de usuário geradas a partir dos [requisitos elicitados](./requisitosProduto.md) e atribuidas aos temas e épicos no artefado de [backlog](./backlog.md).

## Metodologia

As histórias do usuário são apresentadas na tabela 1 abaixo, com a rastreabilidade dos requisitos e os criérios de aceitação.

## Histórias de Usuário

|ID História|Épicos|Título|História de Usuário| Critérios de Aceitação |Rastreabilidade|
|:--:|:--:|:--:|:--:|:--:|:---:|
|**US01**|**EP01**|Inserir informações do imóvel|Eu, como usuário, desejo inserir características que almejo em um imóvel para locar.| É apresentado campos para inserção das características do imóvel| **RF02** |
|**US02**|**EP02**|Visualizar imóveis vantajosos|Como usuário, eu desejo visualizar imóveis que estejam dentro da minhas expectativas e sejam vantajosos.| Os anúncios são apresentados categorizados, como vantajosos ou não vantajoso, de acordo com as regras de negócio. | **RF02** |
|**US03**|**EP02**|Visualizar anúncios de acordo com preferências|Como usuário, eu desejo visualizar anúncios de alugueis que estejam dentro da minhas expectativas.| Os anúncios devem ser filtrados com as preferências inseridas pelo usuário e depois listados. |**RF02** |
|**US04**|**EP03**|Visualizar classificação de imóveis| EU, como usuário, desejo visualizar classificações e destaques chaves nos anúncios dos imóveis.| Os anúncios devem ser listados e apresentados com algumas classificações básicas, como vantajoso ou não vantajoso, muito recente e outros.| **RF03** |
|**US05**|**EP03**|Visualizar destaques chaves de cada anúncio|Eu, como usuário, desejo visualizar destaques chaves de cada anúncio.| Os anúncios devem apresentar informações básicas do imóvel para fácil entendimento, como número de quartos, pussui garem, quantidade de suites e etc. | **RF010** |
|**US06**|**EP04**|Obter estimativa de preço justo de aluguel |Eu, como usuário, desejo obter uma estimativa do preço de um imóvel. | O modelo de I.A deve predizer o valor de um aluguel para um imóvel da listagem ou para um imóvel não listado, com informações que o usuário fornecer. | **RF01** |
|**US07**|**EP04**|Mensuração do valor do aluguel| Eu, como usuário, desejo obter a mensuração do valor do aluguel de um imóvel. |O modelo de I.A deve realizar a mensuração do valor do aluguel de um imóvel, comparando as características do imóvel em questão, com a dos dados utilizados no treinamento.| **RF01** |
|**US08**|**EP05**|Análise de imóveis| Eu, como usuário, desejo obter análises de anúncios de alugueis e os pontos positivos e negativos em locar o imóvel em questão. | O modelo de I.A integrado a uma LLM, deve realizar uma análise e comparação de imoveis e apresentar os pontos positivos e negativos para uma tomada de decisão do cliente. | **RF03** | **RF01** |
|**US09**|**EP06**|Comparação de preço anunciado pelo sugerido pelo modelo de I.A| Eu, como usuário, desejo obter uma comparação entre o preço anunciado e o valor do aluguel previsto pelo modelo de I.A | A interface deve apresentar o preço do anúncio e o preço previsto pelo modelo de I.A e realizar uma comparação entre eles. | **RF03** |
|**US10**|**EP07**|Acesso a anúncios atualizados| Eu, como usuário, desejo ter acesso aos anúncios de locação de imóveis mais atuais. | O sistema deve realizar constantes buscas e scraps de dados para alimentar o banco de dados com anúncios mais recentes de locação de imóveis. | **RF09** |
|**US11**|**EP08**|Receber feedback sobre custo-benefício | Eu, como usuário, desejo obter um feedback sobre a relação custo / benefício em locar um imóvel específico. | O sistema deve fornecer uma opção de feedback para o usuário do quão benéfico e vantajoso é locar um imóvel específico. | **RF01** |


## Bibliografia

> 1. 2024.1-Requisitos de software - Correios. Disponível em: <https://github.com/EliasOliver21/2024.1-Correios-Requisitos-de-Software/blob/main/docs/modelagem/agil/backlog.md>. Acesso em: 7 de Abril de 2024.

## Histórico de versões
| Versão | Data | Descrição | Autor | Revisor
| :-: | :-: | :-: | :-: | :-:|
|`1.0`| 19/10/2025 | Criação do documento | [Elias Oliveira](https://github.com/EliasOliver21) | []()|'