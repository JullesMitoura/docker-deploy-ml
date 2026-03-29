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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg"
     alt="FastAPI"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 08: Serving do modelo
> Entrega: API de inferência rodando em Docker

---

## O problema do módulo anterior

Nos módulos anteriores, a inferência é feita via CLI  um script Python que lê o modelo, imprime o resultado e encerra. Isso funciona para uso manual, mas não para produção:

```bash
# CLI (módulos anteriores)  uma predição por execução, sem estado, sem concorrência
docker run heat-exchanger-inference python src/inference.py --date 2022-04-15
```

**Em produção, você precisa de:**
- Um servidor que fique em execução contínua
- Endpoint HTTP que outros serviços possam chamar
- Modelo carregado **uma vez** em memória (não re-carregado a cada predição)
- Suporte a múltiplas requisições simultâneas

---

## A solução: FastAPI + uvicorn

```
Cliente HTTP                  Container de serving
─────────────                 ─────────────────────────────────────
curl / frontend  ──POST──►   uvicorn (servidor ASGI)
                              └─► FastAPI app
                              └─► modelo carregado na memória ─► resposta JSON
```

`FastAPI` cuida das rotas, validação de dados e documentação automática.
`uvicorn` é o servidor ASGI que recebe as conexões HTTP e executa a app.

---

## Arquitetura de containers deste módulo

```
┌──────────────────────┐        volume: ./models/        ┌──────────────────────────────┐
│  heat-exchanger-     │  ──── model.pkl ────────────►  │  heat-exchanger-serve        │
│  train               │                                  │                              │
│  (roda uma vez)      │        registry.json             │  FastAPI + uvicorn           │
└──────────────────────┘                                  │  porta 8000                  │
                                                          │  modelo em memória           │
                                                          └──────────────────────────────┘
```

---

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Informações da API e versão do modelo carregado |
| `GET` | `/health` | Health check  usado por load balancers |
| `POST` | `/predict/date` | Prediz eficiência para uma data |
| `POST` | `/predict/efficiency` | Estima a data para uma eficiência alvo |
| `GET` | `/versions` | Lista versões de modelo disponíveis |
| `GET` | `/docs` | Documentação interativa (Swagger UI  automática) |

---

## Novidades no código

### `src/app.py` (novo)

O modelo é carregado **uma única vez** no startup via `lifespan`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # executa ANTES da API aceitar requisições
    artifact = pickle.load(open(model_path, "rb"))
    _model, _origin_date, _last_date = ...
    yield
    # executa APÓS o shutdown
```

Após o startup, todas as requisições usam o modelo já em memória  sem re-carregar o arquivo a cada chamada.

### `Dockerfile.serve` (novo)

```
PYTHONPATH=/app/src  → uvicorn encontra app.py e utils/
EXPOSE 8000          → documenta a porta da API
CMD uvicorn app:app  → mantém o servidor em execução contínua
```

### `requirements-serve.txt` (novo)

```
fastapi==0.115.6        → framework de API
uvicorn[standard]==0.32.1  → servidor ASGI
scikit-learn, pandas, numpy  → carregamento e uso do modelo
```

`sqlalchemy` não está aqui  a API nunca acessa o banco de dados.

---

## Estrutura dos arquivos deste módulo

```
modulo8/
├── Dockerfile.train        # gera artefatos versionados (módulo 05)
├── Dockerfile.serve        # NOVO: FastAPI + uvicorn
├── .dockerignore
├── requirements-train.txt
├── requirements-serve.txt  # NOVO: fastapi + uvicorn
├── src/
│   ├── train.py            # pipeline de treino (módulo 05)
│   ├── inference.py        # CLI de inferência (módulo 05)  mantido
│   ├── app.py              # NOVO: FastAPI application
│   └── utils/
│       ├── logger.py
│       └── versioning.py
├── data/
│   └── heat_exchanger.db
└── models/                 # volume compartilhado entre treino e serving
```

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo8
```

### 2. Build das imagens

```bash
docker build -f Dockerfile.train -t heat-exchanger-train .
docker build -f Dockerfile.serve -t heat-exchanger-serve .
```

### 3. Execute o treino para gerar os artefatos

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-train
```

```bash
ls -lh models/
# model_20240101_143052.pkl
# model_latest.pkl
# registry.json
```

### 4. Suba a API de serving

```bash
docker run -d \
  --name heat-serve \
  -v $(pwd)/models:/app/models \
  -p 8000:8000 \
  heat-exchanger-serve
```

- `-d` → roda em background (detached)
- `-p 8000:8000` → publica a porta 8000 do container na sua máquina

Verifique que a API subiu:
```bash
docker logs heat-serve
```
```
INFO     | Carregando modelo: models/model_latest.pkl
INFO     | Modelo carregado  versão: 20240101_143052 | período: 2022-01-01 → 2022-06-30
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5. Teste os endpoints

**Health check:**
```bash
curl http://localhost:8000/health
```
```json
{"status": "ok", "model_version": "20240101_143052", "model_dir": "models"}
```

**Predição por data:**
```bash
curl -X POST http://localhost:8000/predict/date \
  -H "Content-Type: application/json" \
  -d '{"date": "2022-04-15"}'
```
```json
{
  "input_date": "2022-04-15",
  "predicted_efficiency": 94.2341,
  "model_version": "20240101_143052"
}
```

**Predição por eficiência alvo:**
```bash
curl -X POST http://localhost:8000/predict/efficiency \
  -H "Content-Type: application/json" \
  -d '{"efficiency": 94.5}'
```
```json
{
  "target_efficiency": 94.5,
  "predicted_date": "2022-04-03",
  "in_history": true,
  "model_version": "20240101_143052"
}
```

**Listar versões:**
```bash
curl http://localhost:8000/versions
```

### 6. Documentação interativa (Swagger UI)

Acesse no navegador:
```
http://localhost:8000/docs
```

FastAPI gera automaticamente uma interface interativa onde você pode testar os endpoints sem usar curl.

### 7. Troque a versão do modelo sem rebuild

```bash
# Para o container atual
docker stop heat-serve && docker rm heat-serve

# Sobe com versão específica
docker run -d \
  --name heat-serve \
  -v $(pwd)/models:/app/models \
  -p 8000:8000 \
  -e MODEL_VERSION=20240101_143052 \
  heat-exchanger-serve
```

Nenhum rebuild, nenhuma alteração de código.

### 8. Encerre o container

```bash
docker stop heat-serve && docker rm heat-serve
```

---

## Por que FastAPI?

| | Script CLI (módulos anteriores) | FastAPI (módulo 08) |
|---|---|---|
| Execução | Uma predição → encerra | Contínua (server) |
| Modelo carregado | A cada chamada | Uma vez no startup |
| Acesso | Terminal local | HTTP  qualquer cliente |
| Concorrência | 1 por vez | Múltiplas requisições |
| Documentação | README manual | /docs automático |
| Healthcheck | Não | GET /health |
| Validação de entrada | Manual | Pydantic automático |

---

## Checklist de Entrega

- [ ] `docker build -f Dockerfile.serve` conclui sem erros
- [ ] `docker run -v ... -p 8000:8000 heat-exchanger-serve` sobe a API
- [ ] `GET /health` retorna `{"status": "ok"}`
- [ ] `POST /predict/date` retorna eficiência prevista corretamente
- [ ] `POST /predict/efficiency` retorna data estimada corretamente
- [ ] Documentação interativa acessível em `http://localhost:8000/docs`
- [ ] `GET /versions` lista versões do registry
- [ ] Troca de versão via `MODEL_VERSION` funciona sem rebuild
- [ ] Entendeu a diferença entre CLI (inference.py) e serving (app.py)

---
