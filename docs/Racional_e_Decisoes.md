# Racional e decisões

**Quantum Finance — Machine Learning · Segmentação de clientes por valor e custo de servir com K-means**

Este documento acompanha o notebook do trabalho. O notebook mostra o que foi feito e o resultado. Aqui fica registrado **por que** cada escolha foi feita, quais alternativas foram consideradas e o que faria a decisão mudar. As seções citadas são as do notebook.

## 1. Como lemos o enunciado

O enunciado pede o planejamento e a proposta de aplicação de **uma** arquitetura **estudada na disciplina** a um problema real da empresa. Três consequências guiaram o trabalho.

| O que o enunciado diz | Como respondemos |
|---|---|
| É uma proposta, não um sistema pronto | o código é uma prova de conceito; consumo, riscos e roteiro são texto |
| A arquitetura deve ser uma das estudadas | escolhemos entre regressão linear, KNN, K-means, Apriori, séries temporais e Q-learning (Seção 2.2) |
| Quatro tópicos obrigatórios | são as quatro seções do notebook, na mesma ordem e com o mesmo nome |
| Avalia-se a justificativa técnica | cada escolha tem uma evidência executada, e a comparação com alternativas é um experimento, não uma afirmação |
| Avalia-se originalidade e aderência ao contexto | partimos do exercício da Aula 3 e tratamos o que ele deixou em aberto; o recorte liga a segmentação às três dores do enunciado |

## 2. Registro das decisões

Cada decisão segue o mesmo formato: a pergunta, as alternativas, o que foi decidido e por quê, onde está a evidência e o que mudaria a decisão.

### D1. Formato da entrega

* **Alternativas:** slides; documento escrito; notebook.
* **Decisão:** um notebook narrativo e executado, exportado também em PDF, mais este documento de apoio.
* **Por quê:** dois dos quatro critérios de avaliação pedem evidência (justificativa técnica e profundidade). Em um notebook a comparação com alternativas é executada à vista de quem lê. O PDF cumpre o papel de documento escrito para quem não quer abrir o código.
* **O que mudaria:** se a entrega exigisse apresentação oral, um conjunto curto de slides derivado das figuras do notebook.

### D2. Qual desafio

* **Alternativas:** (1) scoring de produtos e risco de ruptura; (2) detecção de anomalias e fraudes; (3) segmentação de clientes.
* **Decisão:** segmentação de clientes.
* **Por quê:** as três dores do enunciado (suporte, logística, marketing) têm a mesma origem: decidir como tratar cada cliente. Uma segmentação atende às três. O desafio também tem correspondência direta com uma arquitetura da disciplina (K-means, Aula 3) e com dados públicos reais.
* **Por que não os outros:** risco de ruptura pede dados de estoque, que as bases públicas de varejo não trazem; seria preciso simular. Para fraude, a arquitetura estudada mais próxima é o KNN, que os slides da Aula 2 descrevem como de alto custo computacional, difícil de defender em escala.
* **O que mudaria:** acesso a dados de estoque ou a transações rotuladas como fraude.

### D3. O recorte: valor × custo de servir

* **Alternativas:** segmentação clássica por valor (RFM); segmentação que inclui o custo de atender.
* **Decisão:** incluir o comportamento de estorno como dimensão de custo de servir.
* **Por quê:** o RFM clássico serve ao marketing e deixa suporte e logística de fora. O enunciado cita os três. O estorno é o sinal de custo disponível na base.
* **Evidência:** os segmentos B e C têm a mesma mediana de pedidos; B quase não estorna e C gera 37% das faturas de estorno com 12% da receita (Seção 3.9).
* **O que mudaria:** com dados de atendimento e de frete, o custo de servir seria medido diretamente.

### D4. A arquitetura: K-means

* **Alternativas dentro da disciplina:** regressão linear, KNN, Apriori, séries temporais, Q-learning.
* **Alternativas de agrupamento:** régua manual (curva ABC, RFM por faixas), hierárquico (Ward), DBSCAN, GMM.
* **Decisão:** K-means.
* **Por quê:** o problema não tem rótulo, e o K-means é a arquitetura da disciplina que agrupa clientes. Tem custo aproximadamente linear, o centroide é o próprio perfil e um cliente novo é classificado com cinco distâncias.
* **Evidência:** teste de escala (Seção 2.5): o hierárquico cresce com expoente próximo de 2. Comparação nos dados reais (Seção 3.10 b): Ward é instável (ARI de 0,52 contra 0,97), o GMM separa mal (silhouette de 0,12) e o DBSCAN varia de 1 a 16 grupos conforme os parâmetros.
* **Limite da decisão:** uma régua simples com a mesma informação separa o futuro tão bem quanto o K-means (ver D12). A escolha se sustenta em vantagens estruturais que a prova de conceito não mediu.
* **O que mudaria:** grupos alongados ou de densidades muito diferentes nos dados da empresa favoreceriam GMM ou métodos por densidade.

### D5. A base de dados

* **Alternativas:** Online Retail (um ano, usada na Aula 3); Online Retail II (dois anos); bases brasileiras de e-commerce; dados sintéticos.
* **Decisão:** Online Retail II.
* **Por quê:** é real, pública, com licença aberta, tem clientes em 41 países e registra estornos. Sobretudo, tem dois anos: o segundo ano permite validar o modelo no futuro, que é o que o exercício da aula deixou em aberto. Bases em que quase todo cliente compra uma única vez não sustentam variáveis de frequência.
* **O que mudaria:** nada na prova de conceito. No projeto, a base é a da empresa.

### D6. Desenho temporal

* **Decisão:** observar 12 meses, validar nos 12 seguintes; no notebook, a escolha de variáveis, transformações e *k* usa só medidas do ano 1.
* **Por quê:** 12 meses cobrem um ciclo sazonal completo (o pico de outubro e novembro). Separar um ano inteiro para validação evita escolher o modelo olhando o resultado que se quer validar.
* **Limite reconhecido:** a validação no ano 2 não foi totalmente cega. Durante o desenvolvimento, resultados do ano 2 foram vistos enquanto configurações alternativas eram exploradas. As escolhas finais se justificam por medidas do ano 1, mas não é possível garantir que não foram influenciadas. Não existe uma terceira janela para confirmação independente; esse papel cabe à validação com os dados da empresa.

### D7. Limpeza

* **Decisão:** cinco filtros aplicados em sequência e auditados (Seção 3.3). Linhas idênticas no mesmo pedido foram mantidas.
* **Por quê:** a sobreposição entre as duas abas da planilha duplicaria pedidos de dezembro de 2010. Códigos que não são mercadoria (frete, ajustes) distorcem ticket e estorno. As linhas idênticas podem ser leituras legítimas do mesmo produto, e são 1,4% das linhas elegíveis.
* **Limite reconhecido:** 22% das linhas de compra não têm cliente identificado e ficam fora.

### D8. As variáveis

* **Decisão:** recência, frequência, ticket médio e estornos por pedido (faturas de estorno divididas pelos pedidos de compra).
* **Valor total fora da distância:** valor = frequência × ticket. Depois do logaritmo, log(valor) = log(frequência) + log(ticket). Incluí-lo contaria a mesma informação duas vezes.
* **Estorno por frequência, não por valor:** o custo de servir vem de cada ocorrência, e o valor estornado é dominado por poucos clientes (no ano 1, 1% deles responde por mais da metade do valor estornado).
* **Evidência:** teste de sensibilidade com três versões (Seção 3.8). A versão adotada tem os grupos mais equilibrados e a maior estabilidade (0,97, contra 0,87 sem a variável e 0,90 com o estorno por valor).

### D9. Preparo da distância

* **Decisão:** logaritmo em frequência e ticket, log(1 + x) em recência, raiz quadrada na proporção de estorno; padronização em todas.
* **Por quê:** as variáveis são muito assimétricas e têm unidades diferentes. O K-means agrupa por distância e supõe grupos compactos.
* **Evidência:** sem preparo, o K-means coloca 70% dos clientes em um grupo e usa dois grupos para isolar algumas dezenas de casos extremos (Seção 3.7).

### D10. O número de segmentos

* **Alternativas:** *k* de 2 a 8.
* **Decisão:** *k* = 5.
* **Por quê:** *k* = 3 tem a maior silhouette, mas coloca 51% dos clientes em um grupo só. Entre as soluções mais finas, o que decide é a estabilidade: *k* = 5 fica acima de 0,9, e *k* = 4 e *k* = 6 mudam com a amostra.
* **O que mudaria:** se as áreas só conseguissem operar três políticas, *k* = 3 seria defensável e é igualmente estável.

### D11. Nomes e letras dos segmentos

* **Decisão:** nomes que descrevem o que as variáveis mostram; letras atribuídas por uma regra fixa sobre os centros.
* **Por quê:** a Aula 3 alertou que "cliente fiel e lucrativo" exige outras evidências. E os números dos grupos mudam entre execuções do K-means; a regra fixa impede que o texto fique dependente dessa numeração.

### D12. Como avaliar

* **Decisão:** cinco critérios (estável, persistente, informativo, acionável, escalável) e comparação com o acaso, com duas réguas tradicionais e com uma régua que recebe a mesma informação do modelo.
* **Por quê:** agrupamento não tem gabarito. Sem critérios declarados, qualquer resultado pode ser defendido. A comparação com réguas segue a regra da Aula 4: um modelo só vale se bater o ingênuo.
* **Resultado reportado como é:** com três variáveis, o K-means fica no patamar da curva ABC e do RF por regras em valor e recompra. Com a quarta variável, perde um pouco nessas duas medidas e separa o atrito futuro cerca de três vezes melhor que a curva ABC. E uma régua de seis grupos (três faixas de valor cruzadas com "teve estorno") iguala a proposta em atrito e a supera em valor e recompra.
* **O que concluímos:** o que pesou foi a informação nova, não o algoritmo. É a mesma lição do notebook de reinforcement learning da Aula 4. O K-means se mantém pelas vantagens estruturais (mais dimensões sem multiplicar células, recalibração por mercado, perfil em todas as variáveis), que são hipótese a confirmar com os dados da empresa.

### D13. Segmento como estado

* **Decisão:** atribuição recalculada todo mês; modelo retreinado uma vez por ano ou quando o monitoramento indicar.
* **Evidência:** a estrutura é estável (ARI de 0,88 entre o modelo congelado e um modelo novo), mas menos da metade dos clientes de cada segmento permanece nele um ano depois (Seção 3.10 c).

### D14. Monitoramento com referência sazonal

* **Decisão:** comparar a participação dos segmentos com o mesmo mês do ano anterior, não com o treino.
* **Evidência:** aplicado a janelas trimestrais, o modelo congelado mostra o segmento B caindo de 20% para 10% em março e voltando a 21% em dezembro (Seção 3.11 e). O modelo não envelheceu; a recência depende da época do ano em que a fotografia é tirada.
* **Limite:** a regra só pôde ser conferida para dezembro. Para os outros meses é hipótese.
* **Observação:** esse efeito não era esperado. Apareceu na simulação e foi mantido no trabalho como achado e como limitação.

### D15. Abstenção

* **Decisão:** a consulta se abstém com dado ausente, valor fora do domínio ou distância acima do percentil 99 do treino.
* **Por quê:** o K-means sempre devolve um grupo, mesmo para um cliente que não se parece com nenhum perfil.
* **Limite:** a distância não é probabilidade. O limiar é ponto de partida e deve ser recalibrado.

### D16. Valor como cenário, não como previsão

* **Decisão:** dimensionar o valor com hipóteses de efeito declaradas (Seção 4.3).
* **Por quê:** a base não tem custos, e o modelo descreve comportamento sem medir o efeito de nenhuma ação. Prometer um ganho seria inventar um número.

## 3. O que foi testado e descartado

| Tentativa | O que aconteceu | Onde |
|---|---|---|
| K-means sem preparo | 70% dos clientes em um grupo; dois grupos com menos de 30 clientes | Seção 3.7 |
| Só padronizar, sem logaritmo | melhora pouco; a assimetria continua | Seção 3.7 |
| Três variáveis, sem estorno | estável (0,87), mas menos que a versão adotada (0,97); não enxerga o atrito | Seção 3.8 |
| Régua informada (valor × teve estorno) | iguala a proposta em atrito e a supera em valor e recompra; mantida no trabalho como referência | Seção 3.10 |
| Estorno medido por valor | um grupo com menos de 8% dos clientes e partição menos estável (0,90) | Seção 3.8 |
| *k* = 3 | maior silhouette; metade da base em um único grupo | Seção 3.8 |
| *k* = 4 e *k* = 6 | instáveis ao reamostrar os clientes | Seção 3.8 |
| Hierárquico (Ward) | instável (0,52) e custo quadrático | Seções 2.5 e 3.10 |
| GMM | estável, mas com a pior separação entre grupos | Seção 3.10 |
| DBSCAN | de 1 a 16 grupos e de 3% a 72% de ruído, conforme os parâmetros | Seção 3.10 |
| Quantidade típica por item, como sinal de atacado | em exploração fora do notebook, piorou silhouette e estabilidade; não foi incluída | — |
| Redução de dimensão para visualizar | não usada: os gráficos mostram as próprias variáveis do modelo, como na Aula 3 | Seção 3.9 |

## 4. Perguntas críticas e respostas

**Por que K-means se uma régua simples faz o mesmo?**
Na prova de conceito, faz: três faixas de valor cruzadas com "teve estorno" separam o futuro tão bem quanto o modelo. Mantemos o K-means por razões que a prova de conceito não mede. Cada dimensão nova multiplica as células de uma régua e não muda o número de perfis do K-means. Os limites da régua precisam ser revistos por alguém em cada mercado; o K-means os recalcula a cada retreino. E o centro de cada segmento descreve o cliente em todas as variáveis de uma vez. Se a empresa fosse operar só com valor e estorno em um mercado, a régua bastaria, e dizemos isso no trabalho.

**Por que *k* = 5 se a silhouette é maior em *k* = 3?**
Com *k* = 3, metade dos clientes fica em um grupo que mistura o recente, o ocasional de ticket alto e o inativo. *k* = 5 é tão estável quanto *k* = 3 e separa esses três perfis.

**Uma silhouette de 0,27 não é baixa?**
É. Indica que os grupos se tocam: o comportamento de compra é um contínuo. Por isso a decisão não se apoia nela, e sim em estabilidade (0,96), persistência no ano seguinte (0,88) e separação do comportamento futuro. O trabalho trata os segmentos como uma convenção útil, não como grupos naturais (Seção 4.1).

**Como garantir que não houve vazamento do ano 2?**
Não há garantia completa. No notebook, variáveis, transformações e *k* são escolhidos com medidas do ano 1, e o ano 2 entra com o modelo congelado. Mas resultados do ano 2 foram vistos durante o desenvolvimento, e só há uma janela futura. O trabalho registra esse limite na Seção 4.1.

**O que é ARI e por que não usar acurácia?**
Acurácia exige a resposta certa de cada cliente, que não existe. O ARI compara duas partições e diz o quanto concordam, sem depender de como os grupos foram numerados. Vale 1 quando são idênticas e fica perto de 0 quando a concordância é a do acaso.

**Os dados são de uma loja britânica de 2009. O que isso prova para a empresa?**
Prova que o método se sustenta em dados reais de e-commerce: os segmentos são estáveis, reaparecem um ano depois e dizem algo sobre o futuro. Não prova nenhum número para a empresa. O roteiro (Seção 4.4) começa repetindo a validação com os dados dela.

**O segmento de estorno recorrente não é uma forma de discriminar clientes?**
Pode se tornar, se for usado para restringir. A proposta é usá-lo para investigar a causa do estorno, que pode estar na operação. Qualquer ação restritiva passa por revisão humana, e a composição de cada segmento é auditada a cada retreino (Seção 4.2).

**Como isso funciona com milhões de clientes em 12 países?**
O treino cresce de forma linear com a base, e há uma variante em lotes para bases que não cabem na memória. A atribuição mensal é um cálculo de distâncias, que pode ser feito no próprio banco de dados. A questão em aberto é a padronização por país, que a prova de conceito não pôde testar porque um país domina a base.

**O que seria feito de forma diferente com os dados da empresa?**
Separar cancelamento de devolução; incluir contatos de atendimento e custos; padronizar por país; tratar a sazonalidade da recência pelo ritmo de compra de cada cliente; e medir o efeito das ações com grupo de controle.

**Por que o nome Quantum Finance, se o enunciado descreve a Quantum Commerce?**
O trabalho leva o nome Quantum Finance. O enunciado descreve a operação de varejo com o nome Quantum Commerce. Tratamos as duas denominações como a mesma empresa e registramos isso na Seção 1.1.
