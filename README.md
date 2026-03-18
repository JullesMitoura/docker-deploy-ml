<div align="center">

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>


<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
     alt="Python"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg"
     alt="Docker"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg"
     alt="scikit-learn"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)


<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

# Docker: Machine Learning para Produção
> Foco: Engenharia de ML, Reprodutibilidade, Produção, Workflow real

Curso prático que conduz o aluno desde a organização de um projeto de ML até o deploy completo de um modelo em produção usando Docker — com CI/CD, versionamento de artefatos e serving via API.

---

## Estrutura do Curso

| Aula | Tema | Resumo | Entrega |
|------|------|--------|---------|
| 01 | [Setup do Projeto de ML](./modulo1/) | Estrutura do projeto, script de treino e inferência rodando localmente | Repositório base funcional, projeto rodando localmente |
| 02 | [Containerizando o Projeto](./modulo2/) | Primeiro Dockerfile, instalação de dependências e execução do treino em container | Projeto rodando em container |
| 03 | Treino e Inferência em Containers Separados | Dockerfiles distintos para treino e inferência com dependências e entrypoints isolados | Dois containers com responsabilidades claras |
| 04 | Otimizando Imagens Docker para ML | Multi-stage build, cache de dependências e redução do tamanho final da imagem | Imagens menores e mais rápidas |
| 05 | Persistindo e Versionando o Modelo | Uso de volumes para salvar o modelo fora do container e versionamento manual de artefatos | Modelo versionado fora da imagem |
| 06 | Automatizando o Build com GitHub Actions | Workflow de CI com build automático, teste do container e cache de build | CI funcionando |
| 07 | Publicando a Imagem no Docker Hub | Autenticação, tags por versão e push automático da imagem via GitHub Actions | Imagem publicada e reutilizável |
| 08 | Servindo o Modelo via API | API FastAPI containerizada com endpoint de predição carregando o modelo treinado | API de inferência rodando em Docker |
| 09 | Configurando o Ambiente de Produção | Variáveis de ambiente, logs e diferenças entre ambientes dev e prod no Docker | Pipeline completo local |
| 10 | Pipeline End-to-End de ML em Produção | Revisão do fluxo completo de treino, build, push e serving com checklist técnico de ML | Projeto finalizado |

---

## Case do Curso

O projeto de ML usado ao longo do curso é um **modelo de monitoramento de trocador de calor** com `scikit-learn`. A escolha foi intencional:

- Dataset leve, com dados reais de sensores industriais (175 registros diários)
- Problema de regressão com tendência temporal clara
- Fácil de entender, mas com estrutura de código similar à produção
- Permite demonstrar todos os conceitos de Docker sem distração de complexidade de dados

### O problema

Modelar a **degradação da eficiência térmica** ao longo do tempo (~-0.018% por dia), com duas capacidades de inferência:
1. Dado uma **data** → prever a eficiência esperada
2. Dado um **valor de eficiência** → encontrar as datas históricas mais próximas

---

## Jornada do Aluno

```
Aula 01-02 → Projeto rodando em container
Aula 03-05 → Boas práticas de Docker para ML
Aula 06-07 → Automação com CI/CD
Aula 08-09 → Serving e ambiente de produção
Aula 10    → Pipeline end-to-end completo
```

---

## Pré-requisitos

- Python 3.11
- Docker instalado e rodando
- Git e conta no GitHub
- Conta no Docker Hub (necessário a partir da Aula 7)

---

## Como navegar

Cada módulo tem seu próprio `README.md` com:
- Contexto teórico da aula
- Passo a passo prático
- Comandos prontos para executar
- Checklist de entrega