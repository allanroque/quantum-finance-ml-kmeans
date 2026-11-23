# Quantum Finance — Machine Learning

**Segmentação de clientes por valor e custo de servir com K-means**

Trabalho final de uma disciplina de Machine Learning em nível de pós-graduação.

## O que é

Uma proposta de aplicação de K-means para segmentar a base de clientes de uma operação de varejo omnicanal presente em 12 países, sustentada por uma prova de conceito com dados reais de e-commerce. O recorte é **valor × custo de servir**: além de quanto o cliente compra, o modelo considera com que frequência ele gera estornos (cancelamentos e devoluções), para que a mesma segmentação sirva a marketing, suporte e logística.

## Por onde começar

| Se você quer | Abra |
|---|---|
| Ler o trabalho completo, sem executar nada | [`Quantum_Finance_ML_Segmentacao_de_Clientes.pdf`](Quantum_Finance_ML_Segmentacao_de_Clientes.pdf) ou o `.html` |
| Ver e executar o código | [`Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb`](Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb) |
| Entender por que cada escolha foi feita | [`docs/Racional_e_Decisoes.pdf`](docs/Racional_e_Decisoes.pdf) |

O notebook já está executado, com todas as saídas salvas.

## Onde está cada tópico do enunciado

| Tópico pedido | Seção do notebook |
|---|---|
| 1. Introdução e Problemática | Seção 1 |
| 2. Motivação e Justificativa da Arquitetura | Seção 2 (argumento e teste de escala) e Seção 3.10 (b) (comparação com dados reais) |
| 3. Proposta de Solução | Seção 3: arquitetura (3.1), dados (3.2 a 3.5), pipeline de treinamento (3.6 a 3.9), avaliação (3.10), consumo (3.11 e 3.12) |
| 4. Considerações e Potencial de Impacto | Seção 4: limitações (4.1), riscos (4.2), valor (4.3), roteiro (4.4) |

## Principais resultados da prova de conceito

* **Cinco segmentos** de tamanho parecido (19% a 21% dos clientes cada), descritos por recência, frequência, ticket médio e estornos por pedido.
* **Estáveis:** ARI acima de 0,96 ao reamostrar os clientes e reajustar o modelo.
* **Persistentes:** o modelo treinado no ano 1 e um modelo treinado do zero no ano 2 concordam em 0,88 de ARI.
* **Informativos:** a recompra no ano seguinte vai de 93% no segmento de maior valor a 36% no inativo.
* **Além da curva ABC:** um em cada quatro clientes da faixa de maior valor está em um segmento de risco ou de atrito que a curva ABC não distingue.

Dois resultados limitam a proposta e estão reportados no notebook. Uma régua simples que receba a mesma informação (faixas de valor cruzadas com "teve estorno") separa o futuro tão bem quanto o modelo: o que pesa é a informação, não o algoritmo, e a vantagem do K-means em dimensões e em mercados ainda precisa ser confirmada com os dados da empresa. E a participação dos segmentos oscila ao longo do ano, por causa da sazonalidade das compras, o que exige uma referência sazonal no monitoramento.

## Estrutura do repositório

```
Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb   notebook executado (entrega principal)
Quantum_Finance_ML_Segmentacao_de_Clientes.html    o mesmo conteúdo, para ler no navegador
Quantum_Finance_ML_Segmentacao_de_Clientes.pdf     o mesmo conteúdo, como documento escrito
docs/
  Racional_e_Decisoes.md / .pdf                    registro das decisões e perguntas prováveis
saidas/
  segmentos_clientes.csv                           um cliente por linha, com segmento e distância
  perfil_dos_segmentos.csv                         perfil de cada segmento
  manifesto_modelo.json                            parâmetros, centros, versões e identificação dos dados
requirements.txt                                   bibliotecas e versões
_build/                                            fontes do notebook e scripts de montagem e exportação
```

## Como executar

**No Google Colab (recomendado).** Envie o arquivo `.ipynb` e execute as células em ordem. Não é preciso instalar nada. A primeira execução baixa a base (45 MB) do repositório da UCI e leva alguns minutos.

**Localmente.**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb
```

O notebook cria duas pastas ao lado dele: `data/` (a base baixada e uma cópia de leitura rápida) e `saidas/` (os artefatos). Nenhuma das duas precisa existir antes.

Se o download automático falhar, baixe o arquivo em <https://archive.ics.uci.edu/dataset/502/online+retail+ii> e salve como `data/online_retail_ii.zip`.

## Dados

[Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), UCI Machine Learning Repository, licença CC BY 4.0. Transações reais de um varejista online britânico entre dezembro de 2009 e dezembro de 2011. A base não é redistribuída aqui; o notebook a baixa e confere o SHA-256.

> Chen, D. (2012). *Online Retail II* [conjunto de dados]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D

Os números da prova de conceito descrevem essa loja, não a empresa do enunciado. O que se transfere é o método.

## Como o notebook é montado

O notebook é gerado a partir dos arquivos em `_build/src/`, que alternam blocos de texto e de código. Para reconstruir, executar e exportar:

```bash
pip install -r requirements.txt nbclient nbconvert markdown
python _build/build.py /caminho/para/uma/pasta/de/execucao
python _build/exportar.py
```

A exportação para PDF usa o Google Chrome em modo sem interface.

Este repositório traz a versão pública do trabalho, sem a identificação da instituição, do professor e dos integrantes. A versão de entrega é montada por `_build/entrega.py` a partir de um arquivo de identificação mantido fora do repositório.
