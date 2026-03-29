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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/githubactions/githubactions-original.svg"
     alt="GitHub Actions"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg"
     alt="FastAPI"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 10: Workflow completo de ML em produção
> Entrega: projeto finalizado

---

## Do commit ao container publicado

Este módulo une tudo que foi construído ao longo do curso em um pipeline end-to-end funcional.

```
git push main
     │
     ▼
GitHub Actions
├── build-train  ──┐
│                  ├──► test ──────────────────────────────────────► publish (se main/tag)
└── build-serve  ──┘    │                                                │
                         ├── treino → artefatos versionados              ├── :latest
                         ├── inferência CLI                              ├── :main
                         └── smoke test da API                           └── :{sha}
```

---

## O fluxo completo: Treino → Build → Push → Serving

### Localmente (via Makefile)

```bash
cd modulo10
cp .env.example .env

make up              # build + train + serve em um comando
make health          # verifica a API
make predict-date DATE=2022-04-15
make predict-efficiency EFFICIENCY=94.5
make versions
make stop
```

### Via CI/CD (GitHub Actions)

```bash
git push origin main          # dispara o pipeline
# → build-train + build-serve (paralelos, com cache GHA)
# → test (treino + inferência CLI + smoke test HTTP da API)
# → push ao Docker Hub (main → :latest + :{sha})
```

```bash
git tag v1.0.0 && git push origin v1.0.0
# → mesmo pipeline
# → tags semver: :v1.0.0 + :1.0 + :1 + :latest
```

---

## Estrutura dos arquivos deste módulo

```
modulo10/
├── Makefile                    # atalhos para todos os comandos do curso
├── docker-compose.yml          # pipeline local orquestrado
├── .env.example                # template de variáveis de ambiente
├── Dockerfile.train            # multi-stage, artefatos versionados
├── Dockerfile.serve            # multi-stage, FastAPI + HEALTHCHECK
├── .dockerignore
├── requirements-train.txt
├── requirements-serve.txt
├── src/
│   ├── train.py                # treino com versionamento
│   ├── app.py                  # API FastAPI completa
│   └── utils/
│       ├── logger.py
│       └── versioning.py
├── data/
│   └── heat_exchanger.db
└── models/
    └── .gitkeep

.github/workflows/
└── modulo10-pipeline.yml       # CI/CD end-to-end com smoke test da API
```

---

## Revisão: o que foi construído em cada módulo

| Módulo | Entrega | Conceito central |
|--------|---------|-----------------|
| 01 | Projeto local funcional | Estrutura de projeto de ML |
| 02 | Container básico | Dockerfile, imagem base, variáveis de ambiente |
| 03 | Dois containers com responsabilidades claras | Responsabilidade única, requirements separados |
| 04 | Imagens menores | Multi-stage build, .dockerignore |
| 05 | Modelo versionado fora da imagem | Volumes, registry.json, `model_{tag}.pkl` |
| 06 | CI funcionando | GitHub Actions, cache de build, artefatos entre jobs |
| 07 | Imagem publicada | Docker Hub, `metadata-action`, estratégia de branches |
| 08 | API de inferência | FastAPI, uvicorn, lifespan, endpoints REST |
| 09 | Pipeline local completo | Docker Compose, dev vs prod, HEALTHCHECK |
| 10 | Projeto finalizado | Makefile, smoke test, pipeline end-to-end |

---

## Checklist técnico de ML em produção

### Código e ambiente
- [ ] Dependências fixadas com versão exata (`scikit-learn==1.8.0`)
- [ ] Imagem base fixada (`python:3.11-slim`, não `python:latest`)
- [ ] `.dockerignore` excluindo notebooks, `.venv`, `.env`, artefatos de modelo
- [ ] Variáveis de ambiente para configuração (sem hardcode)
- [ ] `PYTHONUNBUFFERED=1` para logs em tempo real

### Imagem Docker
- [ ] Multi-stage build (imagem final sem compiladores)
- [ ] Dependências copiadas antes do código (cache eficiente)
- [ ] Código e dados em camadas separadas
- [ ] `HEALTHCHECK` definido no Dockerfile
- [ ] `EXPOSE` documenta a porta corretamente

### Artefatos de modelo
- [ ] Modelo **nunca** embutido na imagem
- [ ] Versionamento por timestamp (`model_{YYYYMMDD_HHMMSS}.pkl`)
- [ ] `model_latest.pkl` sempre atualizado após treino
- [ ] `registry.json` com metadados e métricas de cada versão
- [ ] Rollback via `MODEL_VERSION` sem rebuild

### CI/CD
- [ ] Build automático em cada push
- [ ] Testes de integração (treino + inferência) antes do push
- [ ] Smoke test da API no pipeline
- [ ] Push ao Docker Hub apenas em main ou tags semver
- [ ] PRs não publicam imagens
- [ ] Cache de build configurado (`type=gha`)

### API de serving
- [ ] Modelo carregado uma única vez no startup (`lifespan`)
- [ ] `GET /health` para health checks
- [ ] Versão do modelo retornada em cada resposta
- [ ] Logs estruturados com nível configurável
- [ ] `restart: unless-stopped` em produção

---

## Próximos passos

Este curso cobriu o ciclo básico de ML em produção com Docker. Os temas abaixo são os passos naturais para evoluir o projeto:

### Orquestração
- **Kubernetes**  escala horizontal de pods de serving, rolling updates, liveness/readiness probes
- **Docker Swarm**  alternativa mais simples ao Kubernetes para clusters pequenos

### MLOps e rastreabilidade
- **MLflow**  tracking de experimentos, model registry com versionamento automático, model serving
- **DVC**  versionamento de dados e pipelines de ML (complementa o git)
- **Weights & Biases**  visualização de treino e comparação de modelos

### Monitoramento
- **Prometheus + Grafana**  métricas de infraestrutura e da API (latência, throughput)
- **Data drift detection**  monitorar se os dados de entrada mudaram em relação ao treino
- **Evidently AI**  relatórios automáticos de drift e qualidade do modelo

### Deploy em nuvem
- **AWS ECS / Fargate**  containers gerenciados na AWS
- **Google Cloud Run**  containers serverless no GCP
- **Azure Container Instances**  containers na Azure

---

## Checklist de Entrega

- [ ] `make up` executa o pipeline completo (build + train + serve) sem erros
- [ ] `make health` retorna `{"status": "ok"}`
- [ ] `make predict-date DATE=2022-04-15` retorna eficiência prevista
- [ ] `make predict-efficiency EFFICIENCY=94.5` retorna data estimada
- [ ] Push em `main` dispara o workflow e publica no Docker Hub
- [ ] Smoke test da API passa no CI (GET /health + POST /predict/*)
- [ ] Tags `:latest` e `:{sha}` visíveis no Docker Hub
- [ ] Git tag `v1.0.0` gera tags semver no Docker Hub

---
