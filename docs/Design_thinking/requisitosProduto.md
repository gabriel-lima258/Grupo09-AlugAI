# Requisitos do Produto

## **1. Introdução**

O presente documento tem como objetivo apresentar os **requisitos funcionais e não funcionais** do sistema **PrediAluguel**, utilizando a técnica de análise documental. Para a elicitação destes requisitos, foram analisados os artefatos produzidos por meio de brainstorming com o framework [Design Thinking](design_thinking.md)

Os requisitos descritos a seguir foram elaborados com foco em **funcionalidade, precisão, desempenho e usabilidade**, garantindo que a solução atenda às expectativas do público e às boas práticas de engenharia de software.

---

## **2. Requisitos Funcionais (RF)**

| Código | Requisito | Descrição |
|:------:|------------|-----------|
| **RF01** | **Estimativa de Aluguel** | O sistema deve calcular o valor estimado de aluguel a partir dos dados fornecidos pelo usuário. |
| **RF02** | **Entrada de Dados** | O usuário deve poder inserir informações do imóvel (metragem, bairro, número de quartos, tipo, vagas etc.) por meio de uma interface web simples. |
| **RF03** | **Comparativo Regional** | O sistema deve exibir a média de aluguel da região consultada e indicar se o valor estimado está acima, dentro ou abaixo da média. |
| **RF04** | **Histórico de Consultas** | O sistema deve armazenar o histórico de pesquisas para que o usuário possa revisitar suas consultas. |
| **RF05** | **Feedback de Precisão** | O sistema deve permitir que o usuário avalie se a estimativa foi adequada (“Correta”, “Alta”, “Baixa”). |
| **RF06** | **Mapa Interativo** | O sistema deve apresentar um mapa com a variação média dos valores de aluguel por bairro ou cidade. |
| **RF07** | **Chat de Suporte** | O sistema deve oferecer um chatbot para esclarecer dúvidas sobre o uso e funcionamento da aplicação. |
| **RF08** | **API de Consulta** | O sistema deve disponibilizar uma API REST pública para que outras plataformas imobiliárias consultem as estimativas. |
| **RF09** | **Atualização de Dados** | O sistema deve atualizar automaticamente sua base de dados (ex: Kaggle, IBGE, portais públicos) de forma periódica. |
| **RF10** | **Explicabilidade da IA** | O sistema deve exibir os principais fatores que influenciaram a previsão (ex: localização, área, número de quartos). |

---

## **3. Requisitos Não Funcionais (RNF)**

| Código | Categoria | Descrição |
|:------:|------------|-----------|
| **RNF01** | **Desempenho** | O tempo médio de resposta da previsão não deve ultrapassar **10 segundos** em 95% das requisições. |
| **RNF02** | **Precisão** | O erro médio absoluto (MAE) do modelo deve permanecer abaixo de **10%** em relação aos valores reais. |
| **RNF03** | **Disponibilidade** | O sistema deve estar disponível **99,5% do tempo**, exceto durante manutenções programadas. |
| **RNF04** | **Usabilidade** | A interface deve ser responsiva, intuitiva e fácil de usar em dispositivos móveis e desktop. |
| **RNF05** | **Escalabilidade** | O sistema deve suportar aumento de até **10 vezes o número de usuários simultâneos** sem degradação perceptível. |
| **RNF06** | **Segurança e Privacidade** | O sistema deve seguir a **LGPD**, garantindo a proteção dos dados de usuários e das informações processadas. |
| **RNF07** | **Manutenibilidade** | O código deve ser modular, bem documentado e de fácil atualização para inclusão de novas fontes de dados. |
| **RNF08** | **Compatibilidade** | O sistema deve ser compatível com os principais navegadores (Chrome, Edge, Firefox, Safari). |
| **RNF09** | **Acessibilidade** | O conteúdo deve seguir as diretrizes **WCAG 2.1**, garantindo legibilidade e compatibilidade com leitores de tela. |
| **RNF10** | **Identidade e Tom de Voz** | O chatbot e as mensagens devem manter um tom **neutro, explicativo e confiável**, reforçando a credibilidade da aplicação. |

<font size="2"><p style="text-align: center"><b>Fonte: <a href="https://github.com/gabriel-lima258">Gabriel Lima</a></b></p></font>

---

## **4. Considerações Finais**

Os requisitos apresentados constituem a **base para o desenvolvimento e validação** do sistema **PrediAluguel**.  
Eles garantem que a aplicação não apenas forneça previsões precisas, mas também **entregue valor real ao usuário**, com foco em:

- **Transparência:** explicações claras sobre como o valor é estimado.  
- **Confiabilidade:** uso de dados públicos e fontes verificadas.  
- **Acessibilidade:** interface intuitiva e disponível para todos os públicos.  

O cumprimento destes requisitos assegura que o **PrediAluguel** se destaque como uma solução tecnológica relevante e socialmente útil no contexto do mercado imobiliário brasileiro.

---

## Histórico de versões
| Versão | Data | Descrição | Autor | Revisor
| :-: | :-: | :-: | :-: | :-:|
|`1.0`| 07/10/2025 | Criação da página | [Gabriel Lima](https://github.com/gabriel-lima258) | [Mateus][MateusGH], [Elias][EliasGH] |


[MateusGH]: https://github.com/mateusvasconcelos182
[GabrielGH]: https://github.com/gabriel-lima258
[EliasGH]: https://github.com/EliasOliver21