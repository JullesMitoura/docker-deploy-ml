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

## Módulo 01: Setup do Projeto de Machine Learning
> **Entrega**: repositório base funcional, projeto rodando localmente

---

Antes de pensar em containers ou deploy, é necessário ter um projeto de ML bem estruturado. Este módulo estabelece a fundação de tudo que vem a seguir: um repositório organizado, com separação clara entre treino e inferência, rodando localmente de forma reproduzível.

A pergunta central aqui não é "como o Docker funciona?", mas sim **"o que vamos containerizar?"**. Entender a anatomia do projeto  dados, código, artefatos e dependências  é o primeiro passo para tomar boas decisões de engenharia nos módulos seguintes.

### O que você vai aprender

- Como estruturar um projeto de ML com separação entre `train.py` e `inference.py`
- Gerenciamento de dependências com `requirements.txt`
- O papel de cada diretório: `data/`, `models/`, `src/`
- Por que projetos de ML têm desafios de reprodutibilidade que aplicações tradicionais não têm

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `train.py` | Script responsável por treinar o modelo e salvar o artefato |
| `inference.py` | Script que carrega o modelo treinado e gera predições |
| `requirements.txt` | Especificação explícita das dependências do projeto |
| Separação de responsabilidades | Treino e inferência como etapas distintas do ciclo de vida |

### Case do curso

O projeto usa um **modelo de monitoramento de trocador de calor**: dado um conjunto de leituras de sensores industriais, o modelo aprende a degradação da eficiência térmica ao longo do tempo. É um problema de regressão simples o suficiente para não distrair, mas realista o suficiente para demonstrar todos os conceitos de produção que o curso aborda.
