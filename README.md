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
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

# Docker: Machine Learning para Produção
> Foco: Engenharia de ML, Reprodutibilidade, Produção, Workflow real

Curso prático que conduz o aluno desde a organização de um projeto de ML até o deploy completo de um modelo em produção usando Docker  com CI/CD, versionamento de artefatos e serving via API REST.

---

## Estrutura do Curso

| Módulo | Tema | Entrega | Conceito central |
|--------|------|---------|-----------------|
| [01](./modulo1/) | Setup do Projeto de ML | Repositório base funcional, projeto rodando localmente | Estrutura de projeto de ML, `train.py`, `inference.py` |
| [02](./modulo2/) | Containerizando o Projeto | Projeto rodando em container | Dockerfile, imagem base, variáveis de ambiente, cache de layers |
| [03](./modulo3/) | Treino e Inferência Separados | Dois containers com responsabilidades claras | Responsabilidade única, `Dockerfile.train`, `Dockerfile.inference`, volumes |
| [04](./modulo4/) | Otimizando Imagens | Imagens menores e mais rápidas | Multi-stage build, `.dockerignore`, estratégia de cache |
| [05](./modulo5/) | Versionando Artefatos | Modelo versionado fora da imagem | `model_{tag}.pkl`, `registry.json`, `model_latest.pkl`, rollback |
| [06](./modulo6/) | CI com GitHub Actions | CI funcionando | Workflow YAML, jobs paralelos, artefatos entre jobs, cache GHA |
| [07](./modulo7/) | Publicando no Docker Hub | Imagem publicada e reutilizável | `docker/login-action`, `metadata-action`, estratégia de branches e tags |
| [08](./modulo8/) | Serving via API | API de inferência rodando em Docker | FastAPI, uvicorn, `lifespan`, endpoints REST, `PYTHONPATH` |
| [09](./modulo9/) | Ambiente de Produção | Pipeline completo local | Docker Compose, `depends_on`, `HEALTHCHECK`, dev vs prod, `.env` |
| [10](./modulo10/) | Workflow End-to-End | Projeto finalizado | Makefile, smoke test no CI, pipeline treino → build → push → serving |

---

## Case do Curso

O projeto de ML usado ao longo do curso é um **modelo de monitoramento de trocador de calor** com `scikit-learn`. A escolha foi intencional:

- Dataset leve com dados reais de sensores industriais (175 registros diários)
- Problema de regressão com tendência temporal clara e interpretável
- Código com estrutura similar à produção, sem distração de complexidade de dados
- Permite demonstrar todos os conceitos de Docker do zero ao deploy

### O problema

Modelar a **degradação da eficiência térmica** ao longo do tempo (~-0.018% por dia), com duas capacidades de inferência:

1. Dado uma **data** → prever a eficiência esperada
2. Dado um **valor de eficiência** → estimar a data correspondente (histórico ou extrapolação)

---

## Jornada do Aluno

```
Módulos 01–02   Projeto rodando em container
     │
     ▼
Módulos 03–05   Boas práticas de Docker para ML
     │           (responsabilidade única, multi-stage, versionamento)
     ▼
Módulos 06–07   Automação com CI/CD
     │           (GitHub Actions, Docker Hub, estratégia de branches)
     ▼
Módulos 08–09   Serving e ambiente de produção
     │           (FastAPI, Docker Compose, HEALTHCHECK, dev vs prod)
     ▼
Módulo 10       Pipeline end-to-end completo
                (Makefile, smoke test, checklist de produção)
```

---

## Evolução do projeto módulo a módulo

```
modulo1/
├── src/
│   ├── train.py
│   └── inference.py
├── data/
└── requirements.txt

modulo2/
├── Dockerfile
└── ...

modulo3/
├── Dockerfile.train
├── Dockerfile.inference
├── requirements-train.txt
└── requirements-inference.txt

modulo4/
├── Dockerfile.train
├── Dockerfile.inference
└── .dockerignore

modulo5/
├── src/
│   ├── train.py
│   ├── inference.py
│   └── utils/
│       ├── logger.py
│       └── versioning.py
└── models/
    ├── model_20240101_143052.pkl
    ├── model_latest.pkl
    └── registry.json

modulo6/
└── .github/workflows/modulo6-ci.yml

modulo7/
└── .github/workflows/modulo7-cd.yml

modulo8/
├── src/
│   └── app.py
├── Dockerfile.serve
└── requirements-serve.txt

modulo9/
├── docker-compose.yml
├── docker-compose.override.yml
├── Dockerfile.serve
└── .env.example

modulo10/
├── Makefile
├── docker-compose.yml
└── .github/workflows/modulo10-pipeline.yml
```

---

## Pré-requisitos

- Python 3.11
- Docker Desktop instalado e rodando
- Git e conta no GitHub
- Conta no Docker Hub (necessário a partir do módulo 7)

---

## GitHub Actions Workflows

| Workflow | Disparo | O que faz |
|----------|---------|-----------|
| [`modulo6-ci.yml`](.github/workflows/modulo6-ci.yml) | Push/PR em `modulo6/**` | Build paralelo + testes de integração |
| [`modulo7-cd.yml`](.github/workflows/modulo7-cd.yml) | Push/PR em `modulo7/**` | Build + testes + push ao Docker Hub |
| [`modulo10-pipeline.yml`](.github/workflows/modulo10-pipeline.yml) | Push/PR em `modulo10/**` | Pipeline completo com smoke test da API |

---

## Como navegar

Cada módulo tem seu próprio `README.md` com:
- Contexto teórico: o problema que o módulo resolve
- Passo a passo prático com comandos prontos
- Comparação com o módulo anterior
- Checklist de entrega
