<div align="center">

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
     alt="Python"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg"
     alt="scikit-learn"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 01: Questionário
> Setup do Projeto de Machine Learning

---

**Questão 1**

Por que modelos baseados em árvores (como GradientBoosting) não foram escolhidos para o case do trocador de calor?

- a) São mais difíceis de instalar como dependência
- b) Não conseguem lidar com dados de sensores industriais
- c) Não extrapolam bem fora do range de treino, o que é necessário para projetar a degradação futura
- d) Geram arquivos `.pkl` maiores, o que prejudica o versionamento

<details>
<summary>Resposta</summary>

**c)** A eficiência cai de forma monotônica ao longo do tempo e precisamos projetar essa tendência para datas futuras. Modelos de árvore interpolam bem dentro do range de treino, mas não extrapolam  a Regressão Linear é a escolha correta para capturar e projetar essa degradação.

</details>

---

**Questão 2**

Qual é a diferença fundamental entre os artefatos de uma aplicação tradicional e os de um projeto de ML?

- a) Aplicações tradicionais não precisam de versionamento; projetos de ML sim
- b) Em ML, o artefato final é apenas o código Python treinado
- c) Projetos de ML geram código + modelo + dados + pré-processador, enquanto apps tradicionais entregam apenas código
- d) Aplicações tradicionais usam Docker; projetos de ML não precisam

<details>
<summary>Resposta</summary>

**c)** Essa diferença é central para entender por que reprodutibilidade é um desafio maior em ML. Um artefato de ML tem múltiplas dimensões: o código, o modelo serializado, os dados usados no treino e o pré-processador. Cada um tem seu próprio ciclo de vida.

</details>

---

**Questão 3**

O que acontece quando um cientista de dados treina um modelo com `sklearn 1.3` e um engenheiro tenta rodar a inferência com `sklearn 1.1`?

- a) O modelo é re-treinado automaticamente com a versão mais nova
- b) O resultado é idêntico, pois a lógica matemática não muda entre versões
- c) O `pickle` avisa sobre a incompatibilidade e recusa carregar o modelo
- d) Pode ocorrer erro, comportamento diferente ou, pior, resultados silenciosamente incorretos

<details>
<summary>Resposta</summary>

**d)** Esse é o problema real que o Docker resolve. Versões diferentes de bibliotecas podem produzir comportamentos distintos  e o pior cenário é quando não há erro explícito, mas os resultados são diferentes sem que ninguém perceba.

</details>
